from src.shared.domain.enums.role import ROLE

class AuthAuthorizerDTO:
    user_id: str
    name: str
    email: str
    role: ROLE
    email_verified: bool

    def __init__(self, user_id: str, name: str, email: str, role: ROLE, email_verified: bool = False):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.role = role
        self.email_verified = email_verified

    @staticmethod
    def from_api_gateway(user_data: dict) -> 'AuthAuthorizerDTO':
        return AuthAuthorizerDTO(
            user_id=user_data['user_id'],
            name=user_data['name'],
            email=user_data['email'],
            role=ROLE[user_data['role']],
            email_verified=user_data['email_verified'],
        )
    
    def __eq__(self, other):
        return self.user_id == other.user_id and self.email == other.email and self.role == other.role and self.name == other.name and self.email_verified == other.email_verified