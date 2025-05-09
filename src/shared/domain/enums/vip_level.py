from enum import IntEnum

class VIP_LEVEL(IntEnum):
    FREE = 0
    VIP_1 = 1

    @staticmethod
    def is_vip(vip_level: 'VIP_LEVEL') -> bool:
        return vip_level.value > 0