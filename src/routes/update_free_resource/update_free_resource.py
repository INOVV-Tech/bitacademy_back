from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.helpers.external_interfaces.http_codes import OK, InternalServerError, BadRequest
from src.shared.helpers.errors.errors import MissingParameters, ForbiddenAction

from src.shared.infra.repositories.repository import Repository
from src.shared.infra.repositories.dtos.auth_authorizer_dto import AuthAuthorizerDTO

from src.shared.domain.enums.role import ROLE
from src.shared.domain.entities.free_resource import FreeResource

ALLOWED_USER_ROLES = [ ROLE.ADMIN ]

class Controller:
    @staticmethod
    def execute(request: IRequest) -> IResponse:
        try:
            requester_user = AuthAuthorizerDTO.from_api_gateway(request.data.get('requester_user'))

            if requester_user.role not in ALLOWED_USER_ROLES:
                raise ForbiddenAction('Acesso não autorizado')
            
            response = Usecase().execute(request.data)

            if 'error' in response:
                return BadRequest(response['error'])
            
            return OK(body=response)
        except MissingParameters as error:
            return BadRequest(error.message)
        except:
            return InternalServerError('Erro interno de servidor')

class Usecase:
    repository: Repository

    def __init__(self):
        self.repository = Repository(free_resource_repo=True)

    def execute(self, request_data: dict) -> dict:
        if 'free_resource' not in request_data \
            or not isinstance(request_data['free_resource'], dict):
            return { 'error': 'Campo "free_resource" não foi encontrado' }
        
        free_resource_update_data = request_data['free_resource']

        if not FreeResource.data_contains_valid_id(free_resource_update_data):
            return { 'error': 'Identificador de material inválido' }
        
        free_resource = self.repository.free_resource_repo.get_one(free_resource_update_data['id'])

        if free_resource is None:
            return { 'error': 'Material não foi encontrado' }
        
        updated_fields = free_resource.update_from_dict(free_resource_update_data)

        if 'cover_img' in updated_fields:
            s3_datasource = self.repository.get_s3_datasource()

            upload_resp = free_resource.cover_img.store_in_s3(s3_datasource)

            if 'error' in upload_resp:
                return upload_resp

        self.repository.free_resource_repo.update(free_resource)

        return {
            'free_resource': free_resource.to_public_dict()
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