from populate.common import load_app_env

load_app_env()

from src.shared.infra.repositories.repository import Repository

from src.shared.coinmarketcap.api import CMCApi

def populate_home_coins():
    repository = Repository(home_coins_repo=True)

    cmc_api = CMCApi()

    home_coins = cmc_api.get_home_coins()

    repository.home_coins_repo.update(home_coins)
    
    print('Populated home coins')