from src.shared.infra.repositories.repository import Repository

from src.shared.domain.entities.community import CommunitySession

from src.shared.utils.time import now_timestamp, sleep_random_float
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

    session_lock = None

    for i in range(0, 3):
        session_lock = repository.community_repo.acquire_session_lock(requester_user.user_id)

        if session_lock is not None:
            break
        
        sleep_random_float()

    if session_lock is None:
        return { 'statusCode': 401, 'body': 'Usuário não pode criar mais sessões no momento' }
    
    session_count = repository.community_repo.count_user_sessions(requester_user.user_id)

    if session_count >= 3:
        repository.community_repo.release_session_lock(requester_user.user_id)

        return { 'statusCode': 401, 'body': 'Usuário não pode criar mais que 3 sessões' }

    session = CommunitySession(
        connection_id=connection_id,
        user_id=requester_user.user_id,
        user_name=requester_user.name,
        user_role=requester_user.role,
        created_at=now_timestamp()
    )

    repository.community_repo.create_session(session)
    repository.community_repo.release_session_lock(requester_user.user_id)

    return { 'statusCode': 200 }