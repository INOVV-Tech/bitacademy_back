from boto3.dynamodb.conditions import Attr

from src.shared.infra.external.dynamo_datasource import DynamoDatasource

from src.shared.domain.repositories.coininfo_repository_interface import ICoinInfoRepository

from src.shared.domain.entities.coininfo import CoinInfo

from src.shared.infra.external.key_formatters import encode_idx_pk

class CoinInfoRepositoryDynamo(ICoinInfoRepository):
    dynamo: DynamoDatasource
    
    @staticmethod
    def coininfo_partition_key_format(coin_info: CoinInfo) -> str:
        return f'COININFO#{coin_info.symbol}'
    
    @staticmethod
    def coininfo_partition_key_format_from_symbol(symbol: str) -> str:
        return f'COININFO#{symbol}'
    
    @staticmethod
    def coininfo_sort_key_format() -> str:
        return 'METADATA'

    @staticmethod
    def coininfo_gsi_entity_get_all_pk() -> str:
        return 'INDEX#COININFO'
    
    @staticmethod
    def coininfo_gsi_entity_get_all_sk(coin_info: CoinInfo) -> str:
        return f'DATE#{coin_info.created_at}'
    
    def __init__(self, dynamo: DynamoDatasource):
        self.dynamo = dynamo

    def create(self, coin_info: CoinInfo) -> CoinInfo:
        item = coin_info.to_dict()

        item['PK'] = self.coininfo_partition_key_format(coin_info)
        item['SK'] = self.coininfo_sort_key_format()
        item[encode_idx_pk('GSI#ENTITY_GETALL#PK')] = self.coininfo_gsi_entity_get_all_pk()
        item[encode_idx_pk('GSI#ENTITY_GETALL#SK')] = self.coininfo_gsi_entity_get_all_sk(coin_info)

        self.dynamo.put_item(item=item)

        return coin_info

    def get_all(self, symbols: list[str]) -> dict:
        filter_expression = None
        
        if len(symbols) > 0:
            filter_expression = Attr('symbol').is_in(symbols)

        response = self.dynamo.query(
            index_name='GetAllEntities',
            partition_key=self.coininfo_gsi_entity_get_all_pk(),
            limit=None,
            exclusive_start_key=None,
            filter_expression=filter_expression,
            scan_index_forward=True
        )
        
        return {
            'coins': [ CoinInfo.from_dict_static(item) for item in response['items'] ]
        }
    
    def get_one(self, symbol: str) -> CoinInfo | None:
        data = self.dynamo.get_item(
            partition_key=self.coininfo_partition_key_format_from_symbol(symbol),
            sort_key=self.coininfo_sort_key_format()
        )

        return CoinInfo.from_dict_static(data['Item']) if 'Item' in data else None