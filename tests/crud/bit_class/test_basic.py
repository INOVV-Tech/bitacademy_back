import pytest

from tests.common import load_app_env, get_requester_user

load_app_env()

from src.shared.helpers.external_interfaces.http_models import HttpRequest

from src.routes.create_bit_class.create_bit_class import Controller as CreateController
from src.routes.get_all_bit_classes.get_all_bit_classes import Controller as GetAllController
from src.routes.get_one_bit_class.get_one_bit_class import Controller as GetOneController
from src.routes.update_bit_class.update_bit_class import Controller as UpdateController
from src.routes.delete_bit_class.delete_bit_class import Controller as DeleteController

class Test_BitClass:
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

        body['bit_class'] = {
            'title': 'Test BitClass',
            'external_url': 'https://www.youtube.com/',
            'tags': [ 'teste', 'free' ],
            'vip_level': 1
        }

        controller = CreateController()

        response = self.call_lambda(controller, body)

        assert response.status_code == 200

    @pytest.mark.skip(reason='Done')
    def test_lambda_get_all(self):
        body = self.get_body()

        body['limit'] = 10
        body['last_evaluated_key'] = ''

        controller = GetAllController()

        response = self.call_lambda(controller, body)

        assert response.status_code == 200

    # @pytest.mark.skip(reason='Done')
    def test_lambda_get_one(self):
        body = self.get_body()

        body['id'] = 'f3f3fdec-3ecb-4717-9f60-7261fc401ab3'

        controller = GetOneController()

        response = self.call_lambda(controller, body)

        assert response.status_code == 200

    @pytest.mark.skip(reason='Done')
    def test_lambda_get_one_by_title(self):
        body = self.get_body()

        body['title'] = 'Test BitClass'

        controller = GetOneController()

        response = self.call_lambda(controller, body)
        
        assert response.status_code == 200

    @pytest.mark.skip(reason='Done')
    def test_lambda_update(self):
        body = self.get_body()

        body['bit_class'] = {
            'id': '95f57894-f802-49f9-8c2b-463a76d19b33',
            'title': 'Test BitClass updated',
            'external_url': 'https://www.google.com/',
            'tags': [ 'teste', 'free', 'maisuma' ],
            'vip_level': 0
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