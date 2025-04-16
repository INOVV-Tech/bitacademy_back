from abc import ABC, abstractmethod

from domain.entities.bit_class import BitClass

class IBitClassRepository(ABC):
    @abstractmethod
    def create(self, bit_class: BitClass) -> BitClass:
        pass

    @abstractmethod
    def get_all(self) -> list[BitClass]:
        pass
    
    @abstractmethod
    def get_one(self, title: str) -> BitClass:
        pass

    @abstractmethod
    def update(self, bit_class: BitClass) -> BitClass:
        pass

    @abstractmethod
    def delete(self, bit_class: BitClass) -> BitClass:
        pass