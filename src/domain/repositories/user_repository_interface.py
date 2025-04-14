from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities.user import User

class IUserRepository(ABC):
  @abstractmethod
  def insert_user(self, user: User) -> User:
    pass
  
  @abstractmethod
  def get_user(self, id: int) -> User:
    pass
  
  @abstractmethod
  def get_all_users(self) -> List[User]:
    pass
  
  @abstractmethod
  def update_user(self, id: int, new_name: Optional[str], new_age: Optional[int]) -> User:
    pass

  @abstractmethod
  def delete_user(self, id: int) -> User:
    pass