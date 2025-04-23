import pytest

from tests.common import load_app_env, get_requester_user, \
    load_resource

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

    # @pytest.mark.skip(reason='Done')
    def test_lambda_create(self):
        body = self.get_body()

        cover_img = load_resource('free_resource_cover_img.jpg')

        body['free_resource'] = {
            'title': 'O que são criptomoedas? Realmente valem à pena?',
            'description': 'O que são Criptomoedas? Imagine uma revolução no mundo financeiro, uma nova forma de dinheiro que não só redefine como realizamos transações, mas também nos dá o poder de controle total sobre nossos ativos. Esse avanço é representado pelas criptomoedas, um tipo de dinheiro puramente digital que utiliza uma tecnologia extremamente sofisticada, conhecida como criptografia, para garantir transações seguras e, na maioria das vezes, anônimas. Ao contrário das moedas tradicionais, como o real ou o dólar, que você pode segurar em mãos, as criptomoedas existem somente no ambiente digital.',
            'cover_img': cover_img,
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