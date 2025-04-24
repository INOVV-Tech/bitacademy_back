from abc import ABC, abstractmethod

from src.shared.domain.entities.tool import Tool

class IToolRepository(ABC):
    @abstractmethod
    def create(self, tool: Tool) -> Tool:
        pass

    @abstractmethod
    def get_all(self, tags: list[str] = [], limit: int = 10, \
        last_evaluated_key: str = '', sort_order: str = 'desc') -> dict:
        pass
    
    @abstractmethod
    def get_one(self, id: str) -> Tool | None:
        pass
    
    @abstractmethod
    def get_one_by_title(self, title: str) -> Tool | None:
        pass

    @abstractmethod
    def update(self, tool: Tool) -> Tool:
        pass

    @abstractmethod
    def delete(self, id: str) -> Tool | None:
        pass