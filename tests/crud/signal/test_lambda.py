import json
import pytest

from tests.common import load_app_env, get_requester_user

load_app_env()

from src.shared.domain.enums.exchange import EXCHANGE
from src.shared.domain.enums.market import MARKET
from src.shared.domain.enums.trade_side import TRADE_SIDE
from src.shared.domain.enums.signal_status import SIGNAL_STATUS
from src.shared.domain.enums.vip_level import VIP_LEVEL
from src.shared.domain.enums.trade_strat import TRADE_STRAT

from src.shared.helpers.external_interfaces.http_models import HttpRequest

from src.routes.create_signal.create_signal import Controller as CreateController
from src.routes.get_all_signals.get_all_signals import Controller as GetAllController
from src.routes.get_one_signal.get_one_signal import Controller as GetOneController
from src.routes.update_signal.update_signal import Controller as UpdateController
from src.routes.delete_signal.delete_signal import Controller as DeleteController

class Test_SignalLambda:
    def print_data(self, data: dict) -> None:
        print(json.dumps(data, indent=4, ensure_ascii=False))

    def get_body(self):
        return {
            'requester_user': get_requester_user(admin=True)
        }
    
    def call_lambda(self, controller, body={}, headers={}, query_params={}):
        request = HttpRequest(body=body, headers=headers, query_params=query_params)

        return controller.execute(request)

    @pytest.mark.skip(reason='Done')
    def test_lambda_create(self):   
        body = self.get_body()

        signals = [
            {
                'title': 'Bitcoio',
                'base_asset': 'BTC',
                'quote_asset': 'USDT',
                'exchange': EXCHANGE.BINANCE.value,
                'market': MARKET.SPOT.value,
                'trade_side': TRADE_SIDE.LONG.value,
                'vip_level': VIP_LEVEL.VIP_1,
                'trade_strat': TRADE_STRAT.SCALPING.value,
                'estimated_pnl': '1.5',
                'stake_relative': '0.02',
                'margin_multiplier': '1',
            },
            {
                'title': 'Vitalikcoin',
                'base_asset': 'ETH',
                'quote_asset': 'USDT',
                'exchange': EXCHANGE.BINANCE.value,
                'market': MARKET.FUTURES_USDT.value,
                'trade_side': TRADE_SIDE.SHORT.value,
                'vip_level': VIP_LEVEL.FREE,
                'trade_strat': TRADE_STRAT.DAY_TRADING.value,
                'estimated_pnl': '1.5',
                'stake_relative': '0.09',
                'margin_multiplier': '7',
            }
        ]

        for signal in signals:
            body['signal'] = signal

            controller = CreateController()

            response = self.call_lambda(controller, body)

            self.print_data(response.data)

            assert response.status_code == 201

    @pytest.mark.skip(reason='Done')
    def test_lambda_get_all(self):
        body = self.get_body()

        # body['title'] = 'Bitcoio'
        body['limit'] = 10
        body['last_evaluated_key'] = ''
        body['sort_order'] = 'desc'

        controller = GetAllController()

        response = self.call_lambda(controller, body)

        self.print_data(response.data)

        assert response.status_code == 200

    @pytest.mark.skip(reason='Done')
    def test_lambda_get_all_by_base_asset(self):
        body = self.get_body()

        body['base_asset'] = 'BTC'
        body['limit'] = 10
        body['last_evaluated_key'] = ''
        body['sort_order'] = 'desc'

        controller = GetAllController()

        response = self.call_lambda(controller, body)

        self.print_data(response.data)

        assert response.status_code == 200

    @pytest.mark.skip(reason='Done')
    def test_lambda_get_all_by_exchanges(self):
        body = self.get_body()

        body['exchanges'] = [ EXCHANGE.BINANCE.value ]
        body['limit'] = 10
        body['last_evaluated_key'] = ''
        body['sort_order'] = 'desc'

        controller = GetAllController()

        response = self.call_lambda(controller, body)

        self.print_data(response.data)

        assert response.status_code == 200

    @pytest.mark.skip(reason='Done')
    def test_lambda_get_all_by_markets(self):
        body = self.get_body()

        body['markets'] = [ MARKET.SPOT.value, MARKET.FUTURES_USDT.value ]
        body['limit'] = 10
        body['last_evaluated_key'] = ''
        body['sort_order'] = 'desc'

        controller = GetAllController()

        response = self.call_lambda(controller, body)

        self.print_data(response.data)

        assert response.status_code == 200
    
    @pytest.mark.skip(reason='Done')
    def test_lambda_get_all_by_trade_sides(self):
        body = self.get_body()

        body['trade_sides'] = [ TRADE_SIDE.LONG.value ]
        body['limit'] = 10
        body['last_evaluated_key'] = ''
        body['sort_order'] = 'desc'

        controller = GetAllController()

        response = self.call_lambda(controller, body)

        self.print_data(response.data)

        assert response.status_code == 200

    @pytest.mark.skip(reason='Done')
    def test_lambda_get_all_by_status(self):
        body = self.get_body()

        body['signal_status'] = [ SIGNAL_STATUS.ENTRY_WAIT.value ]
        body['limit'] = 10
        body['last_evaluated_key'] = ''
        body['sort_order'] = 'desc'

        controller = GetAllController()

        response = self.call_lambda(controller, body)

        self.print_data(response.data)

        assert response.status_code == 200

    @pytest.mark.skip(reason='Done')
    def test_lambda_get_all_by_vip_level(self):
        body = self.get_body()

        body['vip_level'] = VIP_LEVEL.FREE.value
        body['limit'] = 10
        body['last_evaluated_key'] = ''
        body['sort_order'] = 'desc'

        controller = GetAllController()

        response = self.call_lambda(controller, body)

        self.print_data(response.data)

        assert response.status_code == 200

    @pytest.mark.skip(reason='Done')
    def test_lambda_get_all_by_trade_strat(self):
        body = self.get_body()

        body['trade_strats'] = [ TRADE_STRAT.DAY_TRADING.value ]
        body['limit'] = 10
        body['last_evaluated_key'] = ''
        body['sort_order'] = 'desc'

        controller = GetAllController()

        response = self.call_lambda(controller, body)

        self.print_data(response.data)

        assert response.status_code == 200

    @pytest.mark.skip(reason='Done')
    def test_lambda_get_one(self):
        body = self.get_body()

        body['id'] = 'f488e153-35dd-49d5-a278-272b40a4541e'

        controller = GetOneController()

        response = self.call_lambda(controller, body)

        self.print_data(response.data)

        assert response.status_code == 200

    @pytest.mark.skip(reason='Done')
    def test_lambda_update(self):
        body = self.get_body()

        body['signal'] = {
            'id': 'f488e153-35dd-49d5-a278-272b40a4541e',
            'base_asset': 'BTC',
            'quote_asset': 'USDT',
            'market': 'SPOT',
            'trade_side': 'LONG',
            'vip_level': VIP_LEVEL.VIP_1,
            'estimated_pnl': '2',
            'margin_multiplier': '10',
            'stake_relative': '0.05'
        }
        
        controller = UpdateController()

        response = self.call_lambda(controller, body)

        self.print_data(response.data)
        
        assert response.status_code == 200

    @pytest.mark.skip(reason='Done')
    def test_lambda_delete(self):
        body = self.get_body()

        body['id'] = '0a22993c-600b-4d57-afcb-49207e2286df'

        controller = DeleteController()

        response = self.call_lambda(controller, body)

        assert response.status_code == 200