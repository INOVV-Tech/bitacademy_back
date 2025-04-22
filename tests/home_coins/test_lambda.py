import json
import pytest

from tests.common import load_app_env, get_requester_user

load_app_env()

from src.shared.helpers.external_interfaces.http_models import HttpRequest

from src.routes.get_home_coins.get_home_coins import Controller as GetController

from src.cronjobs.update_home_coins.update_home_coins import Controller as UpdateController

class Test_HomeCoinsLambda:
    def print_data(self, data: dict) -> None:
        print(json.dumps(data, indent=4, ensure_ascii=False))
    
    def call_lambda(self, controller, body={}, headers={}, query_params={}):
        request = HttpRequest(body=body, headers=headers, query_params=query_params)

        return controller.execute(request)
    
    def call_cronjob(self, controller):
        return controller.execute()

    @pytest.mark.skip(reason='Done')
    def test_get(self):
        body = {
            'requester_user': get_requester_user(admin=True)
        }

        controller = GetController()

        response = self.call_lambda(controller, body)

        self.print_data(response.data)

        assert response.status_code == 200

    # @pytest.mark.skip(reason='Done')
    def test_cronjob(self):
        body = {}

        controller = UpdateController()

        response = self.call_cronjob(controller)

        self.print_data(response)

        assert 'error' not in response