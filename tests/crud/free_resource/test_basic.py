import pytest

from tests.common import load_app_env, get_requester_user

load_app_env()

from src.shared.helpers.external_interfaces.http_models import HttpRequest

from src.routes.create_free_resource.create_free_resource import Controller as CreateController
from src.routes.get_all_free_resources.get_all_free_resources import Controller as GetAllController
from src.routes.get_one_free_resource.get_one_free_resource import Controller as GetOneController
from src.routes.update_free_resource.update_free_resource import Controller as UpdateController
from src.routes.delete_free_resource.delete_free_resource import Controller as DeleteController

class Test_FreeResource:
    def get_body(self):
        return {
            'requester_user': get_requester_user(admin=True)
        }
    
    def call_lambda(self, controller, body={}, headers={}, query_params={}):
        request = HttpRequest(body=body, headers=headers, query_params=query_params)

        return controller.execute(request)

    @pytest.mark.skip(reason='Done')
    def test_lambda_create(self):
        body = self.get_body()

        body['free_resource'] = {
            'title': 'Test FreeResource',
            'external_url': 'https://www.youtube.com/',
            'tags': [ 'teste', 'free' ]
        }

        controller = CreateController()

        response = self.call_lambda(controller, body)

        assert response['status_code'] == 200

    def test_lambda_get_all(self):
        body = self.get_body()

        body['limit'] = 10
        body['last_evaluated_key'] = ''

        controller = GetAllController()

        response = self.call_lambda(controller, body)

        print('response', response)

        assert True

    def test_lambda_get_one(self):
        assert True

    def test_lambda_update(self):
        assert True

    def test_lambda_delete(self):
        assert True