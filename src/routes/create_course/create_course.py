from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

from src.shared.infra.repositories.repository import Repository
from src.shared.infra.repositories.dtos.auth_authorizer_dto import AuthAuthorizerDTO

from src.shared.domain.enums.role import ROLE
from src.shared.domain.entities.course import Course
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
            course_repo=True,
            tag_repo=True
        )

    def execute(self, requester_user: AuthAuthorizerDTO, request_data: dict, request_params: dict) -> dict:
        if 'course' not in request_data \
            or not isinstance(request_data['course'], dict):
            return { 'error': 'Campo "course" não foi encontrado' }

        (error, course) = Course.from_request_data(request_data['course'], requester_user.user_id)

        if error != '':
            return { 'error': error }
        
        s3_datasource = self.repository.get_s3_datasource()

        upload_cover_resp = course.cover_img.store_in_s3(s3_datasource)

        if 'error' in upload_cover_resp:
            return upload_cover_resp
        
        upload_card_resp = course.card_img.store_in_s3(s3_datasource)

        if 'error' in upload_card_resp:
            return upload_card_resp
        
        self.repository.course_repo.create(course)

        tags = Tag.from_string_list(course.tags)

        if len(tags) > 0:
            for tag in tags:
                self.repository.tag_repo.create(tag)

        return {
            'course': course.to_public_dict()
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