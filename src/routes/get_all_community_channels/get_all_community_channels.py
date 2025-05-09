from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

from src.shared.infra.repositories.repository import Repository
from src.shared.infra.repositories.dtos.auth_authorizer_dto import AuthAuthorizerDTO

from src.shared.domain.enums.role import ROLE
from src.shared.domain.enums.community_type import COMMUNITY_TYPE
from src.shared.domain.entities.community import CommunityChannel

from src.shared.utils.routing import controller_execute
from src.shared.utils.entity import is_valid_getall_object, is_valid_entity_string_list
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
        
        title = ''

        if CommunityChannel.data_contains_valid_title(request_params):
            title = request_params['title'].strip()

        comm_types = []

        if is_valid_entity_string_list(request_params, 'comm_types', min_length=1, max_length=COMMUNITY_TYPE.length()):
            for comm_type in request_params['comm_types']:
                if CommunityChannel.data_contains_valid_comm_type({ 'comm_type': comm_type }):
                    comm_types.append(COMMUNITY_TYPE[comm_type])

        db_data = self.repository.community_repo.get_all_channels(
            title=title,
            comm_types=comm_types,
            user_role=requester_user.role,
            limit=request_params['limit'],
            last_evaluated_key=decode_cursor(request_params['next_cursor']),
            sort_order=request_params['sort_order']
        )

        return encode_cursor_get_all(
            db_data=db_data,
            item_key='community_channels',
            limit=request_params['limit'],
            last_evaluated_key=db_data['last_evaluated_key'],
            public_args=[ requester_user.role ]
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