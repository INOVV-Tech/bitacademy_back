from enum import Enum

class MARKET(Enum):
    SPOT = 'SPOT'
    FUTURES_USDT = 'FUTURES_USDT'
    FUTURES_COIN = 'FUTURES_COIN'

    @staticmethod
    def length() -> int:
        return len(MARKET)