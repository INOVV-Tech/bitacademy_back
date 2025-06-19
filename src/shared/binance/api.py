import json
import requests

from src.shared.domain.enums.market import MARKET

class BinanceApi:
    def __init__(self):
        pass

    def get_binance_spot_url(self, sufix: str) -> str:
        return f'https://api.binance.com/{sufix}'
    
    def get_binance_futures_usdt_url(self, sufix: str) -> str:
        return f'https://fapi.binance.com/{sufix}'
    
    def get_binance_futures_coin_url(self, sufix: str) -> str:
        return f'https://dapi.binance.com/{sufix}'
    
    def external_request(self,
        url: str,
        method: str = 'GET',
        data: dict | None = None,
        url_is_sufix=True,
        data_is_json=False,
        timeout_secs: int = 3,
        market: MARKET = MARKET.SPOT
    ) -> dict:
        if url_is_sufix:
            if market == MARKET.SPOT:
                url = self.get_binance_spot_url(url)
            elif market == MARKET.FUTURES_USDT:
                url = self.get_binance_futures_usdt_url(url)
            elif market == MARKET.FUTURES_COIN:
                url = self.get_binance_futures_coin_url(url)

        headers = {
            'accept': 'application/json'
        }

        if method == 'POST':
            if data_is_json:
                headers['content-type'] = 'application/json'
            else:
                headers['content-type'] = 'application/x-www-form-urlencoded'

        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=timeout_secs)
            else:
                data = data if data is not None else {}

                response = requests.post(url, data=data, headers=headers, timeout=timeout_secs)

            resp = json.loads(response.text)

            return resp
        except:
            return { 'error': 'Binance request failed' }
        
    def symbols_to_query_param(self, symbols: list[str] = []) -> str:
        if len(symbols) == 0:
            return ''
        
        symbols_str = ','.join([ f'"{x}"' for x in symbols ])

        return f'symbols=[{symbols_str}]'
        
    def get_spot_ticker_24hr(self, symbols: list[str] = [], timeout_secs: int = 3) -> dict:
        url = '/api/v3/ticker/24hr'

        symbols_qp = self.symbols_to_query_param(symbols)

        if symbols_qp != '':
            url += f'?{symbols_qp}'

        resp = self.external_request(
            url=url,
            method='GET',
            url_is_sufix=True,
            timeout_secs=timeout_secs,
            market=MARKET.SPOT
        )

        if isinstance(resp, list):
            resp = { 'tickers': resp }
        
        return resp
    
    def get_futures_usdt_ticker_24hr(self, symbol: str = '', timeout_secs: int = 3) -> dict:
        url = '/fapi/v1/ticker/24hr'

        if symbol != '':
            url += f'?symbol={symbol}'

        resp = self.external_request(
            url=url,
            method='GET',
            url_is_sufix=True,
            timeout_secs=timeout_secs,
            market=MARKET.FUTURES_USDT
        )

        if isinstance(resp, list):
            resp = { 'tickers': resp }
        elif isinstance(resp, dict) and 'error' not in resp:
            resp = { 'tickers': [ resp ] }
        
        return resp
    
    def get_futures_coin_ticker_24hr(self, symbol: str = '', timeout_secs: int = 3) -> dict:
        url = '/dapi/v1/ticker/24hr'

        if symbol != '':
            url += f'?symbol={symbol}'

        resp = self.external_request(
            url=url,
            method='GET',
            url_is_sufix=True,
            timeout_secs=timeout_secs,
            market=MARKET.FUTURES_COIN
        )

        if isinstance(resp, list):
            resp = { 'tickers': resp }
        
        return resp
    
    def get_spot_exchange_info(self, timeout_secs: int = 3) -> dict:
        url = '/api/v3/exchangeInfo'

        resp = self.external_request(
            url=url,
            method='GET',
            url_is_sufix=True,
            timeout_secs=timeout_secs,
            market=MARKET.SPOT
        )

        if isinstance(resp, dict):
            resp = { 'symbols': resp['symbols'] }

        return resp
    
    def get_futures_usdt_exchange_info(self, timeout_secs: int = 3) -> dict:
        url = '/fapi/v1/exchangeInfo'

        resp = self.external_request(
            url=url,
            method='GET',
            url_is_sufix=True,
            timeout_secs=timeout_secs,
            market=MARKET.FUTURES_USDT
        )

        if isinstance(resp, dict):
            resp = { 'symbols': resp['symbols'] }

        return resp

    def get_futures_coin_exchange_info(self, timeout_secs: int = 3) -> dict:
        url = '/dapi/v1/exchangeInfo'

        resp = self.external_request(
            url=url,
            method='GET',
            url_is_sufix=True,
            timeout_secs=timeout_secs,
            market=MARKET.FUTURES_COIN
        )

        if isinstance(resp, dict):
            resp = { 'symbols': resp['symbols'] }

        return resp
    
    def aggregate_symbols_as_coins(self, symbols: list[dict]) -> dict:
        coin_dict = {}

        spot_base_assets = [ x['baseAsset'] for x in symbols ]

        for spot_coin in spot_base_assets:
            if spot_coin in coin_dict:
                continue

            coin_dict[spot_coin] = True

        spot_quote_assets = [ x['quoteAsset'] for x in symbols ]

        for spot_coin in spot_quote_assets:
            if spot_coin in coin_dict:
                continue

            coin_dict[spot_coin] = True

        return coin_dict
    
    def get_all_spot_coins(self, timeout_secs: int = 3) -> dict:
        spot_exchange_resp = self.get_spot_exchange_info(timeout_secs=timeout_secs)

        spot_symbols = spot_exchange_resp.get('symbols', [])

        return self.aggregate_symbols_as_coins(spot_symbols)
    
    def get_all_futures_usdt_coins(self, timeout_secs: int = 3) -> dict:
        futures_exchange_resp = self.get_futures_usdt_exchange_info(timeout_secs=timeout_secs)

        futures_symbols = futures_exchange_resp.get('symbols', [])

        return self.aggregate_symbols_as_coins(futures_symbols)
    
    def get_all_futures_coin_coins(self, timeout_secs: int = 3) -> dict:
        futures_exchange_resp = self.get_futures_coin_exchange_info(timeout_secs=timeout_secs)

        futures_symbols = futures_exchange_resp.get('symbols', [])

        return self.aggregate_symbols_as_coins(futures_symbols)

