from pydantic import BaseModel, Field

class FreeResource(BaseModel):
    id: str
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