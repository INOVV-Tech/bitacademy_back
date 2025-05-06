import json
import urllib.request

import src.shared.pyjwt.jwt as jwt
from src.shared.environments import Environments

from src.shared.infra.repositories.dtos.auth_authorizer_dto import AuthAuthorizerDTO

JWKS_URL = f'https://cognito-idp.{Environments.region}.amazonaws.com/{Environments.user_pool_id}/.well-known/jwks.json'

def decode_cognito_jwt_token(token: str) -> AuthAuthorizerDTO | None:
    try:
        with urllib.request.urlopen(JWKS_URL) as f:
            JWKS = json.loads(f.read())['keys']
        
        not_verified_claims = jwt.get_unverified_claims(token)

        claims = jwt.decode(
            token,
            JWKS,
            algorithms=[ 'RS256' ],
            audience=not_verified_claims['aud'],
            issuer=f'https://cognito-idp.{Environments.region}.amazonaws.com/{Environments.user_pool_id}'
        )

        if claims is None:
            return None
        
        return AuthAuthorizerDTO.from_api_gateway(claims)
    except:
        return None