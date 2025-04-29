import json
import pytest

from tests.common import load_app_env

load_app_env()

from src.shared.binance.api import BinanceApi

class Test_SignalCronjob:
    def print_data(self, data: dict) -> None:
        print(json.dumps(data, indent=4, ensure_ascii=False))

    @pytest.mark.skip(reason='Done')
    def test_binance_ticker_queries(self):
        binance_api = BinanceApi()

        spot_tickers = binance_api.get_spot_ticker_24hr(symbols=[ 'BTCUSDT' ])

        print('SPOT')

        self.print_data(spot_tickers)
        
        print('')
        print('FUTURES USDT')

        futures_usdt_tickers = binance_api.get_futures_usdt_ticker_24hr(symbol='BTCUSDT')

        self.print_data(futures_usdt_tickers)

        print('')
        print('FUTURES COIN')

        futures_coin_tickers = binance_api.get_futures_coin_ticker_24hr(symbol='AXSUSD_PERP')

        self.print_data(futures_coin_tickers)

        assert True