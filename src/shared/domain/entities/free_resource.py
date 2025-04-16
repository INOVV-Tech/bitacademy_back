from pydantic import BaseModel, Field

from src.shared.utils.time import now_timestamp
from src.shared.utils.entity import random_entity_id, \
    is_valid_entity_string, is_valid_entity_url, is_valid_entity_string_list

class FreeResource(BaseModel):
    id: str
    title: str
    created_at: int = Field(..., gt=0, description='Timestamp in seconds')
    external_url: str
    tags: list[str]
    user_id: int

    # TODO: text search strategy
    # title_search: str

    @staticmethod
    def from_request_data(data: dict, user_id: int) -> 'tuple[str, FreeResource | None]':
        if not is_valid_entity_string(data, 'title', min_length=2, max_length=128):
            return ('Título inválido', None)
        
        if not is_valid_entity_url(data, 'external_url'):
            return ('Link externo inválido', None)
        
        if 'tags' in data:
            if not is_valid_entity_string_list(data, 'tags', min_length=0):
                return ('Lista de tags inválida', None)
            
            tags = data['tags']
        else:
            tags = []

        free_resource = FreeResource(
            id=random_entity_id(),
            title=data['title'],
            created_at=now_timestamp(),
            external_url=data['external_url'],
            tags=tags,
            user_id=user_id
        )

        return ('', free_resource)

    @staticmethod
    def from_dict_static(data: dict) -> 'FreeResource':
        return FreeResource(
            id=data['id'],
            title=data['title'],
            created_at=data['created_at'],
            external_url=data['external_url'],
            tags=data['tags'],
            user_id=data['user_id']
        )

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'created_at': self.created_at,
            'external_url': self.external_url,
            'tags': self.tags,
            'user_id': self.user_id
        }
    
    def from_dict(self, data: dict) -> 'FreeResource':
        return FreeResource.from_dict_static(data)
    
    def to_public_dict(self):
        return self.to_dict()