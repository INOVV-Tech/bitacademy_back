from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

from src.shared.infra.repositories.repository import Repository
from src.shared.infra.repositories.dtos.auth_authorizer_dto import AuthAuthorizerDTO

from src.shared.domain.enums.role import ROLE
from src.shared.domain.enums.community_type import COMMUNITY_TYPE
from src.shared.domain.entities.community import CommunityMessage

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
        if not CommunityMessage.data_contains_valid_id(request_data):
            return { 'error': 'Identificador de mensagem de comunidade inválido' }
        
        community_message = self.repository.community_repo.get_one_message(request_data['id'])

        if community_message is None:
            return { 'error': 'Mensagem de comunidade não foi encontrada' }
        
        community_channel = self.repository.community_repo.get_one_channel(community_message.channel_id)

        if community_channel is None:
            return { 'error': 'Canal de comunidade não foi encontrado' }
        
        if not community_channel.permissions.is_edit_role(requester_user.role):
            return { 'error': 'Usuário não tem permissão para editar o canal de comunidade' }
        
        if community_channel.comm_type == COMMUNITY_TYPE.CHAT and community_message.user_id != requester_user.user_id:
            return { 'error': 'Usuário não pode editar mensagens de terceiros em canais do tipo CHAT' }
        
        delete_result = self.repository.community_repo.delete_message(community_message.id)

        if delete_result != 200:
            return { 'error': f'Delete falhou com status "{delete_result}"' }
    
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