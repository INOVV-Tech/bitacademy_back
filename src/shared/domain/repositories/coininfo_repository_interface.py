from abc import ABC, abstractmethod

from src.shared.domain.entities.coininfo import CoinInfo

class ICoinInfoRepository(ABC):
    @abstractmethod
    def create(self, coin_info: CoinInfo) -> CoinInfo:
        pass
    
    @abstractmethod
    def get_all(self, symbols: list[str]) -> dict:
        pass