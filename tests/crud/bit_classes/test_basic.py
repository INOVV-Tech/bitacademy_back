import pytest

from tests.common import get_requester_user

from src.shared.helpers.external_interfaces.http_models import HttpRequest

from src.routes.create_bit_class.create_bit_class import Controller as CreateController
from src.routes.get_all_bit_classes.get_all_bit_classes import Controller as GetAllController
from src.routes.get_one_bit_class.get_one_bit_class import Controller as GetOneController
from src.routes.update_bit_class.update_bit_class import Controller as UpdateController
from src.routes.delete_bit_class.delete_bit_class import Controller as DeleteController

class Test_BitClass:
    def get_body(self):
        return {
            'requests_user': get_requester_user()
        }
    
    def call_lambda(self, controller, body={}, headers={}, query_params={}):
        request = HttpRequest(body=body, headers=headers, query_params=query_params)

        return controller.execute(request)

    def test_lambda_create(self):
        body = self.get_body()

        print('body', body)

        assert True

    def test_lambda_get_all(self):
        assert True

    def test_lambda_get_one(self):
        assert True

    def test_lambda_update(self):
        assert True

    def test_lambda_delete(self):
        assert True