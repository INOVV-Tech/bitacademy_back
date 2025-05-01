from src.shared.domain.enums.role import ROLE

from src.shared.domain.enums.user_status import USER_STATUS
from src.shared.domain.entities.user import User

from src.shared.utils.time import now_timestamp

class AuthAuthorizerDTO:
    user_id: str
    name: str
    email: str
    phone: str
    role: ROLE
    enabled: bool
    email_verified: bool

    def __init__(self, user_id: str, name: str, email: str, phone: str, role: ROLE, \
        enabled: bool, email_verified: bool):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.phone = phone
        self.role = role
        self.enabled = enabled
        self.email_verified = email_verified

    @staticmethod
    def from_create_request(data: dict) -> 'AuthAuthorizerDTO':
        return AuthAuthorizerDTO(
            user_id='',
            name=data['name'],
            email=data['email'],
            phone=data['phone_number'],
            role=ROLE[data['custom:role']],
            enabled=True,
            email_verified=False
        )

    @staticmethod
    def from_api_gateway(data: dict) -> 'AuthAuthorizerDTO':
        return AuthAuthorizerDTO(
            user_id=data['user_id'],
            name=data['name'],
            email=data['email'],
            phone=data['phone_number'],
            role=ROLE[data['custom:role']],
            enabled=data['enabled'],
            email_verified=data['email_verified'],
        )
    
    def __eq__(self, other: 'AuthAuthorizerDTO') -> bool:
        return self.user_id == other.user_id \
            and self.email == other.email \
            and self.phone == other.phone \
            and self.role == other.role \
            and self.name == other.name \
            and self.enabled == other.enabled \
            and self.email_verified == other.email_verified
    
    def to_new_user(self) -> User:
        now = now_timestamp()

        return User(
            user_id=self.user_id,
            name=self.name,
            email=self.email,
            phone=self.phone,
            role=self.role.value,
            user_status=USER_STATUS.UNKNOWN,
            created_at=now,
            updated_at=now,
            enabled=self.enabled,
            email_verified=self.email_verified
        )