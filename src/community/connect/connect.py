import json
import urllib.request

import src.shared.pyjwt.jwt as jwt
from src.shared.environments import Environments
from src.shared.infra.repositories.dtos.auth_authorizer_dto import AuthAuthorizerDTO

JWKS_URL = f'https://cognito-idp.{Environments.region}.amazonaws.com/{Environments.user_pool_id}/.well-known/jwks.json'

with urllib.request.urlopen(JWKS_URL) as f:
    JWKS = json.loads(f.read())['keys']

class Controller:
    connection_id: str

    def __init__(self, connection_id: str):
        self.connection_id = connection_id

    def decode_access_token(self, access_token: str) -> AuthAuthorizerDTO | None:
        try:
            not_verified_claims = jwt.get_unverified_claims(access_token)

            claims = jwt.decode(
                access_token,
                JWKS,
                algorithms=[ 'RS256' ],
                audience=not_verified_claims['aud'],
                issuer=f'https://cognito-idp.{Environments.region}.amazonaws.com/{Environments.user_pool_id}'
            )

            return AuthAuthorizerDTO.from_api_gateway(claims)
        except:
            return None

def lambda_handler(event, context) -> dict:
    connection_id = event.get('requestContext', {}) \
        .get('connectionId', '')

    print(f'Connecting: {connection_id}')

    query_params = event.get('queryStringParameters', {})
    access_token = query_params.get('auth', None)

    if access_token is None:
        return { 'statusCode': 401, 'body': 'Token de acesso não foi encontrado ("auth=")' }
    
    controller = Controller(connection_id)

    requester_user = controller.decode_access_token(access_token)

    if requester_user is None:
        return { 'statusCode': 401, 'body': 'Acesso não autorizado' }
    
    print('User data:\n' + json.dumps(requester_user, indent=4, ensure_ascii=False))
    
    return { 'statusCode': 200 }