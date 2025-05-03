from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.helpers.external_interfaces.http_codes import OK, InternalServerError, BadRequest
from src.shared.helpers.errors.errors import MissingParameters, ForbiddenAction

from src.shared.infra.repositories.repository import Repository
from src.shared.infra.repositories.dtos.auth_authorizer_dto import AuthAuthorizerDTO

from src.shared.domain.enums.role import ROLE
from src.shared.domain.enums.vip_level import VIP_LEVEL
from src.shared.domain.entities.course import Course

ALLOWED_USER_ROLES = [
    ROLE.GUEST,
    ROLE.AFFILIATE,
    ROLE.VIP,
    ROLE.TEACHER,
    ROLE.ADMIN
]

VIP_USER_ROLES = [
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
        self.repository = Repository(course_repo=True)

    def execute(self, requester_user: AuthAuthorizerDTO, request_params: dict) -> dict:
        if Course.data_contains_valid_id(request_params):
            return self.query_with_id(requester_user, request_params)

        if Course.data_contains_valid_title(request_params):
            return self.query_with_title(requester_user, request_params)
        
        return { 'error': 'Nenhum identificador encontrado' }
    
    def query_with_id(self, requester_user: AuthAuthorizerDTO, request_params: dict) -> dict:
        course = self.repository.course_repo.get_one(request_params['id'])

        if course is not None:
            if course.vip_level > VIP_LEVEL.FREE and requester_user.role not in VIP_USER_ROLES:
                return { 'course': None }

        return {
            'course': course.to_public_dict() if course is not None else None
        }
    
    def query_with_title(self, requester_user: AuthAuthorizerDTO, request_params: dict) -> dict:
        course = self.repository.course_repo.get_one_by_title(request_params['title'])

        if course is not None:
            if course.vip_level > VIP_LEVEL.FREE and requester_user.role not in VIP_USER_ROLES:
                return { 'course': None }

        return {
            'course': course.to_public_dict() if course is not None else None
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