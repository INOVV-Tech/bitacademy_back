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

        home_coins = cmc_api.get_home_coins()

        print(home_coins)

        assert True