from src.shared.environments import STAGE, Environments

from src.shared.infra.external.dynamo_datasource import DynamoDatasource

### INTERFACES ###

from src.shared.domain.repositories.free_resource_repository_interface import IFreeResourceRepository
from src.shared.domain.repositories.bit_class_repository_interface import IBitClassRepository

### REPOSITORIES ###

from src.shared.infra.repositories.database.free_resource_repository import FreeResourceRepositoryDynamo
from src.shared.infra.repositories.database.bit_class_repository import BitClassRepositoryDynamo

class Repository:
    free_resource_repo: IFreeResourceRepository
    bit_class_repo: IBitClassRepository

    def __init__(
        self,
        free_resource_repo: bool = False,
        bit_class_repo: bool = False
    ):
        self.session = None

        if Environments.stage == STAGE.TEST:
            self._initialize_mock_repositories()
        else:
            self._initialize_database_repositories(
                free_resource_repo,
                bit_class_repo
            )

    def _initialize_mock_repositories(self):
        pass
        
    def _initialize_database_repositories(self, free_resource_repo: bool, bit_class_repo: bool):
        dynamo = DynamoDatasource(
            dynamo_table_name=Environments.dynamo_table_name,
            region=Environments.region,
            endpoint_url='http://localhost:8000' if Environments.persist_local else None
        )

        if free_resource_repo:
            self.free_resource_repo = FreeResourceRepositoryDynamo(dynamo)

        if bit_class_repo:
            self.bit_class_repo = BitClassRepositoryDynamo(dynamo)