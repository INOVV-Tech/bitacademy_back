from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.helpers.external_interfaces.http_codes import OK, InternalServerError, BadRequest
from src.shared.helpers.errors.errors import MissingParameters, ForbiddenAction

from src.shared.infra.repositories.repository import Repository
from src.shared.infra.repositories.dtos.auth_authorizer_dto import AuthAuthorizerDTO

from src.shared.domain.enums.role import ROLE
from src.shared.domain.entities.news import News

ALLOWED_USER_ROLES = [ ROLE.ADMIN, ROLE.CLIENT ]

class Controller:
    @staticmethod
    def execute(request: IRequest) -> IResponse:
        try:
            requester_user = AuthAuthorizerDTO.from_api_gateway(request.data.get('requester_user'))

            if requester_user.role not in ALLOWED_USER_ROLES:
                raise ForbiddenAction('Acesso não autorizado')
            
            response = Usecase().execute(request.data)

            if 'error' in response:
                return BadRequest(response['error'])
            
            return OK(body=response)
        except MissingParameters as error:
            return BadRequest(error.message)
        except:
            return InternalServerError('Erro interno de servidor')

class Usecase:
    repository: Repository

    def __init__(self):
        self.repository = Repository(news_repo=True)

    def execute(self, request_data: dict) -> dict:
        if News.data_contains_valid_id(request_data):
            return self.query_with_id(request_data)

        if News.data_contains_valid_title(request_data):
            return self.query_with_title(request_data)

        return { 'error': 'Nenhum identificador encontrado' }
    
    def query_with_id(self, request_data: dict) -> dict:
        news = self.repository.news_repo.get_one(request_data['id'])

        return {
            'news': news.to_public_dict() if news is not None else None
        }
    
    def query_with_title(self, request_data: dict) -> dict:
        news = self.repository.news_repo.get_one_by_title(request_data['title'])

        return {
            'news': news.to_public_dict() if news is not None else None
        }

def lambda_handler(event, context) -> LambdaHttpResponse:
    http_request = LambdaHttpRequest(event)

    http_request.data['requester_user'] = event.get('requestContext', {}) \
        .get('authorizer', {}) \
        .get('claims', None)
    
    response = Controller.execute(http_request)

    return LambdaHttpResponse(
        status_code=response.status_code, 
        body=response.body, 
        headers=response.headers
    ).toDict()