from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.helpers.external_interfaces.http_codes import OK, InternalServerError, BadRequest
from src.shared.helpers.errors.errors import MissingParameters, ForbiddenAction

from src.shared.infra.repositories.repository import Repository
from src.shared.infra.repositories.dtos.auth_authorizer_dto import AuthAuthorizerDTO

from src.shared.domain.enums.role import ROLE
from src.shared.domain.entities.community import CommunityForumTopic

from src.shared.utils.entity import is_valid_getall_object
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
        try:
            requester_user = request.data.get('requester_user')

            if requester_user is None:
                raise MissingParameters('requester_user')
            
            requester_user = AuthAuthorizerDTO.from_api_gateway(requester_user)

            if requester_user.role not in ALLOWED_USER_ROLES:
                raise ForbiddenAction('Acesso não autorizado')
            
            response = Usecase().execute(requester_user, request.query_params)

            if 'error' in response:
                return BadRequest(response['error'])
            
            return OK(body=response)
        except MissingParameters as error:
            return BadRequest(error.message)
        except ForbiddenAction as error:
            return BadRequest(error.message)
        except:
            return InternalServerError('Erro interno de servidor')

class Usecase:
    repository: Repository

    def __init__(self):
        self.repository = Repository(community_repo=True)

    def execute(self, requester_user: AuthAuthorizerDTO, request_params: dict) -> dict:
        if not is_valid_getall_object(request_params):
            return { 'error': 'Filtro de consulta inválido' }
        
        if not CommunityForumTopic.data_contains_valid_channel_id(request_params):
            return { 'error': 'Identificador de canal de comunidade inválido' }
        
        if not self.repository.community_repo.role_can_read_channel(request_params['channel_id'], requester_user.role):
            return { 'error': 'O canal de comunidade não existe ou o usuário não tem permissão para lê-lo' }
        
        title = ''

        if CommunityForumTopic.data_contains_valid_title(request_params):
            title = request_params['title'].strip()

        db_data = self.repository.community_repo.get_channel_forum_topics(
            channel_id=request_params['channel_id'],
            title=title,
            limit=request_params['limit'],
            last_evaluated_key=decode_cursor(request_params['next_cursor']),
            sort_order=request_params['sort_order']
        )

        return encode_cursor_get_all(
            db_data=db_data,
            item_key='community_forum_topics',
            limit=request_params['limit'],
            last_evaluated_key=db_data['last_evaluated_key']
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