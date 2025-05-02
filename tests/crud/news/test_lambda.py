import json
import pytest

from tests.common import load_app_env, get_requester_user, \
    load_resource

load_app_env()

from src.shared.helpers.external_interfaces.http_models import HttpRequest

from src.routes.create_news.create_news import Controller as CreateController
from src.routes.get_all_news.get_all_news import Controller as GetAllController
from src.routes.get_one_news.get_one_news import Controller as GetOneController
from src.routes.update_news.update_news import Controller as UpdateController
from src.routes.delete_news.delete_news import Controller as DeleteController

class Test_NewsLambda:
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
        
        news_list = [
            {
                'title': 'Test News 1',
                'header': 'uhul header',
                'content': 'Conteúdo teste da notícia',
                'tags': [ 'teste', 'free' ],
                'vip_level': 1,
                'cover_img': cover_img,
                'card_img': cover_img
            },
            {
                'title': 'Test News 2',
                'header': 'uhul header',
                'content': 'Conteúdo teste da notícia',
                'tags': [ 'teste', 'free' ],
                'vip_level': 1,
                'cover_img': cover_img,
                'card_img': cover_img
            },
            {
                'title': 'Test News 3',
                'header': 'uhul header',
                'content': 'Conteúdo teste da notícia',
                'tags': [ 'teste', 'free' ],
                'vip_level': 1,
                'cover_img': cover_img,
                'card_img': cover_img
            },
            {
                'title': 'Test News 4',
                'header': 'uhul header',
                'content': 'Conteúdo teste da notícia',
                'tags': [ 'teste', 'free' ],
                'vip_level': 1,
                'cover_img': cover_img,
                'card_img': cover_img
            }
        ]

        for news in news_list:
            body['news'] = news

            controller = CreateController()

            response = self.call_lambda(controller, body)

            self.print_data(response.data)

        assert response.status_code == 201

    @pytest.mark.skip(reason='Done')
    def test_lambda_get_all(self):
        body = self.get_body()

        query_params = {
            'limit': 2,
            'next_cursor': 'eyJTSyI6ICJNRVRBREFUQSIsICJHU0lfRU5USVRZX0dFVEFMTF9TSyI6ICJEQVRFIzE3NDYxNDQwNDUiLCAiUEsiOiAiTkVXUyM0ZDI5OTM4Ni05Zjc3LTQ5M2UtOTRmYy1jNzQxM2Q1Zjc3M2YiLCAiR1NJX0VOVElUWV9HRVRBTExfUEsiOiAiSU5ERVgjTkVXUyJ9',
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
            'id': '4e6139d5-43a7-4d4f-813c-c41716456de8'
        }

        controller = GetOneController()

        response = self.call_lambda(controller, body, query_params=query_params)

        self.print_data(response.data)

        assert response.status_code == 200

    @pytest.mark.skip(reason='Done')
    def test_lambda_get_one_by_title(self):
        body = self.get_body()

        query_params = {
            'title': 'Test News'
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

        body['news'] = {
            'id': 'a30f03bf-55da-4e6a-99e4-61d816d22062',
            'title': 'Test News updated',
            'header': 'UPDATED',
            'content': 'UPDATED',
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

        body['id'] = 'fce39bab-cbcc-4899-8108-1cc854d714b0'

        controller = DeleteController()

        response = self.call_lambda(controller, body)

        assert response.status_code == 200