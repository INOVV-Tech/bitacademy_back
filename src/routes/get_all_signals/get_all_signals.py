from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.helpers.external_interfaces.http_codes import OK, InternalServerError, BadRequest
from src.shared.helpers.errors.errors import MissingParameters, ForbiddenAction

from src.shared.infra.repositories.repository import Repository
from src.shared.infra.repositories.dtos.auth_authorizer_dto import AuthAuthorizerDTO

from src.shared.domain.enums.role import ROLE
from src.shared.domain.enums.exchange import EXCHANGE
from src.shared.domain.enums.market import MARKET
from src.shared.domain.enums.trade_side import TRADE_SIDE
from src.shared.domain.enums.signal_status import SIGNAL_STATUS
from src.shared.domain.enums.vip_level import VIP_LEVEL
from src.shared.domain.entities.signal import Signal

from src.shared.utils.entity import is_valid_getall_object, \
    is_valid_entity_string_list

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
        self.repository = Repository(signal_repo=True)

    def execute(self, request_data: dict) -> dict:
        if not is_valid_getall_object(request_data):
            return { 'error': 'Filtro de consulta inválido' }

        base_asset = ''

        if Signal.data_contains_valid_base_asset(request_data):
            base_asset = Signal.norm_asset(request_data['base_asset'])

        exchanges = []

        if is_valid_entity_string_list(request_data, 'exchanges', min_length=1, max_length=EXCHANGE.length()):
            for exchange in request_data['exchanges']:
                if Signal.data_contains_valid_exchange({ 'exchange': exchange }):
                    exchanges.append(EXCHANGE[exchange])

        markets = []

        if is_valid_entity_string_list(request_data, 'markets', min_length=1, max_length=MARKET.length()):
            for market in request_data['markets']:
                if Signal.data_contains_valid_market({ 'market': market }):
                    markets.append(MARKET[market])

        trade_sides = []

        if is_valid_entity_string_list(request_data, 'trade_sides', min_length=1, max_length=TRADE_SIDE.length()):
            for trade_side in request_data['trade_sides']:
                if Signal.data_contains_valid_trade_side({ 'trade_side': trade_side }):
                    trade_sides.append(TRADE_SIDE[trade_side])

        signal_status = []

        if is_valid_entity_string_list(request_data, 'signal_status', min_length=1, max_length=SIGNAL_STATUS.length()):
            for status in request_data['signal_status']:
                if Signal.data_contains_valid_status({ 'status': status }):
                    signal_status.append(SIGNAL_STATUS[status])

        vip_level = None

        if Signal.data_contains_valid_vip_level(request_data):
            vip_level = VIP_LEVEL(request_data['vip_level'])

        db_data = self.repository.signal_repo.get_all(
            base_asset=base_asset,
            exchanges=exchanges,
            markets=markets,
            trade_sides=trade_sides,
            signal_status=signal_status,
            vip_level=vip_level,
            limit=request_data['limit'],
            last_evaluated_key=request_data['last_evaluated_key'],
            sort_order=request_data['sort_order']
        )

        db_data['signals'] = [ x.to_public_dict() for x in db_data['signals'] ]

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