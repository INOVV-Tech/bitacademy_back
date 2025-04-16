from boto3.dynamodb.conditions import Attr

from src.shared.infra.external.dynamo_datasource import DynamoDatasource

from src.shared.domain.repositories.free_resource_repository_interface import IFreeResourceRepository
from src.shared.domain.entities.free_resource import FreeResource

class FreeResourceRepositoryDynamo(IFreeResourceRepository):
    dynamo: DynamoDatasource
    
    @staticmethod
    def free_resource_partition_key_format(free_resource: FreeResource) -> str:
        return f'FREE_RESOURCE#{free_resource.id}'
    
    @staticmethod
    def free_resource_partition_key_format_from_id(id: str) -> str:
        return f'FREE_RESOURCE#{id}'
    
    @staticmethod
    def free_resource_sort_key_format() -> str:
        return 'NONE'
    
    @staticmethod
    def free_resource_gsi_primary_key() -> str:
        return 'FREE_RESOURCE'
    
    def __init__(self, dynamo: DynamoDatasource):
        self.dynamo = dynamo

    def create(self, free_resource: FreeResource) -> FreeResource:
        item = free_resource.to_dict()

        item['PK'] = self.free_resource_partition_key_format(free_resource)
        item['SK'] = self.free_resource_sort_key_format()
        item['GSI_ENTITY_GETALL'] = self.free_resource_gsi_primary_key()
        item['GSI_TEXT'] = free_resource.title

        self.dynamo.put_item(item=item)

        return free_resource

    def get_all(self, tags: list[str] = [], limit: int = 10, last_evaluated_key: str = '') -> dict:
        filter_expression = None

        if len(tags) > 0:
            for tag in tags:
                if filter_expression is None:
                    filter_expression = Attr('tags').contains(tag)
                else:
                    filter_expression |= Attr('tags').contains(tag)

        response = self.dynamo.query(
            index_name='GetAllEntities',
            partition_key=self.free_resource_gsi_primary_key(),
            limit=limit,
            exclusive_start_key=last_evaluated_key if last_evaluated_key != '' else None,
            filter_expression=filter_expression
        )
        
        return {
            'free_resources': [ FreeResource.from_dict_static(item) for item in response['items'] ],
            'last_evaluated_key': response.get('last_evaluated_key')
        }
    
    def get_one(self, id: str) -> FreeResource | None:
        data = self.dynamo.get_item(
            partition_key=self.free_resource_partition_key_format_from_id(id),
            sort_key=self.free_resource_sort_key_format()
        )

        return FreeResource.from_dict_static(data['Item']) if 'Item' in data else None
    
    def get_one_by_title(self, title: str) -> FreeResource | None:
        data = self.dynamo.query(
            partition_key=title,
            index_name='GetEntityByText'
        )

        items = data['items']

        return FreeResource.from_dict_static(items[0]) if len(items) > 0 else None

    def update(self, free_resource: FreeResource) -> FreeResource:
        item = free_resource.to_dict()

        item['PK'] = self.free_resource_partition_key_format(free_resource)
        item['SK'] = self.free_resource_sort_key_format()
        item['GSI_ENTITY_GETALL'] = self.free_resource_gsi_primary_key()
        item['GSI_TEXT'] = free_resource.title

        self.dynamo.put_item(item=item)

        return free_resource

    def delete(self, id: str) -> FreeResource | None:
        data = self.dynamo.delete_item(
            partition_key=self.free_resource_partition_key_format_from_id(id),
            sort_key=self.free_resource_sort_key_format()
        )

        if 'Attributes' not in data:
            return None

        return FreeResource.from_dict_static(data['Attributes'])