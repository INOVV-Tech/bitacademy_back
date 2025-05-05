from src.shared.infra.repositories.repository import Repository

def lambda_handler(event, context) -> dict:
    connection_id = event.get('requestContext', {}) \
        .get('connectionId', '')

    repository = Repository(community_repo=True)
    repository.community_repo.delete_session(connection_id)

    return { 'statusCode': 200 }