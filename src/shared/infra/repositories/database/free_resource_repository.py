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
        pass
    
    def get_by_title(self, title: str) -> FreeResource:
        pass
    
    def get_all(self) -> list[FreeResource]:
        pass