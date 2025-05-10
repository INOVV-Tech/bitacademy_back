from abc import ABC, abstractmethod

from src.shared.domain.enums.role import ROLE

from src.shared.infra.repositories.dtos.user_cognito_dto import UserCognitoDTO

class IAuthRepository(ABC):
    @abstractmethod
    def get_user_by_email(self, email: str) -> UserCognitoDTO | None:
        pass

    @abstractmethod
    def update_user_role(self, email: str, role: ROLE) -> bool:
        pass

    @abstractmethod
    def create_user(self, email: str, name: str, role: ROLE) -> UserCognitoDTO | None:
        pass