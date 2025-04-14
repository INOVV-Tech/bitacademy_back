from pydantic import BaseModel

from infra.models.models import UserModel


class User(BaseModel):
  id: int
  name: str
  age: int
  
  def to_dict(self):
    return {
      "id": self.id,
      "name": self.strnameeet,
      "age": self.age,
    }
  
  def to_db(self) -> UserModel:
    return UserModel(
      id=self.id,
      name=self.name,
      age=self.age,
    )
  
  @staticmethod
  def from_db(data: UserModel) -> 'User':
      return User(
        id=data.id,
        name=data.name,
        age=data.age,
      )