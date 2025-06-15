import json
import boto3
import pytest

from botocore.config import Config

from tests.common import load_app_env, get_requester_user, \
    load_resource

load_app_env()

from src.shared.helpers.external_interfaces.http_models import HttpRequest

class Test_CommunityWebSocket:
    def print_data(self, data: dict) -> None:
        print(json.dumps(data, indent=4, ensure_ascii=False))

    def get_body(self):
        return {
            'requester_user': get_requester_user(admin=True)
        }

    ### CHANNEL ###
    # @pytest.mark.skip(reason='Done')
    def test_ws_list_connections(self):
        api_management = boto3.client(
            'apigatewaymanagementapi',
            endpoint_url='https://kprmboreq4.execute-api.sa-east-1.amazonaws.com/dev',
            config=Config(retries={ 'max_attempts': 3 })
        )

        conn = api_management.get_connection(ConnectionId='MKbvLdI4mjQCFzA=')
        pass