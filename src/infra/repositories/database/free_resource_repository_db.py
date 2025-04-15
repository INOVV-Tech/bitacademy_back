from domain.entities.free_resource import FreeResource
from domain.repositories.free_resource_interface import IFreeResourceRepository

from infra.external.postgre_datasource import PostgreDatasource

class FreeResourceRepositoryDb(IFreeResourceRepository):
    def __init__(self, datasource: PostgreDatasource):
        self.datasource = datasource

    def create(self, free_resource: FreeResource) -> FreeResource:
        item = free_resource.to_db()

        resp = self.datasource.add_item(item)

        return FreeResource.from_db(resp)
    
    def get_by_title(self, title: str) -> FreeResource:
        pass
    
    def get_all(self) -> list[FreeResource]:
        pass