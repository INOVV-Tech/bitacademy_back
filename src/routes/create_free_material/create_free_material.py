from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

from src.shared.infra.repositories.repository import Repository
from src.shared.infra.repositories.dtos.auth_authorizer_dto import AuthAuthorizerDTO

from src.shared.domain.enums.role import ROLE
from src.shared.domain.entities.free_material import FreeMaterial
from src.shared.domain.entities.tag import Tag

from src.shared.utils.routing import controller_execute

ALLOWED_USER_ROLES = [ ROLE.ADMIN ]

class Controller:
    @staticmethod
    def execute(request: IRequest) -> IResponse:
        return controller_execute(
            Usecase=Usecase,
            request=request,
            allowed_user_roles=ALLOWED_USER_ROLES,
            fetch_vip_subscription=False,
            return_created=True
        )

class Usecase:
    repository: Repository

    def __init__(self):
        self.repository = Repository(
            free_material_repo=True,
            tag_repo=True
        )

    def execute(self, requester_user: AuthAuthorizerDTO, request_data: dict, request_params: dict) -> dict:
        if 'free_material' not in request_data \
            or not isinstance(request_data['free_material'], dict):
            return { 'error': 'Campo "free_material" não foi encontrado' }

        (error, free_material) = FreeMaterial.from_request_data(request_data['free_material'], requester_user.user_id)

        if error != '':
            return { 'error': error }

        s3_datasource = self.repository.get_s3_datasource()

        upload_resp = free_material.cover_img.store_in_s3(s3_datasource)

        if 'error' in upload_resp:
            return upload_resp
        
        self.repository.free_material_repo.create(free_material)

        tags = Tag.from_string_list(free_material.tags)

        if len(tags) > 0:
            for tag in tags:
                self.repository.tag_repo.create(tag)

        return {
            'free_material': free_material.to_public_dict()
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