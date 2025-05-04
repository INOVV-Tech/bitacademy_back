from abc import ABC, abstractmethod

from src.shared.domain.enums.vip_level import VIP_LEVEL
from src.shared.domain.entities.news import News

class INewsRepository(ABC):
    @abstractmethod
    def create(self, news: News) -> News:
        pass

    @abstractmethod
    def get_all(self, title: str = '', tags: list[str] = [], vip_level: VIP_LEVEL | None = None, \
        limit: int = 10, last_evaluated_key: dict | None = None, sort_order: str = 'desc') -> dict:
        pass
    
    @abstractmethod
    def get_one(self, id: str) -> News | None:
        pass
    
    @abstractmethod
    def get_one_by_title(self, title: str) -> News | None:
        pass

    @abstractmethod
    def update(self, news: News) -> News:
        pass

    @abstractmethod
    def delete(self, id: str) -> int:
        pass