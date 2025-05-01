import json
import pytest

from tests.common import load_app_env, get_requester_user

load_app_env()

from src.shared.helpers.external_interfaces.http_models import HttpRequest

from src.routes.create_user.create_user import Controller as CreateController

from src.shared.domain.enums.role import ROLE

class Test_UserLambda:
    def print_data(self, data: dict) -> None:
        print(json.dumps(data, indent=4, ensure_ascii=False))

    def get_body(self):
        return {}
    
    def get_auth_body(self):
        return {
            'requester_user': get_requester_user(admin=False)
        }
    
    def call_lambda(self, controller, body={}, headers={}, query_params={}):
        request = HttpRequest(body=body, headers=headers, query_params=query_params)

        return controller.execute(request)

    # @pytest.mark.skip(reason='Done')
    def test_lambda_create(self):
        body = self.get_auth_body()

        body['requester_user']['user_id'] = '9d7dcecd-cd67-4824-a73b-2386f1ec1c23'
        body['requester_user']['name'] = 'mazc'
        body['requester_user']['email'] = 'marcocoimbra01@gmail.com'
        body['requester_user']['role'] = ROLE.ADMIN.value

        controller = CreateController()

        response = self.call_lambda(controller, body)

        self.print_data(response.data)

        assert response.status_code == 201