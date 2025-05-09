import base64

from src.shared.infra.repositories.repository import Repository

from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.helpers.external_interfaces.http_codes import OK, InternalServerError

from src.shared.stripe.api import StripeApi

import traceback

class Controller:
    @staticmethod
    def execute(request: IRequest, raw_body: bytes) -> IResponse:
        try:
            response = Usecase().execute(request.headers, raw_body)

            return OK(body=response)
        except Exception as ex:
            print(str(ex))
            print(traceback.print_exc())
            return InternalServerError('Erro interno de servidor')
        
class Usecase:
    repository: Repository
    stripe_api: StripeApi

    def __init__(self):
        self.repository = Repository(
            auth_repo=True,
            vip_subscription_repo=True
        )

        self.stripe_api = StripeApi()
    
    def execute(self, request_headers: dict, raw_body: bytes) -> dict:
        payment_event = self.stripe_api.decode_webhook_event(request_headers, raw_body)

        print('PAYMENT EVENT', payment_event)

        return {}
        
def lambda_handler(event, context) -> LambdaHttpResponse:
    http_request = LambdaHttpRequest(event)

    raw_body = None

    if event.get('isBase64Encoded', False):
        raw_body = base64.b64decode(event['body'])
    else:
        raw_body = event['body'].encode('utf-8')
    
    response = Controller.execute(http_request, raw_body)

    return LambdaHttpResponse(
        status_code=response.status_code, 
        body=response.body, 
        headers=response.headers
    ).toDict()