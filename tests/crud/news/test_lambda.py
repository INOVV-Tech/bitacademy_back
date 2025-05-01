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
            'requester_user': get_requester_user(admin=False)
        }
    
    def call_lambda(self, controller, body={}, headers={}, query_params={}):
        request = HttpRequest(body=body, headers=headers, query_params=query_params)

        return controller.execute(request)

    @pytest.mark.skip(reason='Done')
    def test_lambda_create(self):
        body = self.get_body()

        cover_img = load_resource('catbeach.png',
            encode_base64=True, base64_prefix='data:image/png;base64')

        body['news'] = {
            'title': 'Test News',
            'header': 'uhul header',
            'content': 'Conteúdo teste da notícia',
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
        body['sort_order'] = 'desc'

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
        body['sort_order'] = 'desc'

        controller = GetAllController()

        response = self.call_lambda(controller, body)

        self.print_data(response.data)

        assert response.status_code == 200

    @pytest.mark.skip(reason='Done')
    def test_lambda_get_one(self):
        body = self.get_body()

        body['id'] = '2e7cde25-bfca-4212-8d52-079aa71190d0'

        controller = GetOneController()

        response = self.call_lambda(controller, body)

        self.print_data(response.data)

        assert response.status_code == 200

    @pytest.mark.skip(reason='Done')
    def test_lambda_get_one_by_title(self):
        body = self.get_body()

        body['title'] = 'Test News'

        controller = GetOneController()

        response = self.call_lambda(controller, body)

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