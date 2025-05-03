from boto3.dynamodb.conditions import Attr

from src.shared.infra.external.dynamo_datasource import DynamoDatasource

from src.shared.domain.repositories.community_repository_interface import ICommunityRepository

from src.shared.domain.enums.role import ROLE
from src.shared.domain.enums.community_type import COMMUNITY_TYPE
from src.shared.domain.enums.community_permission import COMMUNITY_PERMISSION
from src.shared.domain.entities.community import CommunityChannel

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
            filter_expressions.append(Attr(f'permissions.{user_role.value}').ne(COMMUNITY_PERMISSION.FORBIDDEN))

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

    def delete_channel(self, id: str) -> CommunityChannel | None:
        data = self.dynamo.delete_item(
            partition_key=self.community_channel_partition_key_format_from_id(id),
            sort_key=self.community_channel_sort_key_format()
        )

        if 'Attributes' not in data:
            return None
        
        return CommunityChannel.from_dict_static(data['Attributes'])