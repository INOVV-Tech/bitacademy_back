from abc import abstractmethod
from domain.entities.address import Address
from domain.repositories.address_repository_interface import IAddressRepository


class AddressRepositoryMock(IAddressRepository):
    
    def create(self, address: Address) -> Address:
        pass

    def associate_user(self, address: Address, user_id: int) -> Address:
        pass