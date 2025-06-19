from pydantic import BaseModel, Field

class CoinInfo(BaseModel):
    name: str
    symbol: str
    slug: str
    num_market_pairs: int
    cmc_id: int
    total_supply: str
    circulating_supply: str
    market_cap: str
    created_at: int = Field(..., gt=0, description='Timestamp in seconds')
    
    @staticmethod
    def from_dict_static(data: dict) -> 'CoinInfo':
        return CoinInfo(
            name=data['name'],
            symbol=data['symbol'],
            slug=data['slug'],
            num_market_pairs=int(data['num_market_pairs']),
            cmc_id=int(data['cmc_id']),
            total_supply=data['total_supply'],
            circulating_supply=data['circulating_supply'],
            market_cap=data['market_cap'],
            created_at=int(data['created_at'])
        )

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
            'created_at': self.created_at
        }
    
    def from_dict(self, data: dict) -> 'CoinInfo':
        return self.from_dict_static(data)
    
    def to_public_dict(self) -> dict:
        result = self.to_dict()

        result['cmc_img_url'] = f'https://s2.coinmarketcap.com/static/img/coins/64x64/{self.cmc_id}.png'

        return result
    
    def to_symbol_public_dict(self) -> dict:
        result = self.to_public_dict()

        del result['symbol']
        del result['num_market_pairs']
        del result['created_at']

        return result