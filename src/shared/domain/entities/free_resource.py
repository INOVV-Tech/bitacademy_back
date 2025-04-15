from pydantic import BaseModel, Field

class FreeResource(BaseModel):
    id: str
    title: str
    created_at: int = Field(..., gt=0, description='Timestamp in seconds')
    url: str
    tags: list[str]

    # TODO: text search strategy
    # title_search: str

    @staticmethod
    def from_dict_static(data: dict) -> 'FreeResource':
        return FreeResource(
            id=data['id'],
            title=data['title'],
            created_at=data['created_at'],
            url=data['url'],
            tags=data['tags']
        )

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'created_at': self.created_at,
            'url': self.url,
            'tags': self.tags
        }
    
    def from_dict(self, data: dict) -> 'FreeResource':
        return FreeResource.from_dict_static(data)