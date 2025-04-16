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
        return free_resource.created_at
    
    def __init__(self, dynamo: DynamoDatasource):
        self.dynamo = dynamo

    def create(self, free_resource: FreeResource) -> FreeResource:
        item = free_resource.to_dict()

        item['PK'] = self.free_resource_partition_key_format(free_resource)
        item['SK'] = self.free_resource_sort_key_format(free_resource)

        self.dynamo.put_item(item=item)

        return free_resource

    def get_all(self) -> list[FreeResource]:
        pass
    
    def get_one(self, title: str) -> FreeResource:
        pass

    def update(self, free_resource: FreeResource) -> FreeResource:
        pass

    def delete(self, free_resource: FreeResource) -> FreeResource:
        pass