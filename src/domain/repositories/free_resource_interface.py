from abc import ABC, abstractmethod

from domain.entities.free_resource import FreeResource

class IFreeResourceRepository(ABC):
    @abstractmethod
    def create(self, free_resource: FreeResource) -> FreeResource:
        pass
    
    @abstractmethod
    def get_by_title(self, title: str) -> FreeResource:
        pass

    @abstractmethod
    def get_all(self) -> list[FreeResource]:
        pass