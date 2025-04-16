from boto3.dynamodb.conditions import Key

from src.shared.infra.external.dynamo_datasource import DynamoDatasource

from src.shared.domain.repositories.free_resource_repository_interface import IFreeResourceRepository
from src.shared.domain.entities.free_resource import FreeResource

class FreeResourceRepositoryDynamo(IFreeResourceRepository):
    dynamo: DynamoDatasource
    
    @staticmethod
    def free_resource_partition_key_format(free_resource: FreeResource) -> str:
        return f'FREE_RESOURCE#{free_resource.title}'
    
    @staticmethod
    def free_resource_sort_key_format(free_resource: FreeResource) -> str:
        return str(free_resource.created_at)
    
    @staticmethod
    def free_resource_gsi_primary_key() -> str:
        return 'FREE_RESOURCE'
    
    def __init__(self, dynamo: DynamoDatasource):
        self.dynamo = dynamo

    def create(self, free_resource: FreeResource) -> FreeResource:
        item = free_resource.to_dict()

        item['PK'] = self.free_resource_partition_key_format(free_resource)
        item['SK'] = self.free_resource_sort_key_format(free_resource)
        item['GSI_GETALL_ENTITIES'] = self.free_resource_gsi_primary_key()

        self.dynamo.put_item(item=item)

        return free_resource

    def get_all(self, limit: int = 10, last_evaluated_key: str = '') -> dict:
        response = self.dynamo.query(
            index_name='GetAllEntities',
            partition_key=self.free_resource_gsi_primary_key(),
            limit=limit,
            exclusive_start_key=last_evaluated_key if last_evaluated_key != '' else None
        )
        
        return {
            'free_resources': [ FreeResource.from_dict_static(item) for item in response['items'] ],
            'last_evaluated_key': response.get('last_evaluated_key')
        }
    
    def get_one(self, title: str) -> FreeResource:
        pass

    def update(self, free_resource: FreeResource) -> FreeResource:
        pass

    def delete(self, free_resource: FreeResource) -> FreeResource:
        pass