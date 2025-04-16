from abc import ABC, abstractmethod

from src.shared.domain.enums.vip_level import VIP_LEVEL
from src.shared.domain.entities.bit_class import BitClass

class IBitClassRepository(ABC):
    @abstractmethod
    def create(self, bit_class: BitClass) -> BitClass:
        pass

    @abstractmethod
    def get_all(self, tags: list[str] = [], vip_level: VIP_LEVEL | None = None, \
        limit: int = 10, last_evaluated_key: str = '') -> dict:
        pass
    
    @abstractmethod
    def get_one(self, id: str) -> BitClass | None:
        pass
    
    @abstractmethod
    def get_one_by_title(self, title: str) -> BitClass | None:
        pass

    @abstractmethod
    def update(self, bit_class: BitClass) -> BitClass:
        pass

    @abstractmethod
    def delete(self, id: str) -> BitClass | None:
        pass