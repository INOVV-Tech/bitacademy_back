from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.helpers.external_interfaces.http_codes import OK, InternalServerError, BadRequest
from src.shared.helpers.errors.errors import MissingParameters, ForbiddenAction

from src.shared.infra.repositories.repository import Repository
from src.shared.infra.repositories.dtos.auth_authorizer_dto import AuthAuthorizerDTO

from src.shared.domain.enums.role import ROLE
from src.shared.domain.entities.free_material import FreeMaterial
from src.shared.utils.entity import is_valid_getall_object

ALLOWED_USER_ROLES = [ ROLE.ADMIN, ROLE.CLIENT ]

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
        self.repository = Repository(free_material_repo=True)

    def execute(self, request_data: dict) -> dict:
        if not is_valid_getall_object(request_data):
            return { 'error': 'Filtro de consulta inválido' }
        
        title = ''

        if FreeMaterial.data_contains_valid_title(request_data):
            title = request_data['title'].strip()
        
        tags = []
        
        if FreeMaterial.data_contains_valid_tags(request_data):
            tags = FreeMaterial.norm_tags(request_data['tags'])

        db_data = self.repository.free_material_repo.get_all(
            title=title,
            tags=tags,
            limit=request_data['limit'],
            last_evaluated_key=request_data['last_evaluated_key'],
            sort_order=request_data['sort_order']
        )

        db_data['free_materials'] = [ x.to_public_dict() for x in db_data['free_materials'] ]

        return db_data

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