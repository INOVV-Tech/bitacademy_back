from enum import Enum

class TRADE_SIDE(Enum):
    LONG = 'LONG'
    SHORT = 'SHORT'

    @staticmethod
    def length() -> int:
        return len(TRADE_SIDE)