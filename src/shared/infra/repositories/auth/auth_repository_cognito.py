import boto3

from src.shared.environments import Environments

from src.shared.domain.repositories.auth_repository_interface import IAuthRepository

from src.shared.infra.repositories.dtos.user_cognito_dto import UserCognitoDTO

class AuthRepositoryCognito(IAuthRepository):
    client_id: str
    user_pool_id: str

    client: boto3.client

    def __init__(self):
        self.client_id = Environments.app_client_id
        self.user_pool_id = Environments.user_pool_id

        self.client = boto3.client('cognito-idp', region_name=Environments.region)
    
    def get_user_by_email(self, email: str) -> UserCognitoDTO | None:
        try:
            response = self.client.admin_get_user(
                UserPoolId=self.user_pool_id,
                Username=email
            )

            if response['UserStatus'] == 'UNCONFIRMED':
                return None
                
            return UserCognitoDTO.from_cognito(response)
        except:
            return None