from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

from src.shared.infra.repositories.repository import Repository
from src.shared.infra.repositories.dtos.auth_authorizer_dto import AuthAuthorizerDTO

from src.shared.domain.enums.role import ROLE

from src.shared.utils.routing import controller_execute
from src.shared.utils.entity import is_valid_getall_object, \
    is_valid_entity_uuid, is_valid_entity_timestamp
from src.shared.utils.pagination import encode_cursor_get_all, decode_cursor

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
        if not is_valid_getall_object(request_params):
            return { 'error': 'Filtro de consulta inválido' }
        
        if not is_valid_entity_uuid(request_params, 'channel_id', version=4):
            return { 'error': 'Identificador de canal de comunidade não foi encontrado' }
        
        if not self.repository.community_repo.role_can_read_channel(request_params['channel_id'], requester_user.role):
            return { 'error': 'O canal de comunidade não existe ou o usuário não tem permissão para lê-lo' }
        
        forum_topic_id = None

        if is_valid_entity_uuid(request_params, 'forum_topic_id', version=4):
            forum_topic_id = request_params['forum_topic_id']

        ini_timestamp = None
        end_timestamp = None

        if is_valid_entity_timestamp(request_params, 'ini_timestamp'):
            ini_timestamp = request_params['ini_timestamp']

        if is_valid_entity_timestamp(request_params, 'end_timestamp'):
            end_timestamp = request_params['end_timestamp']

        db_data = self.repository.community_repo.get_channel_messages(
            channel_id=request_params['channel_id'],
            forum_topic_id=forum_topic_id,
            ini_timestamp=ini_timestamp,
            end_timestamp=end_timestamp,
            limit=request_params['limit'],
            last_evaluated_key=decode_cursor(request_params['next_cursor']),
            sort_order=request_params['sort_order']
        )

        return encode_cursor_get_all(
            db_data=db_data,
            item_key='community_messages',
            limit=request_params['limit'],
            last_evaluated_key=db_data['last_evaluated_key'],
            public_args=[]
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