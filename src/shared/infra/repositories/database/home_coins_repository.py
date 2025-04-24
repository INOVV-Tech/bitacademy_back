from src.shared.infra.external.dynamo_datasource import DynamoDatasource

from src.shared.domain.repositories.home_coins_repository_interface import IHomeCoinsRepository

from src.shared.domain.entities.home_coins import HomeCoins

class HomeCoinsRepositoryDynamo(IHomeCoinsRepository):
    dynamo: DynamoDatasource
    
    @staticmethod
    def home_coins_partition_key_format() -> str:
        return f'HOME_COINS'
    
    @staticmethod
    def home_coins_sort_key_format() -> str:
        return 'METADATA'
    
    def __init__(self, dynamo: DynamoDatasource):
        self.dynamo = dynamo

    def update(self, home_coins: HomeCoins) -> HomeCoins:
        item = home_coins.to_dict()

        item['PK'] = self.home_coins_partition_key_format()
        item['SK'] = self.home_coins_sort_key_format()

        self.dynamo.put_item(item=item)

        return home_coins
    
    def get(self) -> HomeCoins | None:
        data = self.dynamo.get_item(
            partition_key=self.home_coins_partition_key_format(),
            sort_key=self.home_coins_sort_key_format()
        )

        return HomeCoins.from_dict_static(data['Item']) if 'Item' in data else None