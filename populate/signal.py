import os
import random
from populate.common import load_app_env, load_resource

load_app_env()

from src.shared.infra.repositories.repository import Repository
from src.shared.infra.repositories.dtos.auth_authorizer_dto import AuthAuthorizerDTO

from src.shared.domain.enums.role import ROLE
from src.shared.domain.enums.vip_level import VIP_LEVEL
from src.shared.domain.enums.exchange import EXCHANGE
from src.shared.domain.enums.market import MARKET
from src.shared.domain.enums.trade_side import TRADE_SIDE
from src.shared.domain.enums.trade_strat import TRADE_STRAT
from src.shared.domain.entities.signal import Signal

requester_user = AuthAuthorizerDTO(
    user_id=os.environ.get('POPULATE_USER_ID'),
    name=os.environ.get('POPULATE_USER_NAME'),
    email='',
    phone='',
    role=ROLE.ADMIN,
    email_verified=True,
    phone_verified=True,
    vip_subscription=None
)

def populate_signals():
    repository = Repository(signal_repo=True)

    base_assets = [ 'BTC', 'FUN', 'LQTY', 'SLF', 'CTK', 'ALT', 'KAIA', 'IO' ]

    signals = []

    for base_asset in base_assets:
        signals.append({
            'title': f'{base_asset}/USDT Signal',
            'base_asset': base_asset,
            'quote_asset': 'USDT',
            'exchange': random.choice(list(EXCHANGE)).value,
            'market': random.choice(list(MARKET)).value,
            'trade_side': random.choice(list(TRADE_SIDE)).value,
            'vip_level': random.choice(list(VIP_LEVEL)),
            'trade_strat': random.choice(list(TRADE_STRAT)).value,
            'estimated_pnl': '1.5',
            'stake_relative': '0.02',
            'margin_multiplier': '1',
            'price_entry_min': '93000',
            'price_entry_max': '96000',
            'price_stop': '91000',
            'price_targets': [ '97000', '98000', '100000' ],
            'external_url': 'http://www.google.com',
            'description': ''
        })

    for i in range(len(signals)):
        (error, signal) = Signal.from_request_data(signals[i], requester_user)

        repository.signal_repo.create(signal)

        print(f'Populated {(i + 1)} signal')

    print('Populated signals')