from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.helpers.external_interfaces.http_codes import Created, InternalServerError, BadRequest
from src.shared.helpers.errors.errors import MissingParameters, ForbiddenAction

from src.shared.infra.repositories.repository import Repository
from src.shared.infra.repositories.dtos.auth_authorizer_dto import AuthAuthorizerDTO

from src.shared.domain.enums.role import ROLE
from src.shared.domain.entities.course import Course

ALLOWED_USER_ROLES = [ ROLE.ADMIN ]

class Controller:
    @staticmethod
    def execute(request: IRequest) -> IResponse:
        try:
            requester_user = AuthAuthorizerDTO.from_api_gateway(request.data.get('requester_user'))

            if requester_user.role not in ALLOWED_USER_ROLES:
                raise ForbiddenAction('Acesso não autorizado')
            
            response = Usecase().execute(requester_user, request.data)

            if 'error' in response:
                return BadRequest(response['error'])
            
            return Created(body=response)
        except MissingParameters as error:
            return BadRequest(error.message)
        except:
            return InternalServerError('Erro interno de servidor')

class Usecase:
    repository: Repository

    def __init__(self):
        self.repository = Repository(course_repo=True)

    def execute(self, requester_user: AuthAuthorizerDTO, request_data: dict) -> dict:
        if 'course' not in request_data \
            or not isinstance(request_data['course'], dict):
            return { 'error': 'Campo "course" não foi encontrado' }

        (error, course) = Course.from_request_data(request_data['course'], requester_user.user_id)

        if error != '':
            return { 'error': error }
        
        s3_datasource = self.repository.get_s3_datasource()

        upload_cover_resp = course.cover_img.store_in_s3(s3_datasource)

        if 'error' in upload_cover_resp:
            return upload_cover_resp
        
        upload_card_resp = course.card_img.store_in_s3(s3_datasource)

        if 'error' in upload_card_resp:
            return upload_card_resp
        
        self.repository.course_repo.create(course)

        return {
            'course': course.to_public_dict()
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