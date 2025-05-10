from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

from src.shared.infra.repositories.repository import Repository
from src.shared.infra.repositories.dtos.auth_authorizer_dto import AuthAuthorizerDTO

from src.shared.domain.enums.role import ROLE

from src.shared.utils.routing import controller_execute
from src.shared.utils.pagination import encode_cursor_get_all

ALLOWED_USER_ROLES = [
    ROLE.GUEST,
    ROLE.AFFILIATE,
    ROLE.VIP,
    ROLE.TEACHER,
    ROLE.ADMIN
]

class Controller:
    @staticmethod
    def execute(request: IRequest) -> IResponse:
        return controller_execute(
            Usecase=Usecase,
            request=request,
            allowed_user_roles=ALLOWED_USER_ROLES,
            fetch_vip_subscription=True
        )

class Usecase:
    repository: Repository

    def __init__(self):
        self.repository = Repository(
            home_coins_repo=True,
            community_repo=True,
            news_repo=True
        )

    def execute(self, requester_user: AuthAuthorizerDTO, request_data: dict, request_params: dict) -> dict:
        return {
            'vip_subscription': requester_user.vip_subscription.to_public_dict(),
            'home_coins': self.get_home_coins(),
            'community_channels': self.get_community_channels(requester_user),
            'news_list': self.get_news(requester_user)
        }

    def get_home_coins(self) -> dict | None:
        home_coins = self.repository.home_coins_repo.get()

        return home_coins.to_public_dict() if home_coins is not None else None
    
    def get_community_channels(self, requester_user: AuthAuthorizerDTO) -> dict:
        db_data = self.repository.community_repo.get_all_channels(
            title='',
            comm_types=[],
            user_role=requester_user.role,
            limit=10,
            last_evaluated_key=None,
            sort_order='desc'
        )

        return encode_cursor_get_all(
            db_data=db_data,
            item_key='community_channels',
            limit=10,
            last_evaluated_key=None,
            public_args=[ requester_user.role ]
        )

    def get_news(self, requester_user: AuthAuthorizerDTO) -> dict:
        vip_level = requester_user.vip_subscription.restrict_access(None)

        db_data = self.repository.news_repo.get_all(
            title='',
            tags=[],
            vip_level=vip_level,
            limit=10,
            last_evaluated_key=None,
            sort_order='desc'
        )

        return encode_cursor_get_all(
            db_data=db_data,
            item_key='news_list',
            limit=10,
            last_evaluated_key=None
        )

def lambda_handler(event, context) -> LambdaHttpResponse:
    http_request = LambdaHttpRequest(event)

    http_request.data['requester_user'] = event.get('requestContext', {}) \
        .get('authorizer', {}) \
        .get('claims', None)
    
    response = Controller.execute(http_request)

    return LambdaHttpResponse(
        status_code=response.status_code, 
        body=response.body, 
        headers=response.headers
    ).toDict()