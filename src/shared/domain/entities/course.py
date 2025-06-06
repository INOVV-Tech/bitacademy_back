from pydantic import BaseModel, ConfigDict, Field

from src.shared.domain.enums.vip_level import VIP_LEVEL

from src.shared.utils.time import now_timestamp
from src.shared.utils.entity import random_entity_id, \
    is_valid_entity_string, is_valid_entity_url, is_valid_entity_string_list, \
    is_valid_entity_uuid, is_valid_entity_base64_string, is_valid_entity_int_enum

from src.shared.infra.object_storage.file import ObjectStorageFile

class Course(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    id: str
    title: str
    description: str
    teachers: list[str]
    duration: str
    cover_img: ObjectStorageFile
    card_img: ObjectStorageFile
    created_at: int = Field(..., gt=0, description='Timestamp in seconds')
    external_url: str
    tags: list[str]
    user_id: str
    vip_level: VIP_LEVEL

    @staticmethod
    def data_contains_valid_id(data: dict) -> bool:
        return is_valid_entity_uuid(data, 'id', version=4)
    
    @staticmethod
    def data_contains_valid_title(data: dict) -> bool:
        return is_valid_entity_string(data, 'title', min_length=2, max_length=256)
    
    @staticmethod
    def data_contains_valid_description(data: dict) -> bool:
        return is_valid_entity_string(data, 'description', min_length=2, max_length=2048)
    
    @staticmethod
    def data_contains_valid_teachers(data: dict) -> bool:
        return is_valid_entity_string_list(data, 'teachers', min_length=0)
    
    @staticmethod
    def data_contains_valid_duration(data: dict) -> bool:
        return is_valid_entity_string(data, 'duration', min_length=2, max_length=128)
    
    @staticmethod
    def data_contains_valid_external_url(data: dict) -> bool:
        return is_valid_entity_url(data, 'external_url')
    
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
    def norm_teachers(teachers: list[str]) -> list[str]:
        return [ x.strip() for x in teachers ]

    @staticmethod
    def from_request_data(data: dict, user_id: str) -> 'tuple[str, Course | None]':
        if not Course.data_contains_valid_title(data):
            return ('Título inválido', None)
        
        if not Course.data_contains_valid_description(data):
            return ('Descrição inválida', None)
        
        if not Course.data_contains_valid_teachers(data):
            return ('Lista de professores inválida', None)
        
        teachers = Course.norm_teachers(data['teachers'])

        if not Course.data_contains_valid_duration(data):
            return ('Duração inválida', None)

        if not Course.data_contains_valid_external_url(data):
            return ('Link externo inválido', None)
        
        if not Course.data_contains_valid_cover_img(data):
            return ('Imagem de capa inválida', None)
        
        if not Course.data_contains_valid_card_img(data):
            return ('Imagem de card inválida', None)
        
        if 'tags' in data:
            if not Course.data_contains_valid_tags(data):
                return ('Lista de tags inválida', None)
            
            tags = Course.norm_tags(data['tags'])
        else:
            tags = []

        if not Course.data_contains_valid_vip_level(data):
            return ('Level de VIP inválido', None)

        course = Course(
            id=random_entity_id(),
            title=data['title'].strip(),
            description=data['description'].strip(),
            teachers=teachers,
            duration=data['duration'].strip(),
            cover_img=ObjectStorageFile.from_base64_data(data['cover_img']),
            card_img=ObjectStorageFile.from_base64_data(data['card_img']),
            created_at=now_timestamp(),
            external_url=data['external_url'].strip(),
            tags=tags,
            user_id=user_id,
            vip_level=VIP_LEVEL(data['vip_level'])
        )

        if not course.cover_img.verify_base64_image():
            return ('Imagem de capa inválida', None)
        
        if not course.card_img.verify_base64_image():
            return ('Imagem de card inválida', None)
        
        return ('', course)

    @staticmethod
    def from_dict_static(data: dict) -> 'Course':
        return Course(
            id=data['id'],
            title=data['title'],
            description=data['description'],
            teachers=data['teachers'],
            duration=data['duration'],
            cover_img=ObjectStorageFile.from_dict_static(data['cover_img']),
            card_img=ObjectStorageFile.from_dict_static(data['card_img']),
            created_at=int(data['created_at']),
            external_url=data['external_url'],
            tags=data['tags'],
            user_id=data['user_id'],
            vip_level=VIP_LEVEL(data['vip_level'])
        )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'teachers': self.teachers,
            'duration': self.duration,
            'cover_img': self.cover_img.to_dict(),
            'card_img': self.card_img.to_dict(),
            'created_at': self.created_at,
            'external_url': self.external_url,
            'tags': self.tags,
            'user_id': self.user_id,
            'vip_level': self.vip_level.value
        }
    
    def from_dict(self, data: dict) -> 'Course':
        return self.from_dict_static(data)
    
    def to_public_dict(self) -> dict:
        result = self.to_dict()

        del result['user_id']

        return result
    
    def update_from_dict(self, data: dict) -> dict:
        updated_fields = {}

        if Course.data_contains_valid_title(data):
            self.title = data['title'].strip()

            updated_fields['title'] = self.title

        if Course.data_contains_valid_external_url(data):
            self.external_url = data['external_url'].strip()

            updated_fields['external_url'] = self.external_url

        if Course.data_contains_valid_tags(data):
            self.tags = Course.norm_tags(data['tags'])

            updated_fields['tags'] = self.tags

        if Course.data_contains_valid_vip_level(data):
            self.vip_level = VIP_LEVEL(data['vip_level'])

            updated_fields['vip_level'] = self.vip_level

        if Course.data_contains_valid_description(data):
            self.description = data['description'].strip()

            updated_fields['description'] = self.description

        if Course.data_contains_valid_teachers(data):
            self.teachers = Course.norm_teachers(data['teachers'])

            updated_fields['teachers'] = self.teachers

        if Course.data_contains_valid_duration(data):
            self.duration = data['duration'].strip()

            updated_fields['duration'] = self.duration

        if Course.data_contains_valid_cover_img(data):
            cover_img = ObjectStorageFile.from_base64_data(data['cover_img'])

            if cover_img.verify_base64_image():
                self.cover_img = cover_img

                updated_fields['cover_img'] = self.cover_img

        if Course.data_contains_valid_card_img(data):
            card_img = ObjectStorageFile.from_base64_data(data['card_img'])

            if card_img.verify_base64_image():
                self.card_img = card_img

                updated_fields['card_img'] = self.card_img

        updated_fields['any_updated'] = len(updated_fields.keys()) > 0

        return updated_fields