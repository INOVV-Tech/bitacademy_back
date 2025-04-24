from src.shared.environments import STAGE, Environments

from src.shared.infra.external.dynamo_datasource import DynamoDatasource
from src.shared.infra.external.s3_datasource import S3Datasource

### INTERFACES ###

from src.shared.domain.repositories.free_material_repository_interface import IFreeMaterialRepository
from src.shared.domain.repositories.course_repository_interface import ICourseRepository
from src.shared.domain.repositories.home_coins_repository_interface import IHomeCoinsRepository
from src.shared.domain.repositories.news_repository_interface import INewsRepository
from src.shared.domain.repositories.tool_repository_interface import IToolRepository

### REPOSITORIES ###

from src.shared.infra.repositories.database.free_material_repository import FreeMaterialRepositoryDynamo
from src.shared.infra.repositories.database.course_repository import CourseRepositoryDynamo
from src.shared.infra.repositories.database.home_coins_repository import HomeCoinsRepositoryDynamo
from src.shared.infra.repositories.database.news_repository import NewsRepositoryDynamo
from src.shared.infra.repositories.database.tool_repository import ToolRepositoryDynamo

class Repository:
    free_material_repo: IFreeMaterialRepository
    course_repo: ICourseRepository
    home_coins_repo: IHomeCoinsRepository
    news_repo: INewsRepository
    tool_repo: IToolRepository

    def __init__(
        self,
        free_material_repo: bool = False,
        course_repo: bool = False,
        home_coins_repo: bool= False,
        news_repo: bool = False,
        tool_repo: bool = False
    ):
        self.session = None

        if Environments.stage == STAGE.TEST:
            self._initialize_mock_repositories()
        else:
            self._initialize_database_repositories(
                free_material_repo,
                course_repo,
                home_coins_repo,
                news_repo,
                tool_repo
            )

    def get_s3_datasource(self) -> S3Datasource:
        return S3Datasource(
            bucket_name=Environments.bucket_name,
            region=Environments.region
        )
    
    def _initialize_mock_repositories(self):
        pass
        
    def _initialize_database_repositories(self, free_material_repo: bool, course_repo: bool, \
        home_coins_repo: bool, news_repo: bool, tool_repo: bool):
        dynamo = DynamoDatasource(
            dynamo_table_name=Environments.dynamo_table_name,
            region=Environments.region,
            endpoint_url='http://localhost:8000' if Environments.persist_local else None
        )

        if free_material_repo:
            self.free_material_repo = FreeMaterialRepositoryDynamo(dynamo)

        if course_repo:
            self.course_repo = CourseRepositoryDynamo(dynamo)

        if home_coins_repo:
            self.home_coins_repo = HomeCoinsRepositoryDynamo(dynamo)

        if news_repo:
            self.news_repo = NewsRepositoryDynamo(dynamo)

        if tool_repo:
            self.tool_repo = ToolRepositoryDynamo(dynamo)