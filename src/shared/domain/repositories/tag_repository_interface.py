from abc import ABC, abstractmethod

from src.shared.domain.entities.tag import Tag

class ITagRepository(ABC):
    @abstractmethod
    def create(self, tag: Tag) -> Tag:
        pass
    
    @abstractmethod
    def get_all(self, title: str = '', limit: int = 10, last_evaluated_key: dict | None = None, \
        sort_order: str = 'desc') -> dict:
        pass