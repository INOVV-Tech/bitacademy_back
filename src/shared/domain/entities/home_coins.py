from pydantic import BaseModel, Field, ConfigDict

class CoinInfo:
    name: str
    symbol: str
    slug: str
    num_market_pairs: int
    cmc_id: int
    total_supply: str
    circulating_supply: str
    market_cap: str
    price: str
    volume_24h: str
    volume_change: str
    percent_change_1h: str
    percent_change_24h: str
    percent_change_7d: str
    percent_change_30d: str
    percent_change_60d: str
    percent_change_90d: str

    @staticmethod
    def from_cmc_request(data: dict) -> 'CoinInfo':
        quote_USD = data['quote']['USD']

        return CoinInfo(
            name=data['name'],
            symbol=data['symbol'],
            slug=data['slug'],
            num_market_pairs=data['num_market_pairs'],
            cmc_id=data['id'],
            total_supply=str(data['total_supply']),
            circulating_supply=str(data['circulating_supply']),
            market_cap=str(quote_USD['market_cap']),
            price=str(quote_USD['price']),
            volume_24h=str(quote_USD['volume_24h']),
            volume_change=str(quote_USD['volume_change']),
            percent_change_1h=str(quote_USD['percent_change_1h']),
            percent_change_24h=str(quote_USD['percent_change_24h']),
            percent_change_7d=str(quote_USD['percent_change_7d']),
            percent_change_30d=str(quote_USD['percent_change_30d']),
            percent_change_60d=str(quote_USD['percent_change_60d']),
            percent_change_90d=str(quote_USD['percent_change_90d'])
        )
    
    @staticmethod
    def from_static_dict(data: dict) -> 'CoinInfo':
        return CoinInfo(
            name=data['name'],
            symbol=data['symbol'],
            slug=data['slug'],
            num_market_pairs=data['num_market_pairs'],
            cmc_id=data['id'],
            total_supply=data['total_supply'],
            circulating_supply=data['circulating_supply'],
            market_cap=data['market_cap'],
            price=data['price'],
            volume_24h=data['volume_24h'],
            volume_change=data['volume_change'],
            percent_change_1h=data['percent_change_1h'],
            percent_change_24h=data['percent_change_24h'],
            percent_change_7d=data['percent_change_7d'],
            percent_change_30d=data['percent_change_30d'],
            percent_change_60d=data['percent_change_60d'],
            percent_change_90d=data['percent_change_90d']
        )

    def __init__(self):
        pass

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'symbol': self.symbol,
            'slug': self.slug,
            'num_market_pairs': self.num_market_pairs,
            'cmc_id': self.cmc_id,
            'total_supply': self.total_supply,
            'circulating_supply': self.circulating_supply,
            'market_cap': self.market_cap,
            'price': self.price,
            'volume_24h': self.volume_24h,
            'volume_change': self.volume_change,
            'percent_change_1h': self.percent_change_1h,
            'percent_change_24h': self.percent_change_24h,
            'percent_change_7d': self.percent_change_7d,
            'percent_change_30d': self.percent_change_30d,
            'percent_change_60d': self.percent_change_60d,
            'percent_change_90d': self.percent_change_90d
        }
    
    def to_public_dict(self) -> dict:
        return self.to_dict()

class HomeCoins(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    updated_at: int = Field(..., gt=0, description='Timestamp in seconds')
    coins: list[CoinInfo]

    @staticmethod
    def from_dict_static(data: dict) -> 'HomeCoins':
        return HomeCoins(
            updated_at=data['updated_at'],
            coins=[ CoinInfo.from_static_dict(x) for x in data['coins'] ]
        )

    def to_dict(self) -> dict:
        return {
            'updated_at': self.updated_at,
            'coins': [ x.to_public_dict() for x in self.coins ],
        }
    
    def from_dict(self, data: dict) -> 'HomeCoins':
        return self.from_dict_static(data)
    
    def to_public_dict(self):
        return self.to_dict()