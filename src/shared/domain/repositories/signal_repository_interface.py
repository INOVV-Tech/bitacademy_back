from abc import ABC, abstractmethod

from src.shared.domain.enums.exchange import EXCHANGE
from src.shared.domain.enums.market import MARKET
from src.shared.domain.enums.trade_side import TRADE_SIDE
from src.shared.domain.enums.signal_status import SIGNAL_STATUS
from src.shared.domain.enums.vip_level import VIP_LEVEL
from src.shared.domain.enums.trade_strat import TRADE_STRAT
from src.shared.domain.entities.signal import Signal

class ISignalRepository(ABC):
    @abstractmethod
    def create(self, signal: Signal) -> Signal:
        pass

    @abstractmethod
    def get_all(self,
        title: str = '',
        base_asset: str = '',
        exchanges: list[EXCHANGE] = [],
        markets: list[MARKET] = [],
        trade_sides: list[TRADE_SIDE] = [],
        signal_status: list[SIGNAL_STATUS] = [],
        vip_level: VIP_LEVEL | None = None,
        trade_strats: list[TRADE_STRAT] = [],
        limit: int = 10, last_evaluated_key: dict | None = None, sort_order: str = 'desc') -> dict:
        pass
    
    @abstractmethod
    def get_one(self, id: str) -> Signal | None:
        pass

    @abstractmethod
    def update(self, signal: Signal) -> Signal:
        pass

    @abstractmethod
    def delete(self, id: str) -> int:
        pass