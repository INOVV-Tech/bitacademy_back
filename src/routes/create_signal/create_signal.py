from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.helpers.external_interfaces.http_codes import Created, InternalServerError, BadRequest
from src.shared.helpers.errors.errors import MissingParameters, ForbiddenAction

from src.shared.infra.repositories.repository import Repository
from src.shared.infra.repositories.dtos.auth_authorizer_dto import AuthAuthorizerDTO

from src.shared.domain.enums.role import ROLE
from src.shared.domain.entities.signal import Signal

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
            
            response = Usecase().execute(requester_user, request.data)

            if 'error' in response:
                return BadRequest(response['error'])
            
            return Created(body=response)
        except MissingParameters as error:
            return BadRequest(error.message)
        except ForbiddenAction as error:
            return BadRequest(error.message)
        except:
            return InternalServerError('Erro interno de servidor')

class Usecase:
    repository: Repository

    def __init__(self):
        self.repository = Repository(signal_repo=True)

    def execute(self, requester_user: AuthAuthorizerDTO, request_data: dict) -> dict:
        if 'signal' not in request_data \
            or not isinstance(request_data['signal'], dict):
            return { 'error': 'Campo "signal" não foi encontrado' }

        (error, signal) = Signal.from_request_data(request_data['signal'], requester_user.user_id)

        if error != '':
            return { 'error': error }
        
        self.repository.signal_repo.create(signal)

        return {
            'signal': signal.to_public_dict()
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