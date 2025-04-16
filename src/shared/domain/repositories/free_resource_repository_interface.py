from abc import ABC, abstractmethod

from src.shared.domain.entities.free_resource import FreeResource

class IFreeResourceRepository(ABC):
    @abstractmethod
    def create(self, free_resource: FreeResource) -> FreeResource:
        pass

    @abstractmethod
    def get_all(self) -> list[FreeResource]:
        pass
    
    @abstractmethod
    def get_one(self, title: str) -> FreeResource:
        pass

    @abstractmethod
    def update(self, free_resource: FreeResource) -> FreeResource:
        pass

    @abstractmethod
    def delete(self, free_resource: FreeResource) -> FreeResource:
        pass

