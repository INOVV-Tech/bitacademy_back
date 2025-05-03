from src.shared.environments import STAGE, Environments

from src.shared.infra.external.dynamo_datasource import DynamoDatasource
from src.shared.infra.external.s3_datasource import S3Datasource

### INTERFACES ###

from src.shared.domain.repositories.free_material_repository_interface import IFreeMaterialRepository
from src.shared.domain.repositories.course_repository_interface import ICourseRepository
from src.shared.domain.repositories.home_coins_repository_interface import IHomeCoinsRepository
from src.shared.domain.repositories.news_repository_interface import INewsRepository
from src.shared.domain.repositories.tool_repository_interface import IToolRepository
from src.shared.domain.repositories.tag_repository_interface import ITagRepository
from src.shared.domain.repositories.signal_repository_interface import ISignalRepository
from src.shared.domain.repositories.community_repository_interface import ICommunityRepository

### REPOSITORIES ###

from src.shared.infra.repositories.database.free_material_repository import FreeMaterialRepositoryDynamo
from src.shared.infra.repositories.database.course_repository import CourseRepositoryDynamo
from src.shared.infra.repositories.database.home_coins_repository import HomeCoinsRepositoryDynamo
from src.shared.infra.repositories.database.news_repository import NewsRepositoryDynamo
from src.shared.infra.repositories.database.tool_repository import ToolRepositoryDynamo
from src.shared.infra.repositories.database.tag_repository import TagRepositoryDynamo
from src.shared.infra.repositories.database.signal_repository import SignalRepositoryDynamo
from src.shared.infra.repositories.database.community_repository import CommunityRepositoryDynamo

class Repository:
    free_material_repo: IFreeMaterialRepository
    course_repo: ICourseRepository
    home_coins_repo: IHomeCoinsRepository
    news_repo: INewsRepository
    tool_repo: IToolRepository
    tag_repo: ITagRepository
    signal_repo: ISignalRepository
    community_repo: ICommunityRepository

    def __init__(
        self,
        free_material_repo: bool = False,
        course_repo: bool = False,
        home_coins_repo: bool= False,
        news_repo: bool = False,
        tool_repo: bool = False,
        tag_repo: bool = False,
        signal_repo: bool = False,
        community_repo: bool = False
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
                tool_repo,
                tag_repo,
                signal_repo,
                community_repo
            )

    def get_s3_datasource(self) -> S3Datasource:
        return S3Datasource(
            bucket_name=Environments.bucket_name,
            region=Environments.region
        )
    
    def _initialize_mock_repositories(self):
        pass
        
    def _initialize_database_repositories(self, free_material_repo: bool, course_repo: bool, \
        home_coins_repo: bool, news_repo: bool, tool_repo: bool, tag_repo: bool, signal_repo: bool, \
        community_repo: bool):
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

        if tag_repo:
            self.tag_repo = TagRepositoryDynamo(dynamo)

        if signal_repo:
            self.signal_repo = SignalRepositoryDynamo(dynamo)

        if community_repo:
            self.community_repo = CommunityRepositoryDynamo(dynamo)