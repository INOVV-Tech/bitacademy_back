from typing import Optional

from pydantic import BaseModel

from infra.models.models import AddressModel


class Address(BaseModel):
  id: int
  street: str
  number: str
  city: str
  state: str
  user_id: Optional[int]
  
  def to_dict(self):
    return {
      "id": self.id,
      "street": self.street,
      "number": self.number,
      "city": self.city,
      "state": self.state,
      "user_id": self.user_id
    }
  
  def to_db(self) -> AddressModel:
    return AddressModel(
      id=self.id,
      street=self.street,
      number=self.number,
      city=self.city,
      state=self.state,
      user_id=self.user_id
    )
  
  @staticmethod
  def from_db(data: AddressModel) -> 'Address':
      return Address(
        id=data.id,
        street=data.street,
        number=data.number,
        city=data.city,
        state=data.state,
        user_id=data.user_id
      )
  