from pydantic import BaseModel, ConfigDict, Field

from src.shared.domain.enums.vip_level import VIP_LEVEL

from src.shared.utils.time import now_timestamp
from src.shared.utils.entity import random_entity_id, \
    is_valid_entity_string, is_valid_entity_string_list, \
    is_valid_entity_uuid, is_valid_entity_base64_string, is_valid_entity_int_enum

from src.shared.infra.object_storage.file import ObjectStorageFile

class News(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: str
    title: str
    header: str
    content: str
    cover_img: ObjectStorageFile
    card_img: ObjectStorageFile
    created_at: int = Field(..., gt=0, description='Timestamp in seconds')
    tags: list[str]
    user_id: str
    vip_level: VIP_LEVEL

    @staticmethod
    def data_contains_valid_id(data: dict) -> bool:
        return is_valid_entity_uuid(data, 'id', version=4)
    
    @staticmethod
    def data_contains_valid_title(data: dict) -> bool:
        return is_valid_entity_string(data, 'title', min_length=2, max_length=512)
    
    @staticmethod
    def data_contains_valid_header(data: dict) -> bool:
        return is_valid_entity_string(data, 'header', min_length=2, max_length=1024)

    @staticmethod
    def data_contains_valid_content(data: dict) -> bool:
        return is_valid_entity_string(data, 'content', min_length=2, max_length=8128)
    
    @staticmethod
    def data_contains_valid_cover_img(data: dict) -> bool:
        return is_valid_entity_base64_string(data, 'cover_img')
    
    @staticmethod
    def data_contains_valid_card_img(data: dict) -> bool:
        return is_valid_entity_base64_string(data, 'card_img')
    
    @staticmethod
    def data_contains_valid_tags(data: dict) -> bool:
        return is_valid_entity_string_list(data, 'tags', min_length=0)
    
    @staticmethod
    def data_contains_valid_vip_level(data: dict) -> bool:
        return is_valid_entity_int_enum(data, 'vip_level', VIP_LEVEL)
    
    @staticmethod
    def norm_tags(tags: list[str]) -> list[str]:
        return [ tag.strip().lower() for tag in tags ]

    @staticmethod
    def from_request_data(data: dict, user_id: str) -> 'tuple[str, News | None]':
        if not News.data_contains_valid_title(data):
            return ('Título inválido', None)
        
        if not News.data_contains_valid_header(data):
            return ('Título inválido', None)

        if not News.data_contains_valid_content(data):
            return ('Conteúdo inválido', None)
        
        if not News.data_contains_valid_cover_img(data):
            return ('Imagem de capa inválida', None)

        if not News.data_contains_valid_card_img(data):
            return ('Imagem de card inválida', None)
        
        if 'tags' in data:
            if not News.data_contains_valid_tags(data):
                return ('Lista de tags inválida', None)
            
            tags = News.norm_tags(data['tags'])
        else:
            tags = []

        if not News.data_contains_valid_vip_level(data):
            return ('Level de VIP inválido', None)

        news = News(
            id=random_entity_id(),
            title=data['title'].strip(),
            header=data['header'].strip(),
            content=data['content'].strip(),
            cover_img=ObjectStorageFile.from_base64_data(data['cover_img']),
            card_img=ObjectStorageFile.from_base64_data(data['card_img']),
            created_at=now_timestamp(),
            tags=tags,
            user_id=user_id,
            vip_level=VIP_LEVEL(data['vip_level'])
        )

        if not news.cover_img.verify_base64_image():
            return ('Imagem de capa inválida', None)
        
        if not news.card_img.verify_base64_image():
            return ('Imagem de card inválida', None)

        return ('', news)

    @staticmethod
    def from_dict_static(data: dict) -> 'News':
        return News(
            id=data['id'],
            title=data['title'],
            header=data['header'],
            content=data['content'],
            cover_img=ObjectStorageFile.from_dict_static(data['cover_img']),
            card_img=ObjectStorageFile.from_dict_static(data['card_img']),
            created_at=int(data['created_at']),
            tags=data['tags'],
            user_id=data['user_id'],
            vip_level=VIP_LEVEL(data['vip_level'])
        )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'header': self.header,
            'content': self.content,
            'cover_img': self.cover_img.to_dict(),
            'card_img': self.card_img.to_dict(),
            'created_at': self.created_at,
            'tags': self.tags,
            'user_id': self.user_id,
            'vip_level': self.vip_level.value
        }
    
    def from_dict(self, data: dict) -> 'News':
        return self.from_dict_static(data)
    
    def to_public_dict(self) -> dict:
        result = self.to_dict()

        del result['user_id']

        return result
    
    def update_from_dict(self, data: dict) -> dict:
        updated_fields = {}

        if News.data_contains_valid_title(data):
            self.title = data['title'].strip()

            updated_fields['title'] = self.title

        if News.data_contains_valid_header(data):
            self.header = data['header'].strip()

            updated_fields['header'] = self.header

        if News.data_contains_valid_content(data):
            self.content = data['content'].strip()

            updated_fields['content'] = self.content

        if News.data_contains_valid_tags(data):
            self.tags = News.norm_tags(data['tags'])

            updated_fields['tags'] = self.tags

        if News.data_contains_valid_vip_level(data):
            self.vip_level = VIP_LEVEL(data['vip_level'])

            updated_fields['vip_level'] = self.vip_level

        if News.data_contains_valid_cover_img(data):
            cover_img = ObjectStorageFile.from_base64_data(data['cover_img'])

            if cover_img.verify_base64_image():
                self.cover_img = cover_img

                updated_fields['cover_img'] = self.cover_img
        
        if News.data_contains_valid_card_img(data):
            card_img = ObjectStorageFile.from_base64_data(data['card_img'])

            if card_img.verify_base64_image():
                self.card_img = card_img

                updated_fields['card_img'] = self.card_img

        updated_fields['any_updated'] = len(updated_fields.keys()) > 0

        return updated_fields