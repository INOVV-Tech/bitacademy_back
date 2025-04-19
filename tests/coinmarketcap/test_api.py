import json
import pytest

from tests.common import load_app_env, get_requester_user

load_app_env()

from src.shared.coinmarketcap.api import CMCApi

class Test_CMCApi:
    def print_data(self, data: dict) -> None:
        print(json.dumps(data, indent=4, ensure_ascii=False))

    # @pytest.mark.skip(reason='Done')
    def test_top_cripto(self):
        cmc_api = CMCApi()

        data = cmc_api.get_top_cripto()
        
        self.print_data(data)
        
        assert 'error' not in data