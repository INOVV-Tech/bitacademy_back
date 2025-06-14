from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

from src.shared.infra.repositories.repository import Repository
from src.shared.infra.repositories.dtos.auth_authorizer_dto import AuthAuthorizerDTO

from src.shared.domain.enums.role import ROLE
from src.shared.domain.enums.community_type import COMMUNITY_TYPE
from src.shared.domain.entities.community import CommunityMessage

from src.shared.messaging.comm_sender import broadcast_msg_update

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
        if 'community_message' not in request_data \
            or not isinstance(request_data['community_message'], dict):
            return { 'error': 'Campo "community_message" não foi encontrado' }
        
        community_message_update_data = request_data['community_message']

        if not CommunityMessage.data_contains_valid_id(community_message_update_data):
            return { 'error': 'Identificador de mensagem de comunidade inválido' }
        
        community_message = self.repository.community_repo.get_one_message(community_message_update_data['id'])

        if community_message is None:
            return { 'error': 'Mensagem de comunidade não foi encontrada' }
        
        community_channel = self.repository.community_repo.get_one_channel(community_message.channel_id)

        if community_channel is None:
            return { 'error': 'Canal de comunidade não foi encontrado' }
        
        if not community_channel.permissions.is_edit_role(requester_user.role):
            return { 'error': 'Usuário não tem permissão para editar o canal de comunidade' }
        
        if not requester_user.role == ROLE.ADMIN and community_message.user_id != requester_user.user_id:
            return { 'error': 'Usuário não pode editar mensagens de terceiros em canais do tipo CHAT' }
        
        updated_fields = community_message.update_from_dict(community_message_update_data)

        if not updated_fields['any_updated']:
            return { 'community_message': None }

        self.repository.community_repo.update_message(community_message)

        read_roles = community_channel.permissions.get_all_read_roles()

        if len(read_roles) > 0:
            broadcast_msg_update(
                msg=community_message,
                read_roles=read_roles
            )

        return {
            'community_message': community_message.to_public_dict()
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