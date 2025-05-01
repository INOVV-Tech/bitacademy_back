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
    email_verified: bool
    phone_verified: bool
    enabled: bool

    def __init__(self, user_id: str, name: str, email: str, phone: str, role: ROLE, \
        email_verified: bool, phone_verified: bool, enabled: bool):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.phone = phone
        self.role = role
        self.email_verified = email_verified
        self.phone_verified = phone_verified
        self.enabled = enabled

    @staticmethod
    def from_api_gateway(data: dict) -> 'AuthAuthorizerDTO':
        return AuthAuthorizerDTO(
            user_id=data['sub'],
            name=data['name'],
            email=data['email'],
            phone=data['phone_number'],
            role=ROLE[data['custom:role']],
            email_verified=data['email_verified'],
            phone_verified=data['phone_verified'],
            enabled=True
        )
    
    def __eq__(self, other: 'AuthAuthorizerDTO') -> bool:
        return self.user_id == other.user_id \
            and self.name == other.name \
            and self.email == other.email \
            and self.phone == other.phone \
            and self.role == other.role \
            and self.email_verified == other.email_verified \
            and self.phone_verified == other.phone_verified \
            and self.enabled == other.enabled \
    
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
            email_verified=self.email_verified,
            phone_verified=self.phone_verified,
            enabled=self.enabled
        )