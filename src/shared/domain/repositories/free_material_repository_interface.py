from abc import ABC, abstractmethod

from src.shared.domain.entities.free_material import FreeMaterial

class IFreeMaterialRepository(ABC):
    @abstractmethod
    def create(self, free_material: FreeMaterial) -> FreeMaterial:
        pass

    @abstractmethod
    def get_all(self, title: str = '', tags: list[str] = [], limit: int = 10, last_evaluated_key: str = '', \
        sort_order: str = 'desc') -> dict:
        pass
    
    @abstractmethod
    def get_one(self, id: str) -> FreeMaterial | None:
        pass
    
    @abstractmethod
    def get_one_by_title(self, title: str) -> FreeMaterial | None:
        pass

    @abstractmethod
    def update(self, free_material: FreeMaterial) -> FreeMaterial:
        pass

    @abstractmethod
    def delete(self, id: str) -> FreeMaterial | None:
        pass

