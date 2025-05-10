import base64

from src.shared.environments import Environments

from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.helpers.external_interfaces.http_codes import OK, InternalServerError

from src.shared.infra.repositories.repository import Repository
from src.shared.infra.repositories.dtos.user_cognito_dto import UserCognitoDTO

from src.shared.stripe.api import StripeApi

from src.shared.domain.enums.role import ROLE
from src.shared.domain.entities.vip_subscription import VipSubscription

class Controller:
    @staticmethod
    def execute(request: IRequest, raw_body: bytes) -> IResponse:
        try:
            response = Usecase().execute(request.headers, raw_body)

            return OK(body=response)
        except:
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
        checkout_completed = self.stripe_api.decode_webhook_event(request_headers, raw_body)

        if checkout_completed is None:
            return {}
        
        status = checkout_completed['status']
        payment_status = checkout_completed['payment_status']

        if status != 'complete':
            return {}
        
        if payment_status != 'paid':
            return {}
        
        session_id = checkout_completed['id']
        customer_email = checkout_completed['customer_details']['email']
        customer_name = checkout_completed['customer_details']['name']

        products = self.stripe_api.get_session_products(session_id)

        found_vip_product = False

        for item in products['data']:
            product = item['price']['product']

            if product['name'] == Environments.vip_subscription_product_name:
                found_vip_product = True
                break
        
        if found_vip_product:
            self.handle_vip_subscription(customer_email, customer_name)

        return {}
    
    def update_user_role(self, user_dto: UserCognitoDTO, role: ROLE) -> None:
        if user_dto.role == role:
            return
        
        self.repository.auth_repo.update_user_role(user_dto.email, role)
    
    def handle_vip_subscription(self, user_email: str, user_name: str) -> None:
        user_dto = self.repository.auth_repo.get_user_by_email(user_email)

        if user_dto is None:
            user_dto = self.repository.auth_repo.create_user(user_email, user_name, ROLE.VIP)

            if user_dto is None:
                return
        
        if user_dto.role not in [ ROLE.GUEST, ROLE.VIP ]:
            # TODO: only guest/vip cant buy/renew vip subscription ?
            return

        vip_subscription = self.repository.vip_subscription_repo.get_one(user_dto.user_id)

        if vip_subscription is None:
            vip_subscription = VipSubscription.vip_one_month(user_dto.user_id)

            self.repository.vip_subscription_repo.create(vip_subscription)

            self.update_user_role(user_dto, ROLE.VIP)
            return
        
        vip_subscription.expire_at = VipSubscription.expire_one_month()

        self.repository.vip_subscription_repo.update(vip_subscription)

        self.update_user_role(user_dto, ROLE.VIP)
        
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