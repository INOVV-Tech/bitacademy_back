from boto3.dynamodb.conditions import Attr

from src.shared.infra.external.dynamo_datasource import DynamoDatasource

from src.shared.domain.repositories.signal_repository_interface import ISignalRepository

from src.shared.domain.enums.exchange import EXCHANGE
from src.shared.domain.enums.market import MARKET
from src.shared.domain.enums.trade_side import TRADE_SIDE
from src.shared.domain.enums.signal_status import SIGNAL_STATUS
from src.shared.domain.enums.vip_level import VIP_LEVEL
from src.shared.domain.enums.trade_strat import TRADE_STRAT
from src.shared.domain.entities.signal import Signal

from src.shared.infra.external.key_formatters import encode_idx_pk

from src.shared.utils.time import now_timestamp

class SignalRepositoryDynamo(ISignalRepository):
    dynamo: DynamoDatasource
    
    @staticmethod
    def signal_partition_key_format(signal: Signal) -> str:
        return f'SIGNAL#{signal.id}'
    
    @staticmethod
    def signal_partition_key_format_from_id(id: str) -> str:
        return f'SIGNAL#{id}'
    
    @staticmethod
    def signal_sort_key_format() -> str:
        return 'METADATA'
    
    @staticmethod
    def signal_gsi_entity_get_all_pk() -> str:
        return 'INDEX#SIGNAL'
    
    @staticmethod
    def signal_gsi_entity_get_all_sk(signal: Signal) -> str:
        return f'DATE#{signal.created_at}'
    
    def __init__(self, dynamo: DynamoDatasource):
        self.dynamo = dynamo

    def create(self, signal: Signal) -> Signal:
        item = signal.to_dict()

        item['PK'] = self.signal_partition_key_format(signal)
        item['SK'] = self.signal_sort_key_format()
        item[encode_idx_pk('GSI#ENTITY_GETALL#PK')] = self.signal_gsi_entity_get_all_pk()
        item[encode_idx_pk('GSI#ENTITY_GETALL#SK')] = self.signal_gsi_entity_get_all_sk(signal)

        self.dynamo.put_item(item=item)

        return signal
    
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
        filter_expressions = []

        if title != '':
            filter_expressions.append(Attr('title').contains(title))

        if base_asset != '':
            filter_expressions.append(Attr('base_asset').eq(base_asset))
        
        if len(exchanges) > 0:
            exchange_filter_expression = None

            for exchange in exchanges:
                if exchange_filter_expression is None:
                    exchange_filter_expression = Attr('exchange').eq(exchange.value)
                else:
                    exchange_filter_expression |= Attr('exchange').eq(exchange.value)

            filter_expressions.append(exchange_filter_expression)

        if len(markets) > 0:
            market_filter_expression = None

            for market in markets:
                if market_filter_expression is None:
                    market_filter_expression = Attr('market').eq(market.value)
                else:
                    market_filter_expression |= Attr('market').eq(market.value)

            filter_expressions.append(market_filter_expression)

        if len(trade_sides) > 0:
            trade_side_filter_expression = None

            for trade_side in trade_sides:
                if trade_side_filter_expression is None:
                    trade_side_filter_expression = Attr('trade_side').eq(trade_side.value)
                else:
                    trade_side_filter_expression |= Attr('trade_side').eq(trade_side.value)

            filter_expressions.append(trade_side_filter_expression)

        if len(signal_status) > 0:
            status_filter_expression = None

            for status in signal_status:
                if status_filter_expression is None:
                    status_filter_expression = Attr('status').eq(status.value)
                else:
                    status_filter_expression |= Attr('status').eq(status.value)

            filter_expressions.append(status_filter_expression)

        if vip_level is not None:
            filter_expressions.append(Attr('vip_level').lte(vip_level.value))

        if len(trade_strats) > 0:
            trade_strat_filter_expression = None

            for trade_strat in trade_strats:
                if trade_strat_filter_expression is None:
                    trade_strat_filter_expression = Attr('trade_strat').eq(trade_strat.value)
                else:
                    trade_strat_filter_expression |= Attr('trade_strat').eq(trade_strat.value)

            filter_expressions.append(trade_strat_filter_expression)

        filter_expression = None

        if len(filter_expressions) > 0:
            for f_exp in filter_expressions:
                if filter_expression is None:
                    filter_expression = f_exp
                else:
                    filter_expression &= f_exp

        response = self.dynamo.query(
            index_name='GetAllEntities',
            partition_key=self.signal_gsi_entity_get_all_pk(),
            limit=limit,
            exclusive_start_key=last_evaluated_key if last_evaluated_key != '' else None,
            filter_expression=filter_expression,
            scan_index_forward=False if sort_order == 'desc' else True
        )

        count_response = self.dynamo.count(
            index_name='GetAllEntities',
            partition_key=self.signal_gsi_entity_get_all_pk(),
            filter_expression=filter_expression,
        )
        
        return {
            'signals': [ Signal.from_dict_static(item) for item in response['items'] ],
            'last_evaluated_key': response.get('last_evaluated_key'),
            'total': count_response['count']
        }
    
    def get_one(self, id: str) -> Signal | None:
        data = self.dynamo.get_item(
            partition_key=self.signal_partition_key_format_from_id(id),
            sort_key=self.signal_sort_key_format()
        )

        return Signal.from_dict_static(data['Item']) if 'Item' in data else None

    def update(self, signal: Signal) -> Signal:
        signal.updated_at = now_timestamp()

        item = signal.to_dict()

        item['PK'] = self.signal_partition_key_format(signal)
        item['SK'] = self.signal_sort_key_format()
        item[encode_idx_pk('GSI#ENTITY_GETALL#PK')] = self.signal_gsi_entity_get_all_pk()
        item[encode_idx_pk('GSI#ENTITY_GETALL#SK')] = self.signal_gsi_entity_get_all_sk(signal)

        self.dynamo.put_item(item=item)
        
        return signal
    
    def delete(self, id: str) -> int:
        resp = self.dynamo.delete_item(
            partition_key=self.signal_partition_key_format_from_id(id),
            sort_key=self.signal_sort_key_format()
        )

        return resp['ResponseMetadata']['HTTPStatusCode']