from abc import ABC, abstractmethod

from src.shared.domain.entities.vip_subscription import VipSubscription

class IVipSubscriptionRepository(ABC):
    @abstractmethod
    def create(self, vip_subscription: VipSubscription) -> VipSubscription:
        pass

    @abstractmethod
    def get_all(self, user_ids: list[str] = [], limit: int = 10, \
        last_evaluated_key: dict | None = None, sort_order: str = 'desc') -> dict:
        pass
    
    @abstractmethod
    def get_one(self, user_id: str) -> VipSubscription | None:
        pass

    @abstractmethod
    def update(self, vip_subscription: VipSubscription) -> VipSubscription:
        pass

    @abstractmethod
    def delete(self, user_id: str) -> int:
        pass