from pydantic import BaseModel, Field

class BitClass(BaseModel):
    id: str
    title: str
    created_at: int = Field(..., gt=0, description='Timestamp in seconds')
    external_url: str
    tags: list[str]
    vip_level: int
    user_id: int

    @staticmethod
    def from_dict_static(data: dict) -> 'BitClass':
        return BitClass(
            id=data['id'],
            title=data['title'],
            created_at=data['created_at'],
            external_url=data['external_url'],
            tags=data['tags'],
            vip_level=data['vip_level'],
            user_id=data['user_id']
        )

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'created_at': self.created_at,
            'external_url': self.external_url,
            'tags': self.tags,
            'vip_level': self.vip_level,
            'user_id': self.user_id
        }
    
    def from_dict(self, data: dict) -> 'BitClass':
        return BitClass.from_dict_static(data)