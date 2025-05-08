from src.shared.domain.enums.role import ROLE

from src.shared.infra.repositories.dtos.user_cognito_dto import UserCognitoDTO

class AuthAuthorizerDTO:
    user_id: str
    name: str
    email: str
    phone: str
    role: ROLE
    email_verified: bool
    phone_verified: bool

    @staticmethod
    def from_api_gateway(data: dict) -> 'AuthAuthorizerDTO':
        return AuthAuthorizerDTO(
            user_id=data['sub'],
            name=data['name'],
            email=data['email'],
            phone=data['phone_number'] if 'phone_number' in data else '',
            role=ROLE[data['custom:role']] if 'custom:role' in data else ROLE.GUEST,
            email_verified=bool(data['email_verified']) if 'email_verified' in data else False,
            phone_verified=bool(data['phone_number_verified']) if 'phone_number_verified' in data else False
        )
    
    @staticmethod
    def from_user_dto(user_dt: UserCognitoDTO) -> 'AuthAuthorizerDTO':
        return AuthAuthorizerDTO(
            user_id=user_dt.user_id,
            name=user_dt.name,
            email=user_dt.email,
            phone=user_dt.phone,
            role=user_dt.role,
            email_verified=user_dt.email_verified,
            phone_verified=user_dt.phone_verified
        )
    
    def __init__(self, user_id: str, name: str, email: str, phone: str, role: ROLE, \
        email_verified: bool, phone_verified: bool):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.phone = phone
        self.role = role
        self.email_verified = email_verified
        self.phone_verified = phone_verified

    def to_dict(self) -> dict:
        return {
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'role': self.role.value,
            'email_verified': self.email_verified,
            'phone_verified': self.phone_verified
        }