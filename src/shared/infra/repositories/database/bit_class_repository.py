from boto3.dynamodb.conditions import Attr

from src.shared.infra.external.dynamo_datasource import DynamoDatasource

from src.shared.domain.repositories.bit_class_repository_interface import IBitClassRepository

from src.shared.domain.enums.vip_level import VIP_LEVEL
from src.shared.domain.entities.bit_class import BitClass

from src.shared.infra.external.key_formatters import encode_idx_pk

class BitClassRepositoryDynamo(IBitClassRepository):
    dynamo: DynamoDatasource
    
    @staticmethod
    def bit_class_partition_key_format(bit_class: BitClass) -> str:
        return f'BIT_CLASS#{bit_class.id}'
    
    @staticmethod
    def bit_class_partition_key_format_from_id(id: str) -> str:
        return f'BIT_CLASS#{id}'
    
    @staticmethod
    def bit_class_sort_key_format() -> str:
        return 'NONE'
    
    @staticmethod
    def bit_class_gsi_primary_key() -> str:
        return 'BIT_CLASS'
    
    def __init__(self, dynamo: DynamoDatasource):
        self.dynamo = dynamo

    def create(self, bit_class: BitClass) -> BitClass:
        item = bit_class.to_dict()

        item['PK'] = self.bit_class_partition_key_format(bit_class)
        item['SK'] = self.bit_class_sort_key_format()
        item[encode_idx_pk('GSI#ENTITY_GETALL')] = self.bit_class_gsi_primary_key()
        item[encode_idx_pk('GSI#TEXT')] = bit_class.title

        self.dynamo.put_item(item=item)

        return bit_class

    def get_all(self, tags: list[str] = [], vip_level: VIP_LEVEL | None = None, \
        limit: int = 10, last_evaluated_key: str = '') -> dict:
        tags_filter_expression = None

        if len(tags) > 0:
            for tag in tags:
                if tags_filter_expression is None:
                    tags_filter_expression = Attr('tags').contains(tag)
                else:
                    tags_filter_expression |= Attr('tags').contains(tag)

        vip_filter_expression = None

        if vip_level is not None:
            vip_filter_expression = Attr('vip_level').eq(vip_level.value)

        filter_expression = None

        if tags_filter_expression is not None:
            filter_expression = tags_filter_expression

        if vip_filter_expression is not None:
            if filter_expression is None:
                filter_expression = vip_filter_expression
            else:
                filter_expression &= vip_filter_expression

        response = self.dynamo.query(
            index_name='GetAllEntities',
            partition_key=self.bit_class_gsi_primary_key(),
            limit=limit,
            exclusive_start_key=last_evaluated_key if last_evaluated_key != '' else None,
            filter_expression=filter_expression
        )
        
        return {
            'bit_classes': [ BitClass.from_dict_static(item) for item in response['items'] ],
            'last_evaluated_key': response.get('last_evaluated_key')
        }
    
    def get_one(self, id: str) -> BitClass | None:
        data = self.dynamo.get_item(
            partition_key=self.bit_class_partition_key_format_from_id(id),
            sort_key=self.bit_class_sort_key_format()
        )

        return BitClass.from_dict_static(data['Item']) if 'Item' in data else None
    
    def get_one_by_title(self, title: str) -> BitClass | None:
        data = self.dynamo.query(
            partition_key=title,
            index_name='GetEntityByText'
        )

        items = data['items']

        return BitClass.from_dict_static(items[0]) if len(items) > 0 else None

    def update(self, bit_class: BitClass) -> BitClass:
        item = bit_class.to_dict()

        item['PK'] = self.bit_class_partition_key_format(bit_class)
        item['SK'] = self.bit_class_sort_key_format()
        item[encode_idx_pk('GSI#ENTITY_GETALL')] = self.bit_class_gsi_primary_key()
        item[encode_idx_pk('GSI#TEXT')] = bit_class.title

        self.dynamo.put_item(item=item)
        
        return bit_class

    def delete(self, id: str) -> BitClass | None:
        data = self.dynamo.delete_item(
            partition_key=self.bit_class_partition_key_format_from_id(id),
            sort_key=self.bit_class_sort_key_format()
        )

        if 'Attributes' not in data:
            return None

        return BitClass.from_dict_static(data['Attributes'])