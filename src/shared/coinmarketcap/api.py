import json
import requests

from src.shared.environments import Environments

from src.shared.coinmarketcap.enums.sort_option import CMC_SORT_OPTION

class CMCApi:
    CMD_API_KEY: str = Environments.cmc_api_key 

    def __init__(self):
        pass

    def get_cmc_url(self, sufix: str) -> str:
        return f'https://pro-api.coinmarketcap.com/{sufix}'
    
    def external_request(self, url: str, method: str = 'GET', data: dict | None = None, url_is_sufix=True, \
        data_is_json=False, timeout_secs: int = 3) -> dict:
        if url_is_sufix:
            url = self.get_cmc_url(url)

        headers = {
            'accept': 'application/json',
            'X-CMC_PRO_API_KEY': self.CMD_API_KEY
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

            cmc_resp = json.loads(response.text)

            status = cmc_resp['status']

            if status['error_code'] != 0:
                return { 'error': status['error_message'] }

            return cmc_resp
        except:
            return { 'error': 'CMC request failed' }
        
    def get_top_cripto(self, limit: int = 10, sort: CMC_SORT_OPTION = CMC_SORT_OPTION.MARKET_CAP, timeout_secs: int = 3):
        url_sufix = 'v1/cryptocurrency/listings/latest?'
    
        url_sufix += f'limit={limit}'
        url_sufix += f'&sort={sort.value}'

        resp = self.external_request(
            url=url_sufix,
            method='GET',
            url_is_sufix=True,
            timeout_secs=timeout_secs
        )

        if 'error' in resp:
            return resp

        return resp['data']