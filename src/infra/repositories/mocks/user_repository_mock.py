from typing import List, Optional
from domain.entities.user import User
from domain.repositories.user_repository_interface import IUserRepository


class UserRepositoryMock(IUserRepository):

  def insert_user(self, user: User) -> User:
    pass
  
  def get_user(self, id: int) -> User:
    pass
  
  def get_all_users(self) -> List[User]:
    pass
  
  def update_user(self, id: int, new_name: Optional[str], new_age: Optional[int]) -> User:
    pass

  def delete_user(self, id: int) -> User:
    pass