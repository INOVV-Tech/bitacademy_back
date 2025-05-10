import stripe
from typing import Any

from src.shared.environments import Environments

class StripeApi:
    def __init__(self):
        self.privkey = Environments.stripe_privkey
        self.webhook_privkey = Environments.stripe_webhook_privkey

        stripe.api_key = self.privkey
    
    def decode_webhook_event(self, request_headers: dict, raw_body: bytes) -> Any | None:
        sig_header = request_headers['Stripe-Signature']

        try:
            event = stripe.Webhook.construct_event(raw_body, sig_header, \
                self.webhook_privkey)

            if event['type'] != 'checkout.session.completed':
                return None
            
            checkout_completed = event['data']['object']

            return checkout_completed
        except:
            pass

        return None
    
    def get_session_products(self, session_id: str) -> dict:
        return stripe.checkout.Session.list_line_items(session_id, expand=[ 'data.price.product' ])
