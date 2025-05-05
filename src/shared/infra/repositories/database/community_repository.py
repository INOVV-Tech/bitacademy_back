from boto3.dynamodb.conditions import Attr

from src.shared.infra.external.dynamo_datasource import DynamoDatasource

from src.shared.domain.repositories.community_repository_interface import ICommunityRepository

from src.shared.domain.enums.role import ROLE
from src.shared.domain.enums.community_type import COMMUNITY_TYPE
from src.shared.domain.enums.community_permission import COMMUNITY_PERMISSION
from src.shared.domain.entities.community import CommunityChannel, \
    CommunityForumTopic, CommunitySession

from src.shared.infra.external.key_formatters import encode_idx_pk

class CommunityRepositoryDynamo(ICommunityRepository):
    dynamo: DynamoDatasource
    
    def __init__(self, dynamo: DynamoDatasource):
        self.dynamo = dynamo

    ### CHANNEL ###
    @staticmethod
    def community_channel_partition_key_format(community_channel: CommunityChannel) -> str:
        return f'COMMUNITY_CHANNEL#{community_channel.id}'
    
    @staticmethod
    def community_channel_partition_key_format_from_id(id: str) -> str:
        return f'COMMUNITY_CHANNEL#{id}'
    
    @staticmethod
    def community_channel_sort_key_format() -> str:
        return 'METADATA'

    @staticmethod
    def community_channel_gsi_entity_get_all_pk() -> str:
        return 'INDEX#COMMUNITY_CHANNEL'
    
    @staticmethod
    def community_channel_gsi_entity_get_all_sk(community_channel: CommunityChannel) -> str:
        return f'DATE#{community_channel.created_at}'

    def create_channel(self, community_channel: CommunityChannel) -> CommunityChannel:
        item = community_channel.to_dict()

        item['PK'] = self.community_channel_partition_key_format(community_channel)
        item['SK'] = self.community_channel_sort_key_format()
        item[encode_idx_pk('GSI#ENTITY_GETALL#PK')] = self.community_channel_gsi_entity_get_all_pk()
        item[encode_idx_pk('GSI#ENTITY_GETALL#SK')] = self.community_channel_gsi_entity_get_all_sk(community_channel)

        self.dynamo.put_item(item=item)

        return community_channel

    def get_all_channels(self,
        title: str = '',
        comm_types: list[COMMUNITY_TYPE] = [],
        user_role: ROLE | None = None,
        limit: int = 10, last_evaluated_key: dict | None = None, sort_order: str = 'desc') -> dict:
        filter_expressions = []
        
        if title != '':
            filter_expressions.append(Attr('title').contains(title))

        if len(comm_types) > 0:
            comm_types_filter_expression = None

            for comm_type in comm_types:
                if comm_types_filter_expression is None:
                    comm_types_filter_expression = Attr('comm_type').eq(comm_type.value)
                else:
                    comm_types_filter_expression |= Attr('comm_type').eq(comm_type.value)

            filter_expressions.append(comm_types_filter_expression)

        if user_role is not None:
            filter_expressions.append(Attr(f'permissions.{user_role.value}').ne(COMMUNITY_PERMISSION.FORBIDDEN.value))

        filter_expression= None

        if len(filter_expressions) > 0:
            for f_exp in filter_expressions:
                if filter_expression is None:
                    filter_expression = f_exp
                else:
                    filter_expression &= f_exp

        response = self.dynamo.query(
            index_name='GetAllEntities',
            partition_key=self.community_channel_gsi_entity_get_all_pk(),
            limit=limit,
            exclusive_start_key=last_evaluated_key if last_evaluated_key != '' else None,
            filter_expression=filter_expression,
            scan_index_forward=False if sort_order == 'desc' else True
        )

        count_response = self.dynamo.count(
            index_name='GetAllEntities',
            partition_key=self.community_channel_gsi_entity_get_all_pk(),
            filter_expression=filter_expression,
        )
        
        return {
            'community_channels': [ CommunityChannel.from_dict_static(item) for item in response['items'] ],
            'last_evaluated_key': response.get('last_evaluated_key'),
            'total': count_response['count']
        }
    
    def get_one_channel(self, id: str) -> CommunityChannel | None:
        data = self.dynamo.get_item(
            partition_key=self.community_channel_partition_key_format_from_id(id),
            sort_key=self.community_channel_sort_key_format()
        )

        return CommunityChannel.from_dict_static(data['Item']) if 'Item' in data else None
    
    def get_one_channel_by_title(self, title: str) -> CommunityChannel | None:
        filter_expression = Attr('title').contains(title)

        data = self.dynamo.query(
            index_name='GetAllEntities',
            partition_key=self.community_channel_gsi_entity_get_all_pk(),
            filter_expression=filter_expression
        )
        
        items = data['items']

        return CommunityChannel.from_dict_static(items[0]) if len(items) > 0 else None

    def update_channel(self, community_channel: CommunityChannel) -> CommunityChannel:
        item = community_channel.to_dict()

        item['PK'] = self.community_channel_partition_key_format(community_channel)
        item['SK'] = self.community_channel_sort_key_format()
        item[encode_idx_pk('GSI#ENTITY_GETALL#PK')] = self.community_channel_gsi_entity_get_all_pk()
        item[encode_idx_pk('GSI#ENTITY_GETALL#SK')] = self.community_channel_gsi_entity_get_all_sk(community_channel)

        self.dynamo.put_item(item=item)
        
        return community_channel

    def delete_channel(self, id: str) -> int:
        resp = self.dynamo.delete_item(
            partition_key=self.community_channel_partition_key_format_from_id(id),
            sort_key=self.community_channel_sort_key_format()
        )

        return resp['ResponseMetadata']['HTTPStatusCode']
    
    def role_can_read_channel(self, channel_id: str, user_role: ROLE) -> bool:
        filter_expression = Attr(f'permissions.{user_role.value}').ne(COMMUNITY_PERMISSION.FORBIDDEN.value)

        count_response = self.dynamo.count(
            partition_key=self.community_channel_partition_key_format_from_id(channel_id),
            filter_expression=filter_expression,
        )

        return count_response['count'] > 0
    
    def role_can_edit_channel(self, channel_id: str, user_role: ROLE) -> bool:
        filter_expression = Attr(f'permissions.{user_role.value}').eq(COMMUNITY_PERMISSION.READ_WRITE_EDIT.value)

        count_response = self.dynamo.count(
            partition_key=self.community_channel_partition_key_format_from_id(channel_id),
            filter_expression=filter_expression,
        )

        return count_response['count'] > 0

    ### FORUM ###
    @staticmethod
    def community_forum_topic_partition_key_format(community_forum_topic: CommunityForumTopic) -> str:
        return f'COMMUNITY_FORUM_TOPIC#{community_forum_topic.id}'
    
    @staticmethod
    def community_forum_topic_partition_key_format_from_id(id: str) -> str:
        return f'COMMUNITY_FORUM_TOPIC#{id}'
    
    @staticmethod
    def community_forum_topic_sort_key_format() -> str:
        return 'METADATA'

    @staticmethod
    def community_forum_topic_gsi_entity_get_all_pk(community_forum_topic: CommunityForumTopic) -> str:
        return f'INDEX#COMMUNITY_FORUM_TOPIC#{community_forum_topic.channel_id}'
    
    @staticmethod
    def community_forum_topic_gsi_entity_get_all_pk_from_id(channel_id: str) -> str:
        return f'INDEX#COMMUNITY_FORUM_TOPIC#{channel_id}'
    
    @staticmethod
    def community_forum_topic_gsi_entity_get_all_sk(community_forum_topic: CommunityForumTopic) -> str:
        return f'DATE#{community_forum_topic.created_at}'

    def create_forum_topic(self, community_forum_topic: CommunityForumTopic) -> CommunityForumTopic:
        item = community_forum_topic.to_dict()

        item['PK'] = self.community_forum_topic_partition_key_format(community_forum_topic)
        item['SK'] = self.community_forum_topic_sort_key_format()
        item[encode_idx_pk('GSI#ENTITY_GETALL#PK')] = self.community_forum_topic_gsi_entity_get_all_pk(community_forum_topic)
        item[encode_idx_pk('GSI#ENTITY_GETALL#SK')] = self.community_forum_topic_gsi_entity_get_all_sk(community_forum_topic)

        self.dynamo.put_item(item=item)

        return community_forum_topic

    def get_channel_forum_topics(self,
        channel_id: str,
        title: str = '',
        limit: int = 10, last_evaluated_key: dict | None = None, sort_order: str = 'desc') -> dict:
        filter_expressions = []
        
        if title != '':
            filter_expressions.append(Attr('title').contains(title))

        filter_expression= None

        if len(filter_expressions) > 0:
            for f_exp in filter_expressions:
                if filter_expression is None:
                    filter_expression = f_exp
                else:
                    filter_expression &= f_exp

        response = self.dynamo.query(
            index_name='GetAllEntities',
            partition_key=self.community_forum_topic_gsi_entity_get_all_pk_from_id(channel_id),
            limit=limit,
            exclusive_start_key=last_evaluated_key if last_evaluated_key != '' else None,
            filter_expression=filter_expression,
            scan_index_forward=False if sort_order == 'desc' else True
        )

        count_response = self.dynamo.count(
            index_name='GetAllEntities',
            partition_key=self.community_forum_topic_gsi_entity_get_all_pk_from_id(channel_id),
            filter_expression=filter_expression,
        )
        
        return {
            'community_forum_topics': [ CommunityForumTopic.from_dict_static(item) for item in response['items'] ],
            'last_evaluated_key': response.get('last_evaluated_key'),
            'total': count_response['count']
        }
    
    def get_one_forum_topic(self, id: str) -> CommunityForumTopic | None:
        data = self.dynamo.get_item(
            partition_key=self.community_forum_topic_partition_key_format_from_id(id),
            sort_key=self.community_forum_topic_sort_key_format()
        )

        return CommunityForumTopic.from_dict_static(data['Item']) if 'Item' in data else None
    
    def delete_forum_topic(self, id: str) -> int:
        resp = self.dynamo.delete_item(
            partition_key=self.community_forum_topic_partition_key_format_from_id(id),
            sort_key=self.community_forum_topic_sort_key_format()
        )

        return resp['ResponseMetadata']['HTTPStatusCode']
    
    ### SESSION ###
    @staticmethod
    def community_session_partition_key_format(community_session: CommunitySession) -> str:
        return f'COMMUNITY_SESSION#{community_session.connection_id}'
    
    @staticmethod
    def community_session_partition_key_format_from_id(connection_id: str) -> str:
        return f'COMMUNITY_SESSION#{connection_id}'
    
    @staticmethod
    def community_session_sort_key_format() -> str:
        return 'METADATA'

    @staticmethod
    def community_session_gsi_entity_get_all_pk(community_session: CommunitySession) -> str:
        return f'INDEX#COMMUNITY_SESSION#{community_session.user_role.value}'
    
    @staticmethod
    def community_session_gsi_entity_get_all_pk_from_role(user_role: ROLE) -> str:
        return f'INDEX#COMMUNITY_SESSION#{user_role.value}'
    
    @staticmethod
    def community_session_gsi_entity_get_all_sk(community_session: CommunitySession) -> str:
        return f'DATE#{community_session.created_at}'
    
    @staticmethod
    def community_session_gsi_entity_get_by_id_pk(community_session: CommunitySession) -> str:
        return f'INDEX#COMMUNITY_SESSION#{community_session.user_id}'
    
    @staticmethod
    def community_session_gsi_entity_get_by_id_pk_from_id(user_id: str) -> str:
        return f'INDEX#COMMUNITY_SESSION#{user_id}'

    @staticmethod
    def community_session_gsi_entity_get_by_id_sk(community_session: CommunitySession) -> str:
        return f'DATE#{community_session.created_at}'

    def create_session(self, community_session: CommunitySession) -> CommunitySession:
        item = community_session.to_dict()

        item['PK'] = self.community_session_partition_key_format(community_session)
        item['SK'] = self.community_session_sort_key_format()
        item[encode_idx_pk('GSI#ENTITY_GETALL#PK')] = self.community_session_gsi_entity_get_all_pk(community_session)
        item[encode_idx_pk('GSI#ENTITY_GETALL#SK')] = self.community_session_gsi_entity_get_all_sk(community_session)
        item[encode_idx_pk('GSI#ENTITY_GET_BY_ID#PK')] = self.community_session_gsi_entity_get_by_id_pk(community_session)
        item[encode_idx_pk('GSI#ENTITY_GET_BY_ID#SK')] = self.community_session_gsi_entity_get_by_id_sk(community_session)

        self.dynamo.put_item(item=item)

        return community_session
    
    def get_one_session(self, connection_id: str) -> CommunitySession | None:
        data = self.dynamo.get_item(
            partition_key=self.community_session_partition_key_format_from_id(connection_id),
            sort_key=self.community_session_sort_key_format()
        )

        return CommunitySession.from_dict_static(data['Item']) if 'Item' in data else None
    
    def get_user_session(self, user_id: str) -> CommunitySession | None:
        data = self.dynamo.query(
            index_name='GetEntityById',
            partition_key=self.community_session_gsi_entity_get_by_id_pk_from_id(user_id)
        )
        
        items = data['items']

        return CommunitySession.from_dict_static(items[0]) if len(items) > 0 else None
    
    def get_sessions_by_role(self, user_role: ROLE) -> list[CommunitySession]:
        response = self.dynamo.query(
            index_name='GetAllEntities',
            partition_key=self.community_session_gsi_entity_get_all_pk_from_role(user_role)
        )

        return [ CommunitySession.from_dict_static(item) for item in response['items'] ]
    
    def update_session(self, community_session: CommunitySession) -> CommunitySession:
        item = community_session.to_dict()

        item['PK'] = self.community_session_partition_key_format(community_session)
        item['SK'] = self.community_session_sort_key_format()
        item[encode_idx_pk('GSI#ENTITY_GETALL#PK')] = self.community_session_gsi_entity_get_all_pk(community_session)
        item[encode_idx_pk('GSI#ENTITY_GETALL#SK')] = self.community_session_gsi_entity_get_all_sk(community_session)
        item[encode_idx_pk('GSI#ENTITY_GET_BY_ID#PK')] = self.community_session_gsi_entity_get_by_id_pk(community_session)
        item[encode_idx_pk('GSI#ENTITY_GET_BY_ID#SK')] = self.community_session_gsi_entity_get_by_id_sk(community_session)

        self.dynamo.put_item(item=item)

        return community_session
    
    def delete_session(self, connection_id: str) -> int:
        resp = self.dynamo.delete_item(
            partition_key=self.community_session_partition_key_format_from_id(connection_id),
            sort_key=self.community_session_sort_key_format()
        )

        return resp['ResponseMetadata']['HTTPStatusCode']