from src.shared.domain.enums.role import ROLE
from src.shared.domain.enums.user_status import USER_STATUS
from src.shared.domain.entities.user import User

class AuthAuthorizerDTO:
    user_id: str
    name: str
    email: str
    phone: str
    role: ROLE
    email_verified: bool
    phone_verified: bool

    def __init__(self, user_id: str, name: str, email: str, phone: str, role: ROLE, \
        email_verified: bool, phone_verified: bool):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.phone = phone
        self.role = role
        self.email_verified = email_verified
        self.phone_verified = phone_verified

    @staticmethod
    def from_api_gateway(data: dict) -> 'AuthAuthorizerDTO':
        return AuthAuthorizerDTO(
            user_id=data['sub'],
            name=data['name'],
            email=data['email'],
            phone=data['phone_number'],
            role=ROLE[data['custom:role']] if 'custom:role' in data else ROLE.GUEST,
            email_verified=data['email_verified'],
            phone_verified=data['phone_verified']
        )