from pydantic import BaseModel, Field

from src.shared.domain.enums.exchange import EXCHANGE
from src.shared.domain.enums.market import MARKET
from src.shared.domain.enums.trade_side import TRADE_SIDE
from src.shared.domain.enums.vip_level import VIP_LEVEL
from src.shared.domain.enums.signal_status import SIGNAL_STATUS
from src.shared.domain.enums.trade_strat import TRADE_STRAT

from src.shared.utils.decimal import Decimal
from src.shared.utils.time import now_timestamp
from src.shared.utils.entity import random_entity_id, is_valid_uuid, \
    is_valid_entity_string_enum, is_valid_entity_int_enum, is_valid_entity_string, \
    is_valid_entity_decimal

class Signal(BaseModel):
    id: str
    user_id: str
    title: str
    base_asset: str
    quote_asset: str

    exchange: EXCHANGE
    market: MARKET
    trade_side: TRADE_SIDE
    vip_level: VIP_LEVEL
    status: SIGNAL_STATUS
    trade_strat: TRADE_STRAT

    estimated_pnl: Decimal
    stake_relative: Decimal
    margin_multiplier: Decimal

    created_at: int = Field(..., gt=0, description='Timestamp in seconds')
    updated_at: int = Field(..., gt=0, description='Timestamp in seconds')

    @staticmethod
    def data_contains_valid_id(data: dict) -> bool:
        return is_valid_uuid(data, 'id', version=4)
    
    @staticmethod
    def data_contains_valid_title(data: dict) -> bool:
        return is_valid_entity_string(data, 'title', min_length=0, max_length=512)
    
    @staticmethod
    def data_contains_valid_base_asset(data: dict) -> bool:
        return is_valid_entity_string(data, 'base_asset', min_length=3, max_length=4)
    
    @staticmethod
    def data_contains_valid_quote_asset(data: dict) -> bool:
        return is_valid_entity_string(data, 'quote_asset', min_length=3, max_length=4)
    
    @staticmethod
    def data_contains_valid_exchange(data: dict) -> bool:
        return is_valid_entity_string_enum(data, 'exchange', EXCHANGE)
    
    @staticmethod
    def data_contains_valid_market(data: dict) -> bool:
        return is_valid_entity_string_enum(data, 'market', MARKET)
    
    @staticmethod
    def data_contains_valid_trade_side(data: dict) -> bool:
        return is_valid_entity_string_enum(data, 'trade_side', TRADE_SIDE)
    
    @staticmethod
    def data_contains_valid_vip_level(data: dict) -> bool:
        return is_valid_entity_int_enum(data, 'vip_level', VIP_LEVEL)
    
    @staticmethod
    def data_contains_valid_status(data: dict) -> bool:
        return is_valid_entity_string_enum(data, 'status', SIGNAL_STATUS)
    
    @staticmethod
    def data_contains_valid_trade_strat(data: dict) -> bool:
        return is_valid_entity_string_enum(data, 'trade_strat', TRADE_STRAT)
    
    @staticmethod
    def data_contains_valid_estimated_pnl(data: dict) -> bool:
        return is_valid_entity_decimal(data, 'estimated_pnl', min_value='0', max_value='100')
    
    @staticmethod
    def data_contains_valid_stake_relative(data: dict) -> bool:
        return is_valid_entity_decimal(data, 'stake_relative', min_value='0', max_value='1')

    @staticmethod
    def data_contains_valid_margin_multiplier(data: dict) -> bool:
        return is_valid_entity_decimal(data, 'margin_multiplier', min_value='1', max_value='1000')
    
    @staticmethod
    def norm_asset(asset: str) -> str:
        return asset.strip().lower()

    @staticmethod
    def from_request_data(data: dict, user_id: str) -> 'tuple[str, Signal | None]':
        if not Signal.data_contains_valid_title(data):
            return ('Título inválido', None)
        
        if not Signal.data_contains_valid_base_asset(data):
            return ('Ativo base inválido', None)
        
        if not Signal.data_contains_valid_quote_asset(data):
            return ('Ativo de cotação inválido', None)
        
        if not Signal.data_contains_valid_exchange(data):
            return ('Exchange inválida', None)
        
        if not Signal.data_contains_valid_market(data):
            return ('Mercado inválido', None)
        
        if not Signal.data_contains_valid_trade_side(data):
            return ('Direção de trade inválida', None)
        
        if not Signal.data_contains_valid_vip_level(data):
            return ('Level de VIP inválido', None)
        
        if not Signal.data_contains_valid_trade_strat(data):
            return ('Tipo de operação inválida', None)
        
        if not Signal.data_contains_valid_estimated_pnl(data):
            return ('PnL estimado inválido [0, 1]', None)
        
        if not Signal.data_contains_valid_stake_relative(data):
            return ('Stake relativo (Investimento) inválido', None)
        
        if not Signal.data_contains_valid_margin_multiplier(data):
            return ('Alavancagem inválida', None)
        
        base_asset = Signal.norm_asset(data['base_asset'])
        quote_asset = Signal.norm_asset(data['quote_asset'])

        signal = Signal(
            id=random_entity_id(),
            user_id=user_id,
            title=data['title'].strip(),
            base_asset=base_asset,
            quote_asset=quote_asset,

            exchange=EXCHANGE[data['exchange']],
            market=MARKET[data['market']],
            trade_side=TRADE_SIDE[data['trade_side']],
            vip_level=VIP_LEVEL(data['vip_level']),
            status=SIGNAL_STATUS.ENTRY_WAIT,
            trade_strat=TRADE_STRAT[data['trade_strat']],

            estimated_pnl=Decimal(data['estimated_pnl']),
            stake_relative=Decimal(data['stake_relative']),
            margin_multiplier=Decimal(data['margin_multiplier']),

            created_at=now_timestamp(),
            updated_at=now_timestamp()
        )

        if signal.market == MARKET.SPOT and signal.trade_side != TRADE_SIDE.LONG:
            return (f'Direção de trade "{signal.trade_side.value}" com mercado spot não é permitida', None)

        return ('', signal)

    @staticmethod
    def from_dict_static(data: dict) -> 'Signal':
        return Signal(
            id=data['id'],
            user_id=data['user_id'],
            title=data['title'],
            base_asset=data['base_asset'],
            quote_asset=data['quote_asset'],

            exchange=EXCHANGE[data['exchange']],
            market=MARKET[data['market']],
            trade_side=TRADE_SIDE[data['trade_side']],
            vip_level=VIP_LEVEL(data['vip_level']),
            status=SIGNAL_STATUS[data['status']],
            trade_strat=TRADE_STRAT[data['trade_strat']],

            estimated_pnl=Decimal(data['estimated_pnl']),
            stake_relative=Decimal(data['stake_relative']),
            margin_multiplier=Decimal(data['margin_multiplier']),
            
            created_at=int(data['created_at']),
            updated_at=int(data['updated_at']),
        )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'base_asset': self.base_asset,
            'quote_asset': self.quote_asset,

            'exchange': self.exchange.value,
            'market': self.market.value,
            'trade_side': self.trade_side.value,
            'vip_level': self.vip_level.value,
            'status': self.status.value,
            'trade_strat': self.trade_strat.value,

            'estimated_pnl': str(self.estimated_pnl),
            'stake_relative': str(self.stake_relative),
            'margin_multiplier': str(self.margin_multiplier),

            'created_at': self.created_at,
            'updated_at': self.updated_at,            
        }
    
    def from_dict(self, data: dict) -> 'Signal':
        return self.from_dict_static(data)
    
    def to_public_dict(self) -> dict:
        return self.to_dict()
    
    def update_from_dict(self, data: dict) -> dict:
        updated_fields = {}

        if Signal.data_contains_valid_title(data):
            self.title = data['title'].strip()

            updated_fields['title'] = self.title

        if Signal.data_contains_valid_base_asset(data):
            self.base_asset = Signal.norm_asset(data['base_asset'])

            updated_fields['base_asset'] = self.base_asset
        
        if Signal.data_contains_valid_quote_asset(data):
            self.quote_asset = Signal.norm_asset(data['quote_asset'])

            updated_fields['quote_asset'] = self.quote_asset

        if Signal.data_contains_valid_exchange(data):
            self.exchange = EXCHANGE[data['exchange']]

            updated_fields['exchange'] = self.exchange
        
        if Signal.data_contains_valid_market(data):
            self.market = MARKET[data['market']]

            updated_fields['market'] = self.market
        
        if Signal.data_contains_valid_trade_side(data):
            self.trade_side = TRADE_SIDE[data['trade_side']]

            updated_fields['trade_side'] = self.trade_side
        
        if Signal.data_contains_valid_vip_level(data):
            self.vip_level = VIP_LEVEL(data['vip_level'])

            updated_fields['vip_level'] = self.vip_level

        if Signal.data_contains_valid_trade_strat(data):
            self.trade_strat = TRADE_STRAT[data['trade_strat']]

            updated_fields['trade_strat'] = self.trade_strat
        
        if Signal.data_contains_valid_estimated_pnl(data):
            self.estimated_pnl = Decimal(data['estimated_pnl'])

            updated_fields['estimated_pnl'] = self.estimated_pnl

        if Signal.data_contains_valid_stake_relative(data):
            self.stake_relative = Decimal(data['stake_relative'])

            updated_fields['stake_relative'] = self.stake_relative

        if Signal.data_contains_valid_margin_multiplier(data):
            self.margin_multiplier = Decimal(data['margin_multiplier'])

            updated_fields['margin_multiplier'] = self.margin_multiplier

        updated_fields['any_updated'] = len(updated_fields.keys()) > 0

        return updated_fields