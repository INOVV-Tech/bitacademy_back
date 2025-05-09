from boto3.dynamodb.conditions import Attr

from src.shared.infra.external.dynamo_datasource import DynamoDatasource

from src.shared.domain.repositories.vip_subscription_repository_interface import IVipSubscriptionRepository

from src.shared.domain.entities.vip_subscription import VipSubscription

from src.shared.infra.external.key_formatters import encode_idx_pk

class VipSubscriptionRepositoryDynamo(IVipSubscriptionRepository):
    dynamo: DynamoDatasource

    @staticmethod
    def vip_subscription_partition_key_format(vip_subscription: VipSubscription) -> str:
        return f'VIP_SUBSCRIPTION#{vip_subscription.user_id}'
    
    @staticmethod
    def vip_subscription_partition_key_format_from_id(user_id: str) -> str:
        return f'VIP_SUBSCRIPTION#{user_id}'
    
    @staticmethod
    def vip_subscription_sort_key_format() -> str:
        return 'METADATA'
    
    @staticmethod
    def vip_subscription_gsi_entity_get_all_pk() -> str:
        return 'INDEX#VIP_SUBSCRIPTION'
    
    @staticmethod
    def vip_subscription_gsi_entity_get_all_sk(vip_subscription: VipSubscription) -> str:
        return f'DATE#{vip_subscription.created_at}'
    
    def __init__(self, dynamo: DynamoDatasource):
        self.dynamo = dynamo

    def create(self, vip_subscription: VipSubscription) -> VipSubscription:
        item = vip_subscription.to_dict()

        item['PK'] = self.vip_subscription_partition_key_format(vip_subscription)
        item['SK'] = self.vip_subscription_sort_key_format()
        item[encode_idx_pk('GSI#ENTITY_GETALL#PK')] = self.vip_subscription_gsi_entity_get_all_pk()
        item[encode_idx_pk('GSI#ENTITY_GETALL#SK')] = self.vip_subscription_gsi_entity_get_all_sk(vip_subscription)

        self.dynamo.put_item(item=item)

        return vip_subscription

    def get_all(self, user_ids: list[str] = [], limit: int = 10, \
        last_evaluated_key: dict | None = None, sort_order: str = 'desc') -> dict:
        filter_expressions = []

        if len(user_ids) > 0:
            user_filter_expression = None

            for user_id in user_ids:
                if user_filter_expression is None:
                    user_filter_expression = Attr('user_id').eq(user_id)
                else:
                    user_filter_expression |= Attr('user_id').eq(user_id)

            filter_expressions.append(user_filter_expression)

        filter_expression = None

        if len(filter_expressions) > 0:
            for f_exp in filter_expressions:
                if filter_expression is None:
                    filter_expression = f_exp
                else:
                    filter_expression &= f_exp

        response = self.dynamo.query(
            index_name='GetAllEntities',
            partition_key=self.vip_subscription_gsi_entity_get_all_pk(),
            limit=limit,
            exclusive_start_key=last_evaluated_key if last_evaluated_key != '' else None,
            filter_expression=filter_expression,
            scan_index_forward=False if sort_order == 'desc' else True
        )

        count_response = self.dynamo.count(
            index_name='GetAllEntities',
            partition_key=self.vip_subscription_gsi_entity_get_all_pk(),
            filter_expression=filter_expression
        )
        
        return {
            'vip_subscriptions': [ VipSubscription.from_dict_static(item) for item in response['items'] ],
            'last_evaluated_key': response.get('last_evaluated_key'),
            'total': count_response['count']
        }
    
    def get_one(self, user_id: str) -> VipSubscription | None:
        data = self.dynamo.get_item(
            partition_key=self.vip_subscription_partition_key_format_from_id(user_id),
            sort_key=self.vip_subscription_sort_key_format()
        )

        return VipSubscription.from_dict_static(data['Item']) if 'Item' in data else None

    def update(self, vip_subscription: VipSubscription) -> VipSubscription:
        item = vip_subscription.to_dict()

        item['PK'] = self.vip_subscription_partition_key_format(vip_subscription)
        item['SK'] = self.vip_subscription_sort_key_format()
        item[encode_idx_pk('GSI#ENTITY_GETALL#PK')] = self.vip_subscription_gsi_entity_get_all_pk()
        item[encode_idx_pk('GSI#ENTITY_GETALL#SK')] = self.vip_subscription_gsi_entity_get_all_sk(vip_subscription)

        self.dynamo.put_item(item=item)

        return vip_subscription

    def delete(self, user_id: str) -> int:
        resp = self.dynamo.delete_item(
            partition_key=self.vip_subscription_partition_key_format_from_id(user_id),
            sort_key=self.vip_subscription_sort_key_format()
        )

        return resp['ResponseMetadata']['HTTPStatusCode']