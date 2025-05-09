import os
import json
from flask import Flask
from flask import request as flask_request
from pyngrok import ngrok, conf

from src.shared.environments import Environments, STAGE

from tests.common import load_app_env

PORT = 3000
FLASK_APP = Flask(__name__)

conf.get_default().auth_token = os.environ.get('NGROK_AUTH_TOKEN', '')

def encode_data(data):
    return json.dumps(data, indent=4, ensure_ascii=False)

def debug_flask(title):
    print('')
    print('ROUTE: ', title)
    print('query params', encode_data(flask_request.args))
    print('form', encode_data(flask_request.form))

    try:
        print('json', flask_request.get_json())
    except:
        pass

@FLASK_APP.route('/vip_stripe_webohook', methods=[ 'POST' ])
def vip_stripe_webohook():
    Environments.reload()

    from src.shared.helpers.external_interfaces.http_models import HttpRequest
    from src.routes.vip_stripe_webhook.vip_stripe_webhook import Controller as WebhookController

    # debug_flask('vip_stripe_webohook')

    controller = WebhookController()

    request = HttpRequest(body={}, headers=flask_request.headers, query_params={})

    response = controller.execute(request, flask_request.get_data())

    return json.dumps(response.data)

def init_stripe_webhook():
    load_app_env(stage=STAGE.DEV.value)

    public_url = ngrok.connect(PORT, domain=os.environ.get('NGROK_DOMAIN'))
    print(f'Ngrok listening on: {public_url}')

    FLASK_APP.run(port=PORT)
    print(f'Flask listening on port {PORT}')


