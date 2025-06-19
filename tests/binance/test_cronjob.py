import json
import pytest

from tests.common import load_app_env

load_app_env()

from src.cronjobs.update_binance_coins_info.update_binance_coins_info import Controller as UpdateController

from src.shared.infra.repositories.repository import Repository

class Test_BinanceCronjob:
    def print_data(self, data: dict) -> None:
        print(json.dumps(data, indent=4, ensure_ascii=False))

    def call_cronjob(self, controller):
        return controller.execute()
    
    # @pytest.mark.skip(reason='Done')
    def test_cronjob_update(self):
        controller = UpdateController()

        response = self.call_cronjob(controller)

        self.print_data(response)

        assert 'error' not in response

    @pytest.mark.skip(reason='Done')
    def test_get_coins(self):
        repository = Repository(coin_info_repo=True)

        resp = repository.coin_info_repo.get_all(symbols=[ 'BTC', 'DOGE' ])

        print([ x.to_symbol_public_dict() for x in resp['coins'] ])
        
        assert True