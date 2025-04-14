from domain.entities.address import Address
from domain.repositories.address_repository_interface import IAddressRepository
from infra.external.postgre_datasource import PostgreDatasource


class AddressRepositoryDb(IAddressRepository):
  def __init__(self, datasource: PostgreDatasource):
    self.datasource = datasource
    
  def create(self, address: Address) -> Address:
      item = address.to_db()

      resp = self.datasource.add_item(item)

      return Address.from_db(resp)
  
  def associate_user(self, address: Address, user_id: int) -> Address:
      item = address.to_db()

      item.user_id = user_id

      resp = self.datasource.update_item(item)

      return Address.from_db(resp)