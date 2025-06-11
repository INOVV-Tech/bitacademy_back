from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

from src.shared.infra.repositories.repository import Repository
from src.shared.infra.repositories.dtos.auth_authorizer_dto import AuthAuthorizerDTO

from src.shared.domain.enums.role import ROLE
from src.shared.domain.entities.community import CommunityForumTopic

from src.shared.utils.routing import controller_execute
from src.shared.utils.entity import is_valid_getall_object
from src.shared.utils.pagination import encode_cursor_get_all, decode_cursor, encode_cursor

ALLOWED_USER_ROLES = [
    ROLE.GUEST,
    ROLE.AFFILIATE,
    ROLE.VIP,
    ROLE.TEACHER,
    ROLE.ADMIN
]

class Controller:
    @staticmethod
    def execute(request: IRequest) -> IResponse:
        return controller_execute(
            Usecase=Usecase,
            request=request,
            allowed_user_roles=ALLOWED_USER_ROLES,
            fetch_vip_subscription=True
        )

class Usecase:
    repository: Repository

    def __init__(self):
        self.repository = Repository(community_repo=True)

    def execute(self, requester_user: AuthAuthorizerDTO, request_data: dict, request_params: dict) -> dict:
        if not is_valid_getall_object(request_params):
            return { 'error': 'Filtro de consulta inválido' }
        
        if not CommunityForumTopic.data_contains_valid_channel_id(request_params):
            return { 'error': 'Identificador de canal de comunidade inválido' }
        
        if not self.repository.community_repo.role_can_read_channel(request_params['channel_id'], requester_user.role):
            return { 'error': 'O canal de comunidade não existe ou o usuário não tem permissão para lê-lo' }
        
        title = ''

        if CommunityForumTopic.data_contains_valid_title(request_params):
            title = request_params['title'].strip()

        db_data = self.repository.community_repo.get_channel_forum_topics(
            channel_id=request_params['channel_id'],
            title=title,
            limit=request_params['limit'],
            last_evaluated_key=decode_cursor(request_params['next_cursor']),
            sort_order=request_params['sort_order']
        )

        total = db_data['total']
        community_forum_topics: list[CommunityForumTopic] = db_data['community_forum_topics']

        community_messages = self.repository.community_repo.get_forum_last_messages(community_forum_topics)

        next_cursor = db_data['last_evaluated_key']
        next_cursor = encode_cursor(next_cursor) if next_cursor else ''

        output_data = []

        for community_forum_topic in community_forum_topics:
            last_message = next((x for x in community_messages if x.forum_topic_id == community_forum_topic.id), None)

            output_data.append(
                community_forum_topic.to_public_dict(last_message=last_message)
            )

        return {
            'total': total,
            'per_page': request_params['limit'],
            'data': output_data,
            'next_cursor': next_cursor,
            'has_more': bool(next_cursor)
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