import json
import pytest

from tests.common import load_app_env, get_requester_user

load_app_env()

from src.shared.helpers.external_interfaces.http_models import HttpRequest

from src.routes.get_all_community_channels.get_all_community_channels import Controller as GetAllChannelsController

from src.routes.get_home_page_bundle.get_home_page_bundle import Controller as GetController

class Test_HomePageBundleLambda:
    def print_data(self, data: dict) -> None:
        print(json.dumps(data, indent=4, ensure_ascii=False))

    def get_body(self):
        return {
            'requester_user': get_requester_user(admin=True)
        }
    
    def call_lambda(self, controller, body={}, headers={}, query_params={}):
        request = HttpRequest(body=body, headers=headers, query_params=query_params)
        
        return controller.execute(request)

    @pytest.mark.skip(reason='Done')
    def test_lambda_get_home(self):
        body = self.get_body()
        
        controller = GetController()

        response = self.call_lambda(controller, body, query_params={})

        self.print_data(response.data)

        assert response.status_code == 200