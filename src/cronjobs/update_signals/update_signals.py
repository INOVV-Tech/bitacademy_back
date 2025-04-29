from src.shared.infra.repositories.repository import Repository

from src.shared.binance.api import BinanceApi

from src.shared.domain.enums.exchange import EXCHANGE
from src.shared.domain.enums.market import MARKET
from src.shared.domain.enums.trade_side import TRADE_SIDE
from src.shared.domain.enums.signal_status import SIGNAL_STATUS
from src.shared.domain.entities.signal import Signal

from src.shared.utils.time import now_timestamp

class Controller:
    @staticmethod
    def execute() -> dict:
        try:
            return Usecase().execute()
        except:
            return { 'error': 'Erro interno de servidor' }
        
class Usecase:
    repository: Repository
    binance_api: BinanceApi

    def __init__(self):
        self.repository = Repository(signal_repo=True)
        self.binance_api = BinanceApi()
    
    def execute(self) -> dict:
        # TODO: pagination
        db_data = self.repository.signal_repo.get_all(
            signal_status=[ SIGNAL_STATUS.ENTRY_WAIT, SIGNAL_STATUS.RUNNING ],
            limit=10000,
            last_evaluated_key='',
            sort_order='desc'
        )

        signals_grouped = self.group_signals(db_data['signals'])

        signals_updated = 0

        for exchange in EXCHANGE:
            signals_updated += self.update_binance_signals(signals_grouped[exchange.value])
        
        return {
            'signals_updated': signals_updated
        }
    
    def group_signals(self, signals: list[Signal]) -> dict:
        result = {}

        for exchange in EXCHANGE:
            exchange_signals = [ x for x in signals if x.exchange == exchange ]
            exchange_symbols = [ x.get_symbol() for x in exchange_signals ]

            result[exchange.value] = {
                'signals': self.group_by_market(exchange_signals),
                'symbols': exchange_symbols
            }

        return result

    def group_by_market(self, signals: list[Signal]) -> dict:
        result = {}

        for market in MARKET:
            market_signals = [ x for x in signals if x.market == market ]
            market_symbols = [ x.get_symbol() for x in market_signals ]

            result[market.value] = {
                'signals': self.group_by_trade_side(market_signals),
                'symbols': market_symbols
            }

        return result
    
    def group_by_trade_side(self, signals: list[Signal]) -> dict:
        result = {}

        for trade_side in TRADE_SIDE:
            result[trade_side.value] = [ x for x in signals if x.trade_side == trade_side ]

        return result
    
    def update_binance_signals(self, exchange_data: dict) -> int:
        if len(exchange_data['symbols']) == 0:
            return signals_updated

        signals_updated = 0
        
        exchange_signals = exchange_data['signals']

        for market in MARKET:
            if market == MARKET.SPOT:
                signals_updated += self.update_binance_spot_signals(exchange_signals[market.value])
            elif market == MARKET.FUTURES_USDT:
                signals_updated += self.update_binance_futures_usdt_signals(exchange_signals[market.value])
            elif market == MARKET.FUTURES_COIN:
                signals_updated += self.update_binance_futures_coins_signals(exchange_signals[market.value])

        return signals_updated
    
    def update_binance_spot_signals(self, market_data: dict) -> int:
        # 2. puxar preco dos simbolos de todos sinais (se possível)
        # 3. aplicar logica de update e salvar na dynamodb

        print(market_data)

        return 0
    
    def update_binance_futures_usdt_signals(self, market_data: dict) -> int:
        return 0
    
    def update_binance_futures_coins_signals(self, market_data: dict) -> int:
        return 0

def lambda_handler(event, context) -> dict:
    return Controller.execute()