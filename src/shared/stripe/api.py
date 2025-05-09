import stripe

from src.shared.environments import Environments

class StripeApi:
    def __init__(self):
        self.pubkey = Environments.stripe_pubkey
        self.privkey = Environments.stripe_privkey
        self.webhook_privkey = Environments.stripe_webhook_privkey

        stripe.api_key = self.privkey

    def decode_webhook_event(self, request_headers: dict, raw_body: bytes) -> dict | None:
        sig_header = request_headers['Stripe-Signature']

        try:
            event = stripe.Webhook.construct_event(raw_body, sig_header, \
                self.webhook_privkey)

            if event['type'] != 'payment_intent.succeeded':
                return None
            
            payment_intent = event['data']['object']

            if isinstance(payment_intent, dict):
                return payment_intent
        except:
            pass

        return None
        
