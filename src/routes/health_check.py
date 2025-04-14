from src.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.helpers.external_interfaces.http_codes import OK
from src.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse


class Controller:
    @staticmethod
    def execute(request: IRequest) -> IResponse:
        return OK(body="Simple Templas is running!")

def lambda_handler(event, context):
    http_request = LambdaHttpRequest(data=event)
    response = Controller.execute(http_request)
    http_response = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
    
    return http_response.toDict()