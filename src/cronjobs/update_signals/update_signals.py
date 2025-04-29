from src.shared.infra.repositories.repository import Repository

from src.shared.binance.api import BinanceApi

from src.shared.domain.enums.exchange import EXCHANGE
from src.shared.domain.enums.market import MARKET
from src.shared.domain.enums.trade_side import TRADE_SIDE
from src.shared.domain.enums.signal_status import SIGNAL_STATUS
from src.shared.domain.entities.signal import Signal, PriceSnapshot

from src.shared.utils.decimal import Decimal
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
    
    def signals_to_symbols(self, signals: list[Signal]) -> list[str]:
        symbols = [ x.get_symbol() for x in signals ]

        _dict = {}

        result = []

        for symbol in symbols:
            if symbol in _dict:
                continue

            _dict[symbol] = True
            result.append(symbol)

        return result
    
    def group_signals(self, signals: list[Signal]) -> dict:
        result = {}

        for exchange in EXCHANGE:
            exchange_signals = [ x for x in signals if x.exchange == exchange ]
            exchange_symbols = self.signals_to_symbols(exchange_signals)

            result[exchange.value] = {
                'signals': self.group_by_market(exchange_signals),
                'symbols': exchange_symbols
            }

        return result

    def group_by_market(self, signals: list[Signal]) -> dict:
        result = {}

        for market in MARKET:
            market_signals = [ x for x in signals if x.market == market ]
            market_symbols = self.signals_to_symbols(market_signals)

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
            return 0

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
        market_symbols = market_data['symbols']

        if len(market_symbols) == 0:
            return 0

        spot_tickers_resp = self.binance_api.get_spot_ticker_24hr(symbols=market_symbols)

        if 'error' in spot_tickers_resp:
            return 0

        spot_ticker_by_symbol = {}
        
        for ticker_data in spot_tickers_resp['tickers']:
            spot_ticker_by_symbol[ticker_data['symbol']] = ticker_data

        long_signals = market_data['signals'][TRADE_SIDE.LONG.value]
        short_signals = market_data['signals'][TRADE_SIDE.SHORT.value]

        signals_updated = 0

        signals_updated += self.update_binance_long_signals(long_signals, spot_ticker_by_symbol)
        signals_updated += self.update_binance_short_signals(short_signals, spot_ticker_by_symbol)

        return signals_updated
    
    def update_binance_futures_usdt_signals(self, market_data: dict) -> int:
        return 0
    
    def update_binance_futures_coins_signals(self, market_data: dict) -> int:
        return 0
    
    def update_binance_long_signals(self, signals: list[Signal], tickers: dict) -> int:
        if len(signals) == 0:
            return 0
        
        signals_with_tickers = [ x for x in signals if x.get_symbol() in tickers ]

        signals_updated = 0

        for signal in signals_with_tickers:
            ticker_data = tickers[signal.get_symbol()]

            last_price = Decimal(ticker_data['lastPrice'])

            updated = False

            if signal.status == SIGNAL_STATUS.ENTRY_WAIT:
                if last_price >= signal.price_entry_min and last_price <= signal.price_entry_max:
                    signal.status_details.entry_snapshot = PriceSnapshot.from_exchange(last_price)
                    signal.status = SIGNAL_STATUS.RUNNING
                    
                    updated = True
            elif signal.status == SIGNAL_STATUS.RUNNING:
                if last_price <= signal.price_stop:
                    signal.status_details.stop_snapshot = PriceSnapshot.from_exchange(last_price)
                    signal.status = SIGNAL_STATUS.DONE

                    updated = True
                else:
                    if last_price >= signal.price_target_one:
                        signal.status_details.hit_target_one_snapshot = PriceSnapshot.from_exchange(last_price)
                        
                        updated = True

                    if last_price >= signal.price_target_two:
                        signal.status_details.hit_target_two_snapshot = PriceSnapshot.from_exchange(last_price)
                        
                        updated = True

                    if last_price >= signal.price_target_three:
                        signal.status_details.hit_target_three_snapshot = PriceSnapshot.from_exchange(last_price)
                        signal.status = SIGNAL_STATUS.DONE

                        updated = True
            
            if not updated:
                continue

            self.repository.signal_repo.update(signal)

            signals_updated += 1

        return signals_updated
    
    def update_binance_short_signals(self, signals: list[Signal], tickers: dict) -> int:
        if len(signals) == 0:
            return 0
        
        signals_with_tickers = [ x for x in signals if x.get_symbol() in tickers ]

        signals_updated = 0

        for signal in signals_with_tickers:
            ticker_data = tickers[signal.get_symbol()]

            last_price = ticker_data['lastPrice']

            pass

        return signals_updated

def lambda_handler(event, context) -> dict:
    return Controller.execute()