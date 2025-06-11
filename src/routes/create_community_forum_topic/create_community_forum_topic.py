from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

from src.shared.infra.repositories.repository import Repository
from src.shared.infra.repositories.dtos.auth_authorizer_dto import AuthAuthorizerDTO

from src.shared.domain.enums.role import ROLE
from src.shared.domain.enums.community_type import COMMUNITY_TYPE
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
            fetch_vip_subscription=False,
            return_created=True
        )

class Usecase:
    repository: Repository

    def __init__(self):
        self.repository = Repository(community_repo=True)

    def execute(self, requester_user: AuthAuthorizerDTO, request_data: dict, request_params: dict) -> dict:
        if 'community_forum_topic' not in request_data \
            or not isinstance(request_data['community_forum_topic'], dict):
            return { 'error': 'Campo "community_forum_topic" não foi encontrado' }
        
        community_forum_topic_create_data = request_data['community_forum_topic']
        
        if not CommunityForumTopic.data_contains_valid_channel_id(community_forum_topic_create_data):
            return { 'error': 'Identificador de canal de comunidade inválido' }
        
        community_channel = self.repository.community_repo.get_one_channel(community_forum_topic_create_data['channel_id'])

        if community_channel is None:
            return { 'error': 'Canal de comunidade não foi encontrado' }
        
        if not community_channel.permissions.is_edit_role(requester_user.role):
            return { 'error': 'Usuário não tem permissão para editar o canal de comunidade' }
        
        if community_channel.comm_type != COMMUNITY_TYPE.FORUM:
            return { 'error': 'O canal de comunidade não é um fórum' }

        (error, community_forum_topic) = CommunityForumTopic.from_request_data(community_forum_topic_create_data,
            requester_user.user_id)

        if error != '':
            return { 'error': error }
        
        s3_datasource = self.repository.get_s3_datasource()

        upload_icon_resp = community_forum_topic.icon_img.store_in_s3(s3_datasource)

        if 'error' in upload_icon_resp:
            return upload_icon_resp
        
        self.repository.community_repo.create_forum_topic(community_forum_topic)

        return {
            'community_forum_topic': community_forum_topic.to_public_dict()
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