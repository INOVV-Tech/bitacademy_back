from enum import Enum

class TRADE_STRAT(Enum):
    SWING = 'SWING'
    SCALPING = 'SCALPING'
    DAY_TRADING = 'DAY_TRADING'

    @staticmethod
    def length() -> int:
        return len(TRADE_STRAT)