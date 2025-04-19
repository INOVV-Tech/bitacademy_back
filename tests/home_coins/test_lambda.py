import pytest

from tests.common import load_app_env

load_app_env()

from src.shared.helpers.external_interfaces.http_models import HttpRequest

from src.routes.get_home_coins.get_home_coins import Controller as GetController

from src.cronjobs.update_home_coins.update_home_coins import Controller as UpdateController

class Test_HomeCoinsLambda:
    def get_body(self):
        return {}
    
    def call_lambda(self, controller, body={}, headers={}, query_params={}):
        request = HttpRequest(body=body, headers=headers, query_params=query_params)

        return controller.execute(request)

    @pytest.mark.skip(reason='Done')
    def test_get(self):
        body = self.get_body()

        controller = GetController()

        response = self.call_lambda(controller, body)

        assert response.status_code == 200

    @pytest.mark.skip(reason='Done')
    def test_cronjob(self):
        body = self.get_body()

        controller = UpdateController()

        response = self.call_lambda(controller, body)

        assert response.status_code == 200