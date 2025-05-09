import json
import pytest

from tests.common import load_app_env, get_requester_user, \
    load_resource

load_app_env()

from src.shared.helpers.external_interfaces.http_models import HttpRequest

from src.routes.create_free_material.create_free_material import Controller as CreateController
from src.routes.get_all_free_materials.get_all_free_materials import Controller as GetAllController
from src.routes.get_one_free_material.get_one_free_material import Controller as GetOneController
from src.routes.update_free_material.update_free_material import Controller as UpdateController
from src.routes.delete_free_material.delete_free_material import Controller as DeleteController

class Test_FreeMaterialLambda:
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
    def test_lambda_create(self):
        body = self.get_body()

        cover_img = load_resource('catbeach.png',
            encode_base64=True, base64_prefix='data:image/png;base64')

        body['free_material'] = {
            'title': 'O que são criptomoedas? Realmente valem à pena?',
            'description': 'O que são Criptomoedas? Imagine uma revolução no mundo financeiro, uma nova forma de dinheiro que não só redefine como realizamos transações, mas também nos dá o poder de controle total sobre nossos ativos. Esse avanço é representado pelas criptomoedas, um tipo de dinheiro puramente digital que utiliza uma tecnologia extremamente sofisticada, conhecida como criptografia, para garantir transações seguras e, na maioria das vezes, anônimas. Ao contrário das moedas tradicionais, como o real ou o dólar, que você pode segurar em mãos, as criptomoedas existem somente no ambiente digital.',
            'cover_img': cover_img,
            'external_url': 'https://www.youtube.com/',
            'tags': [ 'teste', 'free' ]
        }

        controller = CreateController()

        response = self.call_lambda(controller, body)

        self.print_data(response.data)

        assert response.status_code == 201

    @pytest.mark.skip(reason='Done')
    def test_lambda_get_all(self):
        body = self.get_body()

        query_params = {
            'limit': 10,
            'next_cursor': '',
            'sort_order': 'desc'
        }

        controller = GetAllController()

        response = self.call_lambda(controller, body, query_params=query_params)

        self.print_data(response.data)

        assert response.status_code == 200

    @pytest.mark.skip(reason='Done')
    def test_lambda_get_all_with_tags(self):
        body = self.get_body()

        query_params = {
            'tags': 'teste',
            'limit': 10,
            'next_cursor': '',
            'sort_order': 'desc'
        }

        controller = GetAllController()

        response = self.call_lambda(controller, body, query_params=query_params)

        self.print_data(response.data)

        assert response.status_code == 200

    @pytest.mark.skip(reason='Done')
    def test_lambda_get_one(self):
        body = self.get_body()

        query_params = {
            'id': '69ff308e-8a9f-49d8-beb1-7dbba1bf14aa'
        }

        controller = GetOneController()

        response = self.call_lambda(controller, body, query_params=query_params)

        self.print_data(response.data)

        assert response.status_code == 200

    @pytest.mark.skip(reason='Done')
    def test_lambda_get_one_by_title(self):
        body = self.get_body()

        query_params = {
            'title': 'O que são criptomoedas?'
        }

        controller = GetOneController()

        response = self.call_lambda(controller, body, query_params=query_params)

        self.print_data(response.data)
        
        assert response.status_code == 200

    @pytest.mark.skip(reason='Done')
    def test_lambda_update(self):
        body = self.get_body()

        cover_img = load_resource('catbeach.png',
            encode_base64=True, base64_prefix='data:image/png;base64')

        body['free_material'] = {
            'id': 'e3bf2dfd-67ef-445f-8d54-7387a1be2e0f',
            'title': 'UPDATED',
            'description': 'UPDATED',
            'cover_img': cover_img,
            'external_url': 'https://www.google.com/',
            'tags': [ 'teste', 'free', 'maisuma' ]
        }
        
        controller = UpdateController()

        response = self.call_lambda(controller, body)

        self.print_data(response.data)
        
        assert response.status_code == 200

    @pytest.mark.skip(reason='Done')
    def test_lambda_delete(self):
        body = self.get_body()

        body['id'] = 'e3bf2dfd-67ef-445f-8d54-7387a1be2e0f'

        controller = DeleteController()

        response = self.call_lambda(controller, body)

        assert response.status_code == 200