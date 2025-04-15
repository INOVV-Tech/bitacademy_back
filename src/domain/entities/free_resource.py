from pydantic import BaseModel, Field

from infra.models.models import FreeResourceModel

class FreeResource(BaseModel):
    id: int
    title: str
    created_at: int = Field(..., gt=0, description='Timestamp in seconds')
    url: str
    tags: list[str]

    # TODO: text search strategy
    # title_search: str
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'created_at': self.created_at,
            'url': self.url,
            'tags': self.tags
        }

    def to_db(self) -> FreeResourceModel:
        return FreeResourceModel(
            id=self.id,
            title=self.title,
            created_at=self.created_at,
            url=self.url,
            tags=self.tags
        )
  
    @staticmethod
    def from_db(data: FreeResourceModel) -> 'FreeResource':
        return FreeResource(
            id=data.id,
            title=data.title,
            created_at=data.created_at,
            url=data.url,
            tags=data.tags
        )