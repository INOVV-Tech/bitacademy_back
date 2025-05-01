import json
import pytest

from tests.common import load_app_env, get_requester_user, \
    load_resource

load_app_env()

from src.shared.helpers.external_interfaces.http_models import HttpRequest

from src.routes.create_tool.create_tool import Controller as CreateController
from src.routes.get_all_tools.get_all_tools import Controller as GetAllController
from src.routes.get_one_tool.get_one_tool import Controller as GetOneController
from src.routes.update_tool.update_tool import Controller as UpdateController
from src.routes.delete_tool.delete_tool import Controller as DeleteController

class Test_ToolLambda:
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

        body['tool'] = {
            'title': 'Test Tool',
            'description': 'Ferramenta inovadora para o monitoramento e gestão de criptomoedas, oferecendo dados em tempo real sobre preços, variações de mercado e tendências. Com uma interface intuitiva, permite que usuários acompanhem gráficos detalhados, configurem alertas personalizados e gerenciem seus portfólios de investimentos com segurança. Ideal para traders e investidores, a plataforma facilita a tomada de decisões estratégicas no dinâmico mercado de criptoativos.App com segurança e efetividade garantida.',
            'external_url': 'https://www.youtube.com/',
            'cover_img': cover_img,
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
            'last_evaluated_key': '',
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
            'limit': 10,
            'last_evaluated_key': '',
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
            'id': 'c035bbf8-b48b-47f8-9cf8-7da4fbbf9123'
        }

        controller = GetOneController()

        response = self.call_lambda(controller, body, query_params=query_params)

        self.print_data(response.data)

        assert response.status_code == 200

    @pytest.mark.skip(reason='Done')
    def test_lambda_get_one_by_title(self):
        body = self.get_body()

        query_params = {
            'title': 'Test Tool'
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

        body['tool'] = {
            'id': '1450b3b8-c22d-4df5-9c19-85da8c81bad4',
            'title': 'UPDATED',
            'description': 'UPDATED',
            'external_url': 'https://www.google.com/',
            'cover_img': cover_img,
            'tags': [ 'teste', 'free', 'UPDATED' ]
        }
        
        controller = UpdateController()

        response = self.call_lambda(controller, body)

        self.print_data(response.data)
        
        assert response.status_code == 200

    @pytest.mark.skip(reason='Done')
    def test_lambda_delete(self):
        body = self.get_body()

        body['id'] = '1450b3b8-c22d-4df5-9c19-85da8c81bad4'

        controller = DeleteController()

        response = self.call_lambda(controller, body)

        self.print_data(response.data)

        assert response.status_code == 200