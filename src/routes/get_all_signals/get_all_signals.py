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
from src.shared.domain.enums.trade_strat import TRADE_STRAT
from src.shared.domain.entities.signal import Signal

from src.shared.utils.entity import is_valid_getall_object, \
    is_valid_entity_string_list
from src.shared.utils.pagination import encode_cursor_get_all, decode_cursor

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
            if 'requester_user' not in request.data:
                raise MissingParameters('requester_user')
            
            requester_user = AuthAuthorizerDTO.from_api_gateway(request.data.get('requester_user'))

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
        self.repository = Repository(signal_repo=True)

    def execute(self, requester_user: AuthAuthorizerDTO, request_params: dict) -> dict:
        if not is_valid_getall_object(request_params):
            return { 'error': 'Filtro de consulta inválido' }
        
        title = ''

        if Signal.data_contains_valid_title(request_params):
            title = request_params['title'].strip()

        base_asset = ''

        if Signal.data_contains_valid_base_asset(request_params):
            base_asset = Signal.norm_asset(request_params['base_asset'])

        exchanges = []

        if is_valid_entity_string_list(request_params, 'exchanges', min_length=1, max_length=EXCHANGE.length()):
            for exchange in request_params['exchanges']:
                if Signal.data_contains_valid_exchange({ 'exchange': exchange }):
                    exchanges.append(EXCHANGE[exchange])

        markets = []

        if is_valid_entity_string_list(request_params, 'markets', min_length=1, max_length=MARKET.length()):
            for market in request_params['markets']:
                if Signal.data_contains_valid_market({ 'market': market }):
                    markets.append(MARKET[market])

        trade_sides = []

        if is_valid_entity_string_list(request_params, 'trade_sides', min_length=1, max_length=TRADE_SIDE.length()):
            for trade_side in request_params['trade_sides']:
                if Signal.data_contains_valid_trade_side({ 'trade_side': trade_side }):
                    trade_sides.append(TRADE_SIDE[trade_side])

        signal_status = []

        if is_valid_entity_string_list(request_params, 'signal_status', min_length=1, max_length=SIGNAL_STATUS.length()):
            for status in request_params['signal_status']:
                if Signal.data_contains_valid_status({ 'status': status }):
                    signal_status.append(SIGNAL_STATUS[status])

        trade_strats = []

        if is_valid_entity_string_list(request_params, 'trade_strats', min_length=1, max_length=TRADE_STRAT.length()):
            for trade_strat in request_params['trade_strats']:
                if Signal.data_contains_valid_trade_strat({ 'trade_strat': trade_strat }):
                    trade_strats.append(TRADE_STRAT[trade_strat])

        vip_level = None

        if Signal.data_contains_valid_vip_level(request_params):
            vip_level = VIP_LEVEL(request_params['vip_level'])

        if requester_user.role not in VIP_USER_ROLES:
            vip_level = VIP_LEVEL.FREE

        db_data = self.repository.signal_repo.get_all(
            title=title,
            base_asset=base_asset,
            exchanges=exchanges,
            markets=markets,
            trade_sides=trade_sides,
            signal_status=signal_status,
            trade_strats=trade_strats,
            vip_level=vip_level,
            limit=request_params['limit'],
            last_evaluated_key=decode_cursor(request_params['next_cursor']),
            sort_order=request_params['sort_order']
        )
        
        return encode_cursor_get_all(
            db_data=db_data,
            item_key='signals',
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