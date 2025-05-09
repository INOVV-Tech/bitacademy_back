from pydantic import BaseModel, Field

from src.shared.domain.enums.vip_level import VIP_LEVEL

from src.shared.utils.time import now_timestamp

class VipSubscription(BaseModel):
    user_id: str
    vip_level: VIP_LEVEL
    created_at: int = Field(..., gt=0, description='Timestamp in seconds')
    expire_at: int = Field(..., gt=0, description='Timestamp in seconds')
    
    @staticmethod
    def max_vip_dummy(user_id: str) -> 'VipSubscription':
        created_at = now_timestamp()
        expire_at = created_at + 1500

        return VipSubscription(
            user_id=user_id,
            vip_level=VIP_LEVEL.VIP_1,
            created_at=created_at,
            expire_at=expire_at
        )
    
    @staticmethod
    def free_dummy(user_id: str) -> 'VipSubscription':
        created_at = now_timestamp()
        expire_at = created_at

        return VipSubscription(
            user_id=user_id,
            vip_level=VIP_LEVEL.FREE,
            created_at=created_at,
            expire_at=expire_at
        )

    @staticmethod
    def from_dict_static(data: dict) -> 'VipSubscription':
        return VipSubscription(
            user_id=data['user_id'],
            vip_level=VIP_LEVEL(data['vip_level']),
            created_at=int(data['created_at']),
            expire_at=int(data['expire_at'])
        )

    def to_dict(self) -> dict:
        return {
            'user_id': self.user_id,
            'vip_level': self.vip_level.value,
            'created_at': self.created_at,
            'expire_at': self.expire_at
        }
    
    def to_reduced_dict(self) -> dict:
        return {
            'vip_level': self.vip_level.value,
            'created_at': self.created_at,
            'expire_at': self.expire_at
        }
    
    def from_dict(self, data: dict) -> 'VipSubscription':
        return self.from_dict_static(data)
    
    def to_public_dict(self) -> dict:
        return self.to_dict()
    
    def update_from_dict(self, data: dict) -> dict:
        updated_fields = {}

        updated_fields['any_updated'] = len(updated_fields.keys()) > 0

        return updated_fields
    
    def expired(self) -> bool:
        return now_timestamp() >= self.expire_at
    
    def restrict_access(self, vip_level: VIP_LEVEL | None) -> VIP_LEVEL:
        if vip_level is None:
            return self.vip_level
        
        return VIP_LEVEL(min(self.vip_level.value, vip_level.value))
    
    def can_access(self, vip_level: VIP_LEVEL) -> bool:
        return self.vip_level.value >= vip_level.value