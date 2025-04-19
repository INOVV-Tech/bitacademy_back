import json
import pytest

from tests.common import load_app_env

load_app_env()

from src.shared.coinmarketcap.api import CMCApi

class Test_HomeCoinsApi:
    def print_data(self, data: dict) -> None:
        print(json.dumps(data, indent=4, ensure_ascii=False))

    @pytest.mark.skip(reason='Done')
    def test_cmc_api(self):
        cmc_api = CMCApi()

        home_coins = cmc_api.get_home_coins()

        print(home_coins.to_public_dict())

        assert home_coins is not None