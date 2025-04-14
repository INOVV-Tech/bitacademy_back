from helpers.errors.errors import MissingParameters
from helpers.external_interfaces.external_interface import IRequest, IResponse
from helpers.external_interfaces.http_codes import OK, BadRequest, InternalServerError
from helpers.external_interfaces.http_lambda_requests import CloudFunctionHttpRequest, CloudFunctionHttpResponse, LambdaHttpRequest, LambdaHttpResponse
from infra.repositories.repository import Repository

class Controller:
    @staticmethod
    def execute(request: IRequest) -> IResponse:
        usecase = None
        try:
            response = Usecase().execute()
            return OK(body=response)
        except MissingParameters as error:
            return BadRequest(error.message)
        except ValueError as error:
            return BadRequest(error.args[0])
        except Exception as error:
            return InternalServerError(str(error))
        finally:
            if usecase:
                usecase.repository.close_session()

class Usecase:
    repository: Repository

    def __init__(self):
        self.repository = Repository(user_repo=True)
        self.user_repo = self.repository.user_repo

    def execute(self) -> dict:
        users = self.user_repo.get_all_users()
        return [user.to_dict() for user in users]


def lambda_handler(event, context):
    http_request = LambdaHttpRequest(data=event)
    http_request.data['requester_user'] = event.get('requestContext', {}).get('authorizer', {}).get('claims', None)
    response = Controller.execute(http_request)
    http_response = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
    
    return http_response.toDict()