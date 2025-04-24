from abc import ABC, abstractmethod

from src.shared.domain.enums.vip_level import VIP_LEVEL
from src.shared.domain.entities.course import Course

class ICourseRepository(ABC):
    @abstractmethod
    def create(self, course: Course) -> Course:
        pass

    @abstractmethod
    def get_all(self, tags: list[str] = [], vip_level: VIP_LEVEL | None = None, \
        limit: int = 10, last_evaluated_key: str = '', sort_order: str = 'desc') -> dict:
        pass
    
    @abstractmethod
    def get_one(self, id: str) -> Course | None:
        pass
    
    @abstractmethod
    def get_one_by_title(self, title: str) -> Course | None:
        pass

    @abstractmethod
    def update(self, course: Course) -> Course:
        pass

    @abstractmethod
    def delete(self, id: str) -> Course | None:
        pass