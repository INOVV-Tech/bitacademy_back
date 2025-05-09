from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

from src.shared.infra.repositories.repository import Repository
from src.shared.infra.repositories.dtos.auth_authorizer_dto import AuthAuthorizerDTO

from src.shared.domain.enums.role import ROLE
from src.shared.domain.enums.signal_status import SIGNAL_STATUS
from src.shared.domain.entities.signal import Signal

from src.shared.utils.routing import controller_execute

ALLOWED_USER_ROLES = [ ROLE.ADMIN ]

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
        self.repository = Repository(signal_repo=True)
    
    def execute(self, requester_user: AuthAuthorizerDTO, request_data: dict, request_params: dict) -> dict:
        if 'signal' not in request_data \
            or not isinstance(request_data['signal'], dict):
            return { 'error': 'Campo "signal" não foi encontrado' }
        
        signal_update_data = request_data['signal']

        if not Signal.data_contains_valid_id(signal_update_data):
            return { 'error': 'Identificador de sinal inválido' }
        
        signal = self.repository.signal_repo.get_one(signal_update_data['id'])

        if signal is None:
            return { 'error': 'Sinal não foi encontrado' }
        
        if signal.status != SIGNAL_STATUS.ENTRY_WAIT:
            return { 'error': f'Sinais com status "{signal.status.value}" não podem ser atualizados' }
        
        updated_fields = signal.update_from_dict(signal_update_data)

        if not updated_fields['any_updated']:
            return { 'signal': None }

        self.repository.signal_repo.update(signal)

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