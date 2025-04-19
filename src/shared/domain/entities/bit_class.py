from pydantic import BaseModel, Field

from src.shared.domain.enums.vip_level import VIP_LEVEL

from src.shared.utils.time import now_timestamp
from src.shared.utils.entity import random_entity_id, \
    is_valid_entity_string, is_valid_entity_url, is_valid_entity_string_list, \
    is_valid_uuid

class BitClass(BaseModel):
    id: str
    title: str
    created_at: int = Field(..., gt=0, description='Timestamp in seconds')
    external_url: str
    tags: list[str]
    user_id: str
    vip_level: VIP_LEVEL

    @staticmethod
    def data_contains_valid_id(data: dict) -> bool:
        return is_valid_uuid(data, 'id', version=4)
    
    @staticmethod
    def data_contains_valid_title(data: dict) -> bool:
        return is_valid_entity_string(data, 'title', min_length=2, max_length=128)
    
    @staticmethod
    def data_contains_valid_external_url(data: dict) -> bool:
        return is_valid_entity_url(data, 'external_url')
    
    @staticmethod
    def data_contains_valid_tags(data: dict) -> bool:
        return is_valid_entity_string_list(data, 'tags', min_length=0)
    
    @staticmethod
    def data_contains_valid_vip_level(data: dict) -> bool:
        if 'vip_level' not in data:
            return False
        
        if not isinstance(data['vip_level'], int):
            return False
        
        return data['vip_level'] in [ vipl for vipl in VIP_LEVEL ]
    
    @staticmethod
    def norm_tags(tags: list[str]) -> list[str]:
        return [ tag.strip().lower() for tag in tags ]

    @staticmethod
    def from_request_data(data: dict, user_id: str) -> 'tuple[str, BitClass | None]':
        if not is_valid_entity_string(data, 'title', min_length=2, max_length=128):
            return ('Título inválido', None)
        
        if not is_valid_entity_url(data, 'external_url'):
            return ('Link externo inválido', None)
        
        if 'tags' in data:
            if not is_valid_entity_string_list(data, 'tags', min_length=0):
                return ('Lista de tags inválida', None)
            
            tags = BitClass.norm_tags(data['tags'])
        else:
            tags = []

        if not BitClass.data_contains_valid_vip_level(data):
            return ('VIP level inválido', None)

        bit_class = BitClass(
            id=random_entity_id(),
            title=data['title'].strip(),
            created_at=now_timestamp(),
            external_url=data['external_url'].strip(),
            tags=tags,
            user_id=user_id,
            vip_level=VIP_LEVEL(data['vip_level'])
        )
        
        return ('', bit_class)

    @staticmethod
    def from_dict_static(data: dict) -> 'BitClass':
        return BitClass(
            id=data['id'],
            title=data['title'],
            created_at=data['created_at'],
            external_url=data['external_url'],
            tags=data['tags'],
            user_id=data['user_id'],
            vip_level=VIP_LEVEL(data['vip_level'])
    )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'created_at': self.created_at,
            'external_url': self.external_url,
            'tags': self.tags,
            'user_id': self.user_id,
            'vip_level': self.vip_level.value
        }
    
    def from_dict(self, data: dict) -> 'BitClass':
        return self.from_dict_static(data)
    
    def to_public_dict(self) -> dict:
        return self.to_dict()
    
    def update_from_dict(self, data: dict) -> None:
        if self.data_contains_valid_title(data):
            self.title = data['title'].strip()

        if self.data_contains_valid_external_url(data):
            self.external_url = data['external_url'].strip()

        if self.data_contains_valid_tags(data):
            self.tags = BitClass.norm_tags(data['tags'])

        if self.data_contains_valid_vip_level(data):
            self.vip_level = VIP_LEVEL(data['vip_level'])