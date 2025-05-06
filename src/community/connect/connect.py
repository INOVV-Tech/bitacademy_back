from src.shared.infra.repositories.repository import Repository

from src.shared.domain.entities.community import CommunitySession

from src.shared.utils.time import now_timestamp
from src.shared.utils.websocket_jwt import decode_cognito_jwt_token

def lambda_handler(event, context) -> dict:
    connection_id = event.get('requestContext', {}) \
        .get('connectionId', '')

    access_token = event.get('queryStringParameters', {}) \
        .get('auth', None)

    if access_token is None:
        return { 'statusCode': 401, 'body': 'Token de acesso não foi encontrado ("auth=")' }

    requester_user = decode_cognito_jwt_token(access_token)

    if requester_user is None:
        return { 'statusCode': 401, 'body': 'Acesso não autorizado' }
    
    repository = Repository(community_repo=True)

    community_session = repository.community_repo.get_user_session(requester_user.user_id)

    if community_session is not None:
        community_session.connection_id = connection_id
        repository.community_repo.update_session(community_session)
        
        return { 'statusCode': 200 }

    community_session = CommunitySession(
        connection_id=connection_id,
        user_id=requester_user.user_id,
        user_name=requester_user.name,
        user_role=requester_user.role,
        created_at=now_timestamp()
    )
    
    repository.community_repo.create_session(community_session)

    return { 'statusCode': 200 }