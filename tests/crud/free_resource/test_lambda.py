import pytest

from tests.common import load_app_env, get_requester_user

load_app_env()

from src.shared.helpers.external_interfaces.http_models import HttpRequest

from src.routes.create_free_resource.create_free_resource import Controller as CreateController
from src.routes.get_all_free_resources.get_all_free_resources import Controller as GetAllController
from src.routes.get_one_free_resource.get_one_free_resource import Controller as GetOneController
from src.routes.update_free_resource.update_free_resource import Controller as UpdateController
from src.routes.delete_free_resource.delete_free_resource import Controller as DeleteController

class Test_FreeResourceLambda:
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

        assert response.status_code == 201

    @pytest.mark.skip(reason='Done')
    def test_lambda_get_all(self):
        body = self.get_body()

        body['limit'] = 10
        body['last_evaluated_key'] = ''

        controller = GetAllController()

        response = self.call_lambda(controller, body)

        assert response.status_code == 200

    @pytest.mark.skip(reason='Done')
    def test_lambda_get_all_with_tags(self):
        body = self.get_body()

        body['tags'] = [ 'teste' ]
        body['limit'] = 10
        body['last_evaluated_key'] = ''

        controller = GetAllController()

        response = self.call_lambda(controller, body)

        assert response.status_code == 200

    @pytest.mark.skip(reason='Done')
    def test_lambda_get_one(self):
        body = self.get_body()

        body['id'] = 'f3f3fdec-3ecb-4717-9f60-7261fc401ab3'

        controller = GetOneController()

        response = self.call_lambda(controller, body)

        assert response.status_code == 200

    @pytest.mark.skip(reason='Done')
    def test_lambda_get_one_by_title(self):
        body = self.get_body()

        body['title'] = 'Test FreeResource'

        controller = GetOneController()

        response = self.call_lambda(controller, body)
        
        assert response.status_code == 200

    @pytest.mark.skip(reason='Done')
    def test_lambda_update(self):
        body = self.get_body()

        body['free_resource'] = {
            'id': '95f57894-f802-49f9-8c2b-463a76d19b33',
            'title': 'Test FreeResource updated',
            'external_url': 'https://www.google.com/',
            'tags': [ 'teste', 'free', 'maisuma' ]
        }
        
        controller = UpdateController()

        response = self.call_lambda(controller, body)
        
        assert response.status_code == 200

    @pytest.mark.skip(reason='Done')
    def test_lambda_delete(self):
        body = self.get_body()

        body['id'] = '95f57894-f802-49f9-8c2b-463a76d19b33'

        controller = DeleteController()

        response = self.call_lambda(controller, body)

        assert response.status_code == 200