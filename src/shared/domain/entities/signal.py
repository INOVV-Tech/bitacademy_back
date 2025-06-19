from pydantic import BaseModel, ConfigDict, Field

from src.shared.infra.repositories.dtos.auth_authorizer_dto import AuthAuthorizerDTO

from src.shared.domain.enums.role import ROLE
from src.shared.domain.enums.exchange import EXCHANGE
from src.shared.domain.enums.market import MARKET
from src.shared.domain.enums.trade_side import TRADE_SIDE
from src.shared.domain.enums.vip_level import VIP_LEVEL
from src.shared.domain.enums.signal_status import SIGNAL_STATUS
from src.shared.domain.enums.trade_strat import TRADE_STRAT

from src.shared.utils.decimal import Decimal
from src.shared.utils.time import now_timestamp
from src.shared.utils.entity import random_entity_id, is_valid_entity_uuid, \
    is_valid_entity_string_enum, is_valid_entity_int_enum, is_valid_entity_string, \
    is_valid_entity_decimal, is_valid_entity_url, is_valid_entity_list

class PriceSnapshot:
    @staticmethod
    def from_exchange(price: Decimal) -> 'PriceSnapshot':
        return PriceSnapshot(price, timestamp=now_timestamp())

    @staticmethod
    def from_dict_static(data: dict) -> 'PriceSnapshot':
        return PriceSnapshot(
            price=Decimal(data['price']) if ('price' in data and data['price'] is not None) else None,
            timestamp=int(data['timestamp']) if ('timestamp' in data and data['timestamp'] is not None) else None
        )

    def __init__(self, price: Decimal | None = None, timestamp: int | None = None):
        self.price = price
        self.timestamp = timestamp

    def to_dict(self, raw_decimal=True) -> dict:
        price = None

        if self.price is not None:
            price = self.price if raw_decimal else str(self.price)
        
        return {
            'price': price,
            'timestamp': self.timestamp
        }
    
    def priced(self) -> bool:
        return self.price is not None

class StatusDetails:
    @staticmethod
    def from_dict_static(data: dict) -> 'StatusDetails':
        def decode_price_snapshot(field_key: str) -> PriceSnapshot | None:
            return PriceSnapshot.from_dict_static(data[field_key]) if (field_key in data and data[field_key] is not None) else None

        return StatusDetails(
            entry_snapshot=decode_price_snapshot('entry_snapshot'),
            stop_snapshot=decode_price_snapshot('stop_snapshot'),
            hit_target_snapshots=[ PriceSnapshot.from_dict_static(x) for x in data['hit_target_snapshots'] ],
        )

    def __init__(self,
        entry_snapshot: PriceSnapshot | None = None,
        stop_snapshot: PriceSnapshot | None = None,
        hit_target_snapshots: list[PriceSnapshot] = []
    ):
        self.entry_snapshot = entry_snapshot
        self.stop_snapshot = stop_snapshot
        self.hit_target_snapshots = hit_target_snapshots

    def to_dict(self, raw_decimal=True) -> dict:
        return {
            'entry_snapshot': self.entry_snapshot.to_dict(raw_decimal=raw_decimal) if self.entry_snapshot is not None else None,
            'stop_snapshot': self.stop_snapshot.to_dict(raw_decimal=raw_decimal) if self.stop_snapshot is not None else None,
            'hit_target_snapshots': [ x.to_dict(raw_decimal=raw_decimal) for x in self.hit_target_snapshots ]
        }

class Signal(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: str
    user_id: str
    user_name: str
    user_role: ROLE
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
    price_entry_min: Decimal
    price_entry_max: Decimal
    price_stop: Decimal
    price_targets: list[Decimal]
    status_details: StatusDetails
    created_at: int = Field(..., gt=0, description='Timestamp in seconds')
    updated_at: int = Field(..., gt=0, description='Timestamp in seconds')
    external_url: str
    description: str

    @staticmethod
    def data_contains_valid_id(data: dict) -> bool:
        return is_valid_entity_uuid(data, 'id', version=4)
    
    @staticmethod
    def data_contains_valid_title(data: dict) -> bool:
        return is_valid_entity_string(data, 'title', min_length=0, max_length=512)
    
    @staticmethod
    def data_contains_valid_base_asset(data: dict) -> bool:
        return is_valid_entity_string(data, 'base_asset', min_length=1, max_length=4)
    
    @staticmethod
    def data_contains_valid_quote_asset(data: dict) -> bool:
        return is_valid_entity_string(data, 'quote_asset', min_length=2, max_length=4)
    
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
    def data_contains_valid_price(data: dict, price_key: str) -> bool:
        return is_valid_entity_decimal(data, price_key, min_value='0', max_value='999_999_999_999')
    
    @staticmethod
    def data_contains_valid_price_targets(data: dict) -> bool:
        if not is_valid_entity_list(data, 'price_targets', min_length=1, max_length=9):
            return False
        
        min_value = Decimal('0')
        max_value = Decimal('999_999_999_999')

        try:
            for item in data['price_targets']:
                if not isinstance(item, str):
                    return False
                
                value = Decimal(item)

                if value < min_value or value > max_value:
                    return False
        except:
            return False

        return True
    
    @staticmethod
    def data_contains_valid_external_url(data: dict) -> bool:
        return is_valid_entity_url(data, 'external_url')
    
    @staticmethod
    def data_contains_valid_description(data: dict) -> bool:
        return is_valid_entity_string(data, 'description', min_length=0, max_length=2048)
    
    @staticmethod
    def norm_asset(asset: str) -> str:
        return asset.strip().lower()
    
    @staticmethod
    def from_request_data(data: dict, requester_user: AuthAuthorizerDTO) -> 'tuple[str, Signal | None]':
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

        if not Signal.data_contains_valid_price(data, 'price_entry_min'):
            return ('Preço de entrada mínimo inválido', None)
        
        if not Signal.data_contains_valid_price(data, 'price_entry_max'):
            return ('Preço de entrada máximo inválido', None)
        
        if not Signal.data_contains_valid_price(data, 'price_stop'):
            return ('Preço de stop-loss inválido', None)
        
        if not Signal.data_contains_valid_price_targets(data):
            return ('Lista de preços alvos inválida', None)
        
        if not Signal.data_contains_valid_external_url(data):
            return ('Link externo inválido', None)
        
        if not Signal.data_contains_valid_description(data):
            return ('Descrição inválida', None)

        base_asset = Signal.norm_asset(data['base_asset'])
        quote_asset = Signal.norm_asset(data['quote_asset'])

        status = SIGNAL_STATUS.ENTRY_WAIT

        price_entry_min = Decimal(data['price_entry_min'])
        price_entry_max = Decimal(data['price_entry_max'])

        if price_entry_min == price_entry_max:
            status = SIGNAL_STATUS.RUNNING

        signal = Signal(
            id=random_entity_id(),
            user_id=requester_user.user_id,
            user_name=requester_user.name,
            user_role=requester_user.role,
            title=data['title'].strip(),
            base_asset=base_asset,
            quote_asset=quote_asset,
            exchange=EXCHANGE[data['exchange']],
            market=MARKET[data['market']],
            trade_side=TRADE_SIDE[data['trade_side']],
            vip_level=VIP_LEVEL(data['vip_level']),
            status=status,
            trade_strat=TRADE_STRAT[data['trade_strat']],
            estimated_pnl=Decimal(data['estimated_pnl']),
            stake_relative=Decimal(data['stake_relative']),
            margin_multiplier=Decimal(data['margin_multiplier']),
            price_entry_min=price_entry_min,
            price_entry_max=price_entry_max,
            price_stop=Decimal(data['price_stop']),
            price_targets=[ Decimal(x) for x in data['price_targets'] ],
            status_details=StatusDetails(
                hit_target_snapshots=[ PriceSnapshot() for x in data['price_targets'] ]
            ),
            created_at=now_timestamp(),
            updated_at=now_timestamp(),
            external_url=data['external_url'].strip(),
            description=data['description'].strip()
        )

        return ('', signal)

    @staticmethod
    def from_dict_static(data: dict) -> 'Signal':
        return Signal(
            id=data['id'],
            user_id=data['user_id'],
            user_name=data['user_name'],
            user_role=ROLE[data['user_role']],
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
            price_entry_min=Decimal(data['price_entry_min']),
            price_entry_max=Decimal(data['price_entry_max']),
            price_stop=Decimal(data['price_stop']),
            price_targets=[ Decimal(x) for x in data['price_targets'] ],
            status_details=StatusDetails.from_dict_static(data['status_details']),
            created_at=int(data['created_at']),
            updated_at=int(data['updated_at']),
            external_url=data['external_url'],
            description=data['description']
        )

    def to_dict(self, raw_decimal=True) -> dict:
        def dump_decimal(value: Decimal) -> Decimal | str:
            return value if raw_decimal else str(value)

        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_name': self.user_name,
            'user_role': self.user_role.value,
            'title': self.title,
            'base_asset': self.base_asset,
            'quote_asset': self.quote_asset,
            'exchange': self.exchange.value,
            'market': self.market.value,
            'trade_side': self.trade_side.value,
            'vip_level': self.vip_level.value,
            'status': self.status.value,
            'trade_strat': self.trade_strat.value,
            'estimated_pnl': dump_decimal(self.estimated_pnl),
            'stake_relative': dump_decimal(self.stake_relative),
            'margin_multiplier': dump_decimal(self.margin_multiplier),
            'price_entry_min': dump_decimal(self.price_entry_min),
            'price_entry_max': dump_decimal(self.price_entry_max),
            'price_stop': dump_decimal(self.price_stop),
            'price_targets': [ dump_decimal(x) for x in self.price_targets ],
            'status_details': self.status_details.to_dict(raw_decimal=raw_decimal),
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'external_url': self.external_url,
            'description': self.description         
        }
    
    def from_dict(self, data: dict) -> 'Signal':
        return self.from_dict_static(data)
    
    def to_public_dict(self) -> dict:
        result = self.to_dict(raw_decimal=False)

        del result['user_id']

        return result
    
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

        if Signal.data_contains_valid_price(data, 'price_entry_min'):
            self.price_entry_min = Decimal(data['price_entry_min'])

            updated_fields['price_entry_min'] = self.price_entry_min

        if Signal.data_contains_valid_price(data, 'price_entry_max'):
            self.price_entry_max = Decimal(data['price_entry_max'])

            updated_fields['price_entry_max'] = self.price_entry_max

        if Signal.data_contains_valid_price(data, 'price_stop'):
            self.price_stop = Decimal(data['price_stop'])

            updated_fields['price_stop'] = self.price_stop

        if Signal.data_contains_valid_price_targets(data):
            self.price_targets = [ Decimal(x) for x in data['price_targets'] ]

            updated_fields['price_targets'] = self.price_targets

            self.status_details = StatusDetails(
                hit_target_snapshots=[ PriceSnapshot() for x in self.price_targets ]
            )

        if Signal.data_contains_valid_external_url(data):
            self.external_url = data['external_url'].strip()

            updated_fields['external_url'] = self.external_url
        
        if Signal.data_contains_valid_description(data):
            self.description = data['description'].strip()

            updated_fields['description'] = self.description

        updated_fields['any_updated'] = len(updated_fields.keys()) > 0

        return updated_fields
    
    def get_binance_symbol(self) -> str:
        symbol = f'{self.base_asset.upper()}{self.quote_asset.upper()}'

        if self.market == MARKET.SPOT or self.market == MARKET.FUTURES_USDT:
            return symbol
        
        return symbol + '_PERP'
    
    def get_symbol(self) -> str:
        return self.get_binance_symbol()