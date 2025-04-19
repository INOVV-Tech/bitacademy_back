from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.helpers.external_interfaces.http_codes import OK, InternalServerError, BadRequest
from src.shared.helpers.errors.errors import MissingParameters

from src.shared.infra.repositories.repository import Repository

from src.shared.coinmarketcap.api import CMCApi

class Controller:
    @staticmethod
    def execute(request: IRequest) -> IResponse:
        try:
            headers = request.headers
            query_params = request.query_params

            response = Usecase().execute(query_params, headers)
            
            return OK(body=response)
        except MissingParameters as error:
            return BadRequest(error.message)
        except:
            return InternalServerError('Erro interno de servidor')
        
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

def lambda_handler(event, context) -> LambdaHttpResponse:
    http_request = LambdaHttpRequest(event)
    
    response = Controller.execute(http_request)

    return LambdaHttpResponse(
        status_code=response.status_code, 
        body=response.body, 
        headers=response.headers
    ).toDict()