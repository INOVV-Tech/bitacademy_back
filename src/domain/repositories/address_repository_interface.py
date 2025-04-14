from abc import ABC, abstractmethod

from domain.entities.address import Address

class IAddressRepository(ABC):
  @abstractmethod
  def create(self, address: Address) -> Address:
    pass
  
  @abstractmethod
  def associate_user(self, address: Address, user_id: int) -> Address:
    pass