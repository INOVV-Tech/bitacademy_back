import boto3
from typing import Tuple, List
from botocore.exceptions import ClientError

from src.shared.environments import Environments

from src.shared.domain.entities.user import User
from src.shared.domain.repositories.auth_repository_interface import IAuthRepository

from src.shared.helpers.errors.errors import DuplicatedItem, EntityError, ForbiddenAction, InvalidTokenError

from src.shared.infra.repositories.dtos.user_cognito_dto import UserCognitoDTO

class AuthCognitoRepository(IAuthRepository):
    client_id: str
    user_pool_id: str

    client: boto3.client
    
    def __init__(self):
        self.client_id = Environments.app_client_id
        self.user_pool_id = Environments.user_pool_id

        self.client = boto3.client('cognito-idp', region_name=Environments.region)

    def create_user(self, user: User) -> User:
        cognito_attributes = [
            {
                'Name': 'email',
                'Value': user.email
            },
            {
                'Name': 'name',
                'Value': user.name
            },
            {
                'Name': 'phone_number',
                'Value': user.phone
            },
            {
                'Name': 'custom:general_role',
                'Value': user.role.value
            }
        ]

        try:
            self.client.admin_create_user(
                UserPoolId=self.user_pool_id,
                Username=user.email,
                DesiredDeliveryMediums=['EMAIL'],
                UserAttributes=cognito_attributes
            )
            
            return self.get_user_by_email(user.email)
        except self.client.exceptions.UsernameExistsException:
            raise DuplicatedItem('user')
        except self.client.exceptions.InvalidParameterException as e:
            raise EntityError(e.response.get('Error').get('Message'))
        except:
            raise Exception('Cognito falhou por motivo desconhecido')
    
    def get_all_users(self, page: int) -> List[User]:
        try:
            kwargs = {
                'UserPoolId': self.user_pool_id,
                'Limit': 20
            }

            all_users = list()
            users_remain = True
            next_page = None

            while users_remain and len(all_users) < page * 20:
                if next_page:
                    kwargs['PaginationToken'] = next_page
                
                response = self.client.list_users(**kwargs)

                all_users.extend(response['Users'])

                next_page = response.get('PaginationToken', None)
                users_remain = next_page is not None

            paginated_users = all_users[(page - 1) * 20: page * 20]

            all_users_entities = [ UserCognitoDTO.from_cognito(user).to_entity() for user in paginated_users ]

            return all_users_entities
        except self.client.exceptions.ResourceNotFoundException as e:
            raise EntityError(e.response.get('Error').get('Message'))
        except self.client.exceptions.InvalidParameterException as e:
            raise EntityError(e.response.get('Error').get('Message'))
        except:
            raise Exception('Cognito falhou por motivo desconhecido')
    
    def get_user_by_email(self, email: str) -> User:
        try:
            response = self.client.admin_get_user(
                UserPoolId=self.user_pool_id,
                Username=email
            )

            if response['UserStatus'] == 'UNCONFIRMED':
                return None

            user = UserCognitoDTO.from_cognito(response).to_entity()
                
            return user
        except:
            return None
    
    def update_user(self, email: str, attributes_to_update: dict, enabled: bool = None) -> User:
        try:
            user_attributes = []

            for key, value in attributes_to_update.items():
                if key in UserCognitoDTO.TO_COGNITO_DICT:
                    user_attributes.append({ 'Name': UserCognitoDTO.TO_COGNITO_DICT[key], 'Value': value })

            self.client.admin_update_user_attributes(
                UserPoolId=self.user_pool_id,
                Username=email,
                UserAttributes=user_attributes
            )

            user = self.get_user_by_email(email)

            if enabled is not None:
                if enabled:
                    self.enable_user(email)
                else:
                    self.disable_user(email)
                
                user.enabled = enabled
            
            # TODO: definir "sign_out_user"
            # self.sign_out_user(email)
            
            return user
        except self.client.exceptions.InvalidParameterException as e:
            raise EntityError(e.response.get('Error').get('Message'))
        except:
            raise Exception('Cognito falhou por motivo desconhecido')
    
    def refresh_token(self, refresh_token: str) -> Tuple[str, str, str]:
        try:
            response = self.client.initiate_auth(
                ClientId=self.client_id,
                AuthFlow='REFRESH_TOKEN_AUTH',
                AuthParameters={
                    'REFRESH_TOKEN': refresh_token
                }
            )

            id_token = response['AuthenticationResult']['IdToken']
            access_token = response['AuthenticationResult']['AccessToken']

            return access_token, refresh_token, id_token
        except ClientError as e:
            errorCode = e.response.get('Error').get('Code')

            if errorCode == 'NotAuthorizedException':
                raise InvalidTokenError(message=e.response.get('Error').get('Message'))
            else:
                raise ForbiddenAction(message=e.response.get('Error').get('Message'))
        except:
            raise Exception('Cognito falhou por motivo desconhecido')
    
    def enable_user(self, user_email: str) -> None:
        try:
            self.client.admin_enable_user(
                UserPoolId=self.user_pool_id,
                Username=user_email
            )
        except self.client.exceptions.ResourceNotFoundException as e:
            raise EntityError(e.response.get('Error').get('Message'))
        except self.client.exceptions.InvalidParameterException as e:
            raise EntityError(e.response.get('Error').get('Message'))
        except:
            raise Exception('Cognito falhou por motivo desconhecido')
    
    def disable_user(self, user_email: str) -> None:
        try:
            self.client.admin_disable_user(
                UserPoolId=self.user_pool_id,
                Username=user_email
            )
        except self.client.exceptions.ResourceNotFoundException as e:
            raise EntityError(e.response.get('Error').get('Message'))
        except self.client.exceptions.InvalidParameterException as e:
            raise EntityError(e.response.get('Error').get('Message'))
        except:
            raise Exception('Cognito falhou por motivo desconhecido')