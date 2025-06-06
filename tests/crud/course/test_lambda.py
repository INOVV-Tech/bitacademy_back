import json
import pytest

from tests.common import load_app_env, get_requester_user, \
    load_resource

load_app_env()

from src.shared.helpers.external_interfaces.http_models import HttpRequest

from src.routes.create_course.create_course import Controller as CreateController
from src.routes.get_all_courses.get_all_courses import Controller as GetAllController
from src.routes.get_one_course.get_one_course import Controller as GetOneController
from src.routes.update_course.update_course import Controller as UpdateController
from src.routes.delete_course.delete_course import Controller as DeleteController

class Test_CourseLambda:
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

        body['course'] = {
            'title': 'Test Course',
            'description': 'Domine os principais conceitos do mercado financeiro, conheça diferentes tipos de ativos e descubra estratégias para potencializar seus ganhos em renda fixa, variável e criptomoedas. Fundamentos do mercado financeiro Investimentos em renda fixa e variável Introdução às criptomoedas (Bitcoin, Ethereum e altcoins).',
            'teachers': [ 'Rogério Silva' ],
            'duration': '3 meses',
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
            'tags': [ 'teste' ],
            'vip_level': 1,
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
            'id': 'e160f143-1bb2-4d19-9b39-99e5b2799ca4'
        }

        controller = GetOneController()

        response = self.call_lambda(controller, body, query_params=query_params)

        self.print_data(response.data)

        assert response.status_code == 200

    @pytest.mark.skip(reason='Done')
    def test_lambda_get_one_by_title(self):
        body = self.get_body()

        query_params = {
            'title': 'Test Course'
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

        body['course'] = {
            'id': 'af43f947-7371-4d61-afea-90bbc6e88b6e',
            'title': 'Test Course updated',
            'description': 'Duração do Curso: 3 meses. Descrição: Domine os principais conceitos do mercado financeiro, conheça diferentes tipos de ativos e descubra estratégias para potencializar seus ganhos em renda fixa, variável e criptomoedas. Fundamentos do mercado financeiro Investimentos em renda fixa e variável Introdução às criptomoedas (Bitcoin, Ethereum e altcoins).',
            'teachers': [ 'Rogério Silva' ],
            'duration': '4 meses',
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

        body['id'] = '22a4fc15-2a22-4f1a-8b54-a035150331a2'

        controller = DeleteController()

        response = self.call_lambda(controller, body)

        self.print_data(response.data)

        assert response.status_code == 200