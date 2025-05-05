from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.helpers.external_interfaces.http_codes import OK, InternalServerError, BadRequest
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
            requester_user = request.data.get('requester_user')

            if requester_user is None:
                raise MissingParameters('requester_user')
            
            requester_user = AuthAuthorizerDTO.from_api_gateway(requester_user)
            
            if requester_user.role not in ALLOWED_USER_ROLES:
                raise ForbiddenAction('Acesso não autorizado')
            
            response = Usecase().execute(request.data)

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

    def execute(self, request_data: dict) -> dict:
        if 'course' not in request_data \
            or not isinstance(request_data['course'], dict):
            return { 'error': 'Campo "course" não foi encontrado' }
        
        course_update_data = request_data['course']

        if not Course.data_contains_valid_id(course_update_data):
            return { 'error': 'Identificador de curso inválido' }
        
        course = self.repository.course_repo.get_one(course_update_data['id'])

        if course is None:
            return { 'error': 'Curso não foi encontrado' }
        
        updated_fields = course.update_from_dict(course_update_data)

        if not updated_fields['any_updated']:
            return { 'course': None }

        if 'cover_img' in updated_fields or 'card_img' in updated_fields:
            s3_datasource = self.repository.get_s3_datasource()

        if 'cover_img' in updated_fields:
            upload_resp = course.cover_img.store_in_s3(s3_datasource)

            if 'error' in upload_resp:
                return upload_resp

        if 'card_img' in updated_fields:
            upload_resp = course.card_img.store_in_s3(s3_datasource)

            if 'error' in upload_resp:
                return upload_resp

        self.repository.course_repo.update(course)

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