from abc import ABC, abstractmethod

from src.shared.infra.repositories.dtos.user_cognito_dto import UserCognitoDTO

class IAuthRepository(ABC):
    @abstractmethod
    def get_user_by_email(self, email: str) -> UserCognitoDTO | None:
        pass