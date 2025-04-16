from src.shared.infra.external.dynamo_datasource import DynamoDatasource

from src.shared.domain.repositories.bit_class_repository_interface import IBitClassRepository

from src.shared.domain.entities.bit_class import BitClass

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
        item['GSI_ENTITY_GETALL'] = self.bit_class_gsi_primary_key()
        item['GSI_TEXT'] = bit_class.title

        self.dynamo.put_item(item=item)

        return bit_class

    def get_all(self, limit: int = 10, last_evaluated_key: str = '') -> dict:
        response = self.dynamo.query(
            index_name='GetAllEntities',
            partition_key=self.bit_class_gsi_primary_key(),
            limit=limit,
            exclusive_start_key=last_evaluated_key if last_evaluated_key != '' else None
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
        item['GSI_ENTITY_GETALL'] = self.bit_class_gsi_primary_key()
        item['GSI_TEXT'] = bit_class.title

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