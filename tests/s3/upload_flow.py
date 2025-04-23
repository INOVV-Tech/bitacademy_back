import os
import json
from flask import Flask, jsonify
from flask import request as flask_request
from flask_cors import CORS
from pyngrok import ngrok, conf

from src.shared.environments import Environments, STAGE

from tests.common import load_app_env

PORT = 3000
FLASK_APP = Flask(__name__)

CORS(FLASK_APP)

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
    except Exception as ex:
        print('json error', str(ex))
        pass

@FLASK_APP.route('/file_upload', methods=[ 'POST' ])
def file_upload():
    Environments.reload()

    debug_flask('file_upload')

    response = jsonify({ 'OK': 'ok' })

    return response

def init_file_api():
    load_app_env(stage=STAGE.DEV.value)

    public_url = ngrok.connect(PORT, domain=os.environ.get('NGROK_DOMAIN'))
    print(f'Ngrok listening on: {public_url}')

    FLASK_APP.run(port=PORT)
    print(f'Flask listening on port {PORT}')


