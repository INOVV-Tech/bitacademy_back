from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.helpers.external_interfaces.http_codes import OK, InternalServerError, BadRequest
from src.shared.helpers.errors.errors import MissingParameters

from src.shared.infra.repositories.repository import Repository

class Controller:
    @staticmethod
    def execute(request: IRequest) -> IResponse:
        try:
            response = Usecase().execute()

            if 'error' in response:
                return BadRequest(response['error'])
            
            return OK(body=response)
        except MissingParameters as error:
            return BadRequest(error.message)
        except:
            return InternalServerError('Erro interno de servidor')

class Usecase:
    repository: Repository

    def __init__(self):
        self.repository = Repository(bit_class_repo=True)

    def execute(self) -> dict:
        home_coins = self.repository.home_coins_repo.get()

        return {
            'home_coins': home_coins.to_public_dict() if home_coins is not None else None
        }

def lambda_handler(event, context) -> LambdaHttpResponse:
    http_request = LambdaHttpRequest(event)
    
    response = Controller.execute(http_request)

    return LambdaHttpResponse(
        status_code=response.status_code, 
        body=response.body, 
        headers=response.headers
    ).toDict()