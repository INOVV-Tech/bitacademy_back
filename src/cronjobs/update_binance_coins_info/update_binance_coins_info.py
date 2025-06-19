from src.shared.infra.repositories.repository import Repository

from src.shared.coinmarketcap.api import CMCApi
from src.shared.binance.api import BinanceApi

from src.shared.domain.entities.coininfo import CoinInfo

from src.shared.utils.time import now_timestamp

class Controller:
    @staticmethod
    def execute() -> dict:
        try:
            return Usecase().execute()
        except:
            return { 'error': 'Erro interno de servidor' }
        
class Usecase:
    repository: Repository
    cmc_api: CMCApi
    binance_api: BinanceApi
    
    def __init__(self):
        self.repository = Repository(coin_info_repo=True)
        self.cmc_api = CMCApi()
        self.binance_api = BinanceApi()

    def execute(self) -> dict:
        binance_spot_coins = self.binance_api.get_all_spot_coins(timeout_secs=10)
        binance_futures_usdt_coins = self.binance_api.get_all_futures_usdt_coins(timeout_secs=10)

        coins_on_binance = binance_spot_coins | binance_futures_usdt_coins

        cmc_coins = self.cmc_api.get_all_coins(timeout_secs=10)

        coin_info_dict: dict[str, CoinInfo] = {}

        for cmc_coin in cmc_coins.coins:
            if cmc_coin.symbol not in coins_on_binance:
                continue

            if len(cmc_coin.symbol) < 2:
                continue

            if cmc_coin.symbol in coin_info_dict:
                collision = coin_info_dict[cmc_coin.symbol]
                
                if float(cmc_coin.market_cap) <= float(collision.market_cap):
                    continue
            
            coin_info = CoinInfo(
                name=cmc_coin.name,
                symbol=cmc_coin.symbol,
                slug=cmc_coin.slug,
                num_market_pairs=cmc_coin.num_market_pairs,
                cmc_id=cmc_coin.cmc_id,
                total_supply=cmc_coin.total_supply,
                circulating_supply=cmc_coin.circulating_supply,
                market_cap=cmc_coin.market_cap,
                created_at=now_timestamp()
            )

            coin_info_dict[coin_info.symbol] = coin_info

        coin_info_list = list(coin_info_dict.values())

        count = 0

        for coin_info in coin_info_list:
            self.repository.coin_info_repo.create(coin_info)

            count += 1

            print(f'Symbol = {coin_info.symbol}, Name = {coin_info.name}, Slug = {coin_info.slug} [{count}/{len(coin_info_list)}]')

        return {}

def lambda_handler(event, context) -> dict:
    return Controller.execute()