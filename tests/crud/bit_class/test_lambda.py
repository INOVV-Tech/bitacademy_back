import json
import pytest

from tests.common import load_app_env, get_requester_user, \
    load_resource

load_app_env()

from src.shared.helpers.external_interfaces.http_models import HttpRequest

from src.routes.create_bit_class.create_bit_class import Controller as CreateController
from src.routes.get_all_bit_classes.get_all_bit_classes import Controller as GetAllController
from src.routes.get_one_bit_class.get_one_bit_class import Controller as GetOneController
from src.routes.update_bit_class.update_bit_class import Controller as UpdateController
from src.routes.delete_bit_class.delete_bit_class import Controller as DeleteController

class Test_BitClassLambda:
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

        cover_img = load_resource('free_resource_cover_img.jpg',
            encode_base64=True, base64_prefix='data:image/jpeg;base64')

        body['bit_class'] = {
            'title': 'Test BitClass',
            'description': 'Duração do Curso: 3 meses. Descrição: Domine os principais conceitos do mercado financeiro, conheça diferentes tipos de ativos e descubra estratégias para potencializar seus ganhos em renda fixa, variável e criptomoedas. Fundamentos do mercado financeiro Investimentos em renda fixa e variável Introdução às criptomoedas (Bitcoin, Ethereum e altcoins).',
            'teachers': [ 'Rogério Silva' ],
            'external_url': 'https://www.youtube.com/',
            'tags': [ 'teste', 'free' ],
            'vip_level': 1,
            'cover_img': cover_img,
            'card_img': cover_img
        }

        controller = CreateController()

        response = self.call_lambda(controller, body)

        self.print_data(response.data)

        assert response.status_code == 201

    @pytest.mark.skip(reason='Done')
    def test_lambda_get_all(self):
        body = self.get_body()

        body['limit'] = 10
        body['last_evaluated_key'] = ''

        controller = GetAllController()

        response = self.call_lambda(controller, body)

        self.print_data(response.data)

        assert response.status_code == 200

    @pytest.mark.skip(reason='Done')
    def test_lambda_get_all_with_tags(self):
        body = self.get_body()

        body['tags'] = [ 'teste' ]
        body['vip_level'] = 1
        body['limit'] = 10
        body['last_evaluated_key'] = ''

        controller = GetAllController()

        response = self.call_lambda(controller, body)

        assert response.status_code == 200

    @pytest.mark.skip(reason='Done')
    def test_lambda_get_one(self):
        body = self.get_body()

        body['id'] = 'a1ec6431-db19-4a60-a179-07b40f4ea7aa'

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

        cover_img = load_resource('free_resource_cover_img.jpg',
            encode_base64=True, base64_prefix='data:image/jpeg;base64')

        body['bit_class'] = {
            'id': '6548e4e5-dd8f-4921-b940-1047f97ac6bb',
            'title': 'Test BitClass updated',
            'description': 'Duração do Curso: 3 meses. Descrição: Domine os principais conceitos do mercado financeiro, conheça diferentes tipos de ativos e descubra estratégias para potencializar seus ganhos em renda fixa, variável e criptomoedas. Fundamentos do mercado financeiro Investimentos em renda fixa e variável Introdução às criptomoedas (Bitcoin, Ethereum e altcoins).',
            'teachers': [ 'Rogério Silva' ],
            'external_url': 'https://www.google.com/',
            'tags': [ 'teste', 'free', 'maisuma' ],
            'vip_level': 0,
            'cover_img': cover_img,
            'card_img': cover_img
        }
        
        controller = UpdateController()

        response = self.call_lambda(controller, body)

        self.print_data(response.data)
        
        assert response.status_code == 200

    @pytest.mark.skip(reason='Done')
    def test_lambda_delete(self):
        body = self.get_body()

        body['id'] = 'a1ec6431-db19-4a60-a179-07b40f4ea7aa'

        controller = DeleteController()

        response = self.call_lambda(controller, body)

        assert response.status_code == 200