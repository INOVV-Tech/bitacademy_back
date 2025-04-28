from enum import Enum

class EXCHANGE(Enum):
    BINANCE = 'BINANCE'
    # BYBIT = 'BYBIT'
    # BITGET = 'BITGET'
    # BINGX = 'BINGX'

    @staticmethod
    def length() -> int:
        return len(EXCHANGE)