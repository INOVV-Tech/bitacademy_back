from abc import ABC, abstractmethod
from typing import List, Tuple

from src.shared.domain.entities.user import User
from src.shared.domain.enums.role import ROLE

class IAuthRepository(ABC):
    @abstractmethod
    def get_all_users(self) -> List[User]:
        pass
    
    @abstractmethod
    def create_user(self, email: str, name: str, phone: str, role: ROLE) -> User:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> User:
        pass

    @abstractmethod
    def update_user(self, email: str, attributes_to_update: dict, enabled: bool = None) -> User:
        pass

    @abstractmethod
    def refresh_token(self, refresh_token: str) -> Tuple[str, str, str]:
        pass

    @abstractmethod
    def enable_user(self, user_email: str) -> None:
        pass

    @abstractmethod
    def disable_user(self, user_email: str) -> None:
        pass