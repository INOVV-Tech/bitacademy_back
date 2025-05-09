from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

from src.shared.infra.repositories.repository import Repository
from src.shared.infra.repositories.dtos.auth_authorizer_dto import AuthAuthorizerDTO

from src.shared.domain.enums.role import ROLE
from src.shared.domain.entities.community import CommunityChannel

from src.shared.utils.routing import controller_execute

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
        self.repository = Repository(community_repo=True)

    def execute(self, requester_user: AuthAuthorizerDTO, request_data: dict, request_params: dict) -> dict:
        if CommunityChannel.data_contains_valid_id(request_params):
            return self.query_with_id(requester_user, request_params)

        if CommunityChannel.data_contains_valid_title(request_params):
            return self.query_with_title(requester_user, request_params)
        
        return { 'error': 'Nenhum identificador encontrado' }
    
    def query_with_id(self, requester_user: AuthAuthorizerDTO, request_params: dict) -> dict:
        community_channel = self.repository.community_repo.get_one_channel(request_params['id'])

        if community_channel is not None:
            if community_channel.permissions.is_forbidden(requester_user.role):
                return { 'community_channel': None }
        
        return {
            'community_channel': community_channel.to_public_dict(requester_user.role) if community_channel is not None else None
        }
    
    def query_with_title(self, requester_user: AuthAuthorizerDTO, request_params: dict) -> dict:
        community_channel = self.repository.community_repo.get_one_channel_by_title(request_params['title'])

        if community_channel is not None:
            if community_channel.permissions.is_forbidden(requester_user.role):
                return { 'community_channel': None }

        return {
            'community_channel': community_channel.to_public_dict(requester_user.role) if community_channel is not None else None
        }

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