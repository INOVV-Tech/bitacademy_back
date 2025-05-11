import stripe
from typing import Any

from src.shared.environments import Environments

class StripeApi:
    def __init__(self):
        self.privkey = Environments.stripe_privkey
        self.webhook_privkey = Environments.stripe_webhook_privkey

        stripe.api_key = self.privkey

    def get_sig_header(self, request_headers: dict) -> str | None:
        sig_header = request_headers.get('Stripe-Signature', None)

        if sig_header is None:
            sig_header = request_headers.get('STRIPE-SIGNATURE', None)

        if sig_header is None:
            sig_header = request_headers.get('STRIPE_SIGNATURE', None)
        
        return sig_header
    
    def decode_webhook_event(self, request_headers: dict, raw_body: bytes) -> Any | None:
        try:
            sig_header = self.get_sig_header(request_headers)

            if sig_header is None:
                return None

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
