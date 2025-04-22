from src.shared.infra.repositories.repository import Repository

from src.shared.coinmarketcap.api import CMCApi

class Controller:
    @staticmethod
    def execute() -> dict:
        try:
            return Usecase().execute()
        except:
            return { 'error': 'Erro interno de servidor' }
        
class Usecase:
    repository: Repository
    cmc_api: CMCApi

    def __init__(self):
        self.repository = Repository(home_coins_repo=True)
        self.cmc_api = CMCApi()

    def execute(self) -> dict:
        home_coins = self.cmc_api.get_home_coins()

        if home_coins is None:
            return {}

        self.repository.home_coins_repo.update(home_coins)

        return {}

def lambda_handler(event, context) -> dict:
    return Controller.execute()