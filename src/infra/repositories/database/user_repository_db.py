
from typing import List, Optional
from domain.entities.user import User
from domain.repositories.user_repository_interface import IUserRepository
from infra.external.postgre_datasource import PostgreDatasource
from infra.models.models import UserModel


class UserRepositoryDb(IUserRepository):
  def __init__(self, datasource: PostgreDatasource):
    self.datasource = datasource
    
  def insert_user(self, user: User) -> User:
    item = user.to_db()

    resp = self.datasource.add_item(item)
        
    return User.from_db(resp)

  def get_user(self, id: int) -> User:
    print(id)
    item = self.datasource.get_item(UserModel, id)
    
    if item is None:
      return None

    return User.from_db(item)
  
  def get_all_users(self) -> List[User]:
    items = self.datasource.get_all_items(UserModel)

    return [User.from_db(item) for item in items]

  def update_user(self, id: int, new_name: Optional[str], new_age: Optional[int]) -> User:
    item = self.datasource.get_item(UserModel, id)

    item.name = new_name
    item.age = new_age

    resp = self.datasource.update_item(item)

    return User.from_db(resp)

  def delete_user(self, id: int) -> User:
    item = self.datasource.get_item(UserModel, id)

    resp = self.datasource.delete_item(UserModel, id)

    return User.from_db(resp)
  
  def get_user_by_filters(self, filters: dict) -> List[User]:
    items = self.datasource.query(UserModel, **filters)

    return [User.from_db(item) for item in items]
