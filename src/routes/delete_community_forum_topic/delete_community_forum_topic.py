from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

from src.shared.infra.repositories.repository import Repository
from src.shared.infra.repositories.dtos.auth_authorizer_dto import AuthAuthorizerDTO

from src.shared.domain.enums.role import ROLE
from src.shared.domain.entities.community import CommunityForumTopic

from src.shared.utils.routing import controller_execute

ALLOWED_USER_ROLES = [
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
            fetch_vip_subscription=False
        )

class Usecase:
    repository: Repository

    def __init__(self):
        self.repository = Repository(community_repo=True)

    def execute(self, requester_user: AuthAuthorizerDTO, request_data: dict, request_params: dict) -> dict:
        if not CommunityForumTopic.data_contains_valid_id(request_data):
            return { 'error': 'Identificador de fórum de comunidade inválido' }
        
        community_forum_topic = self.repository.community_repo.get_one_forum_topic(request_data['id'])

        if community_forum_topic is None:
            return { 'error': 'Fórum de comunidade não foi encontrado' }
        
        if not self.repository.community_repo.role_can_edit_channel(community_forum_topic.channel_id, requester_user.role):
            return { 'error': 'O canal de comunidade não existe ou o usuário não tem permissão para editá-lo' }
        
        delete_result = self.repository.community_repo.delete_forum_topic(community_forum_topic.id)

        if delete_result != 200:
            return { 'error': f'Delete falhou com status "{delete_result}"' }

        self.repository.community_repo.delete_all_messages(
            channel_id=community_forum_topic.channel_id,
            forum_topic_id=community_forum_topic.id
        )

        return {}

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