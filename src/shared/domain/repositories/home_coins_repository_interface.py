from abc import ABC, abstractmethod

from src.shared.domain.entities.home_coins import HomeCoins

class IHomeCoinsRepository(ABC):
    @abstractmethod
    def update(self, home_coins: HomeCoins) -> HomeCoins:
        pass

    @abstractmethod
    def get(self) -> HomeCoins | None:
        pass

