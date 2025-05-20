from pydantic import BaseModel, ConfigDict, Field

from src.shared.utils.time import now_timestamp
from src.shared.utils.entity import random_entity_id, \
    is_valid_entity_string, is_valid_entity_string_list, \
    is_valid_entity_uuid, is_valid_entity_base64_string, is_valid_entity_url

from src.shared.infra.object_storage.file import ObjectStorageFile

class Tool(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    id: str
    title: str
    description: str
    external_url: str
    cover_img: ObjectStorageFile
    tags: list[str]
    user_id: str
    created_at: int = Field(..., gt=0, description='Timestamp in seconds')

    @staticmethod
    def data_contains_valid_id(data: dict) -> bool:
        return is_valid_entity_uuid(data, 'id', version=4)
    
    @staticmethod
    def data_contains_valid_title(data: dict) -> bool:
        return is_valid_entity_string(data, 'title', min_length=2, max_length=512)

    @staticmethod
    def data_contains_valid_description(data: dict) -> bool:
        return is_valid_entity_string(data, 'description', min_length=2, max_length=2048)

    @staticmethod
    def data_contains_valid_external_url(data: dict) -> bool:
        return is_valid_entity_url(data, 'external_url')
    
    @staticmethod
    def data_contains_valid_cover_img(data: dict) -> bool:
        return is_valid_entity_base64_string(data, 'cover_img')
    
    @staticmethod
    def data_contains_valid_tags(data: dict) -> bool:
        return is_valid_entity_string_list(data, 'tags', min_length=0)
    
    @staticmethod
    def norm_tags(tags: list[str]) -> list[str]:
        return [ tag.strip().lower() for tag in tags ]

    @staticmethod
    def from_request_data(data: dict, user_id: str) -> 'tuple[str, Tool | None]':
        if not Tool.data_contains_valid_title(data):
            return ('Título inválido', None)

        if not Tool.data_contains_valid_description(data):
            return ('Descrição inválida', None)
        
        if not Tool.data_contains_valid_external_url(data):
            return ('Link externo inválido', None)
        
        if not Tool.data_contains_valid_cover_img(data):
            return ('Imagem de capa inválida', None)
        
        if 'tags' in data:
            if not Tool.data_contains_valid_tags(data):
                return ('Lista de tags inválida', None)
            
            tags = Tool.norm_tags(data['tags'])
        else:
            tags = []

        tool = Tool(
            id=random_entity_id(),
            title=data['title'].strip(),
            description=data['description'].strip(),
            external_url=data['external_url'].strip(),
            cover_img=ObjectStorageFile.from_base64_data(data['cover_img']),
            tags=tags,
            user_id=user_id,
            created_at=now_timestamp()
        )

        if not tool.cover_img.verify_base64_image():
            return ('Imagem de capa inválida', None)
        
        return ('', tool)

    @staticmethod
    def from_dict_static(data: dict) -> 'Tool':
        return Tool(
            id=data['id'],
            title=data['title'],
            description=data['description'],
            external_url=data['external_url'],
            cover_img=ObjectStorageFile.from_dict_static(data['cover_img']),
            tags=data['tags'],
            user_id=data['user_id'],
            created_at=int(data['created_at'])
        )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'external_url': self.external_url,
            'cover_img': self.cover_img.to_dict(),
            'tags': self.tags,
            'user_id': self.user_id,
            'created_at': self.created_at
        }
    
    def from_dict(self, data: dict) -> 'Tool':
        return self.from_dict_static(data)
    
    def to_public_dict(self) -> dict:
        result = self.to_dict()

        del result['user_id']

        return result
    
    def update_from_dict(self, data: dict) -> dict:
        updated_fields = {}

        if Tool.data_contains_valid_title(data):
            self.title = data['title'].strip()

            updated_fields['title'] = self.title

        if Tool.data_contains_valid_description(data):
            self.description = data['description'].strip()

            updated_fields['description'] = self.description

        if Tool.data_contains_valid_external_url(data):
            self.external_url = data['external_url'].strip()

            updated_fields['external_url'] = self.external_url

        if Tool.data_contains_valid_cover_img(data):
            cover_img = ObjectStorageFile.from_base64_data(data['cover_img'])

            if cover_img.verify_base64_image():
                self.cover_img = cover_img

                updated_fields['cover_img'] = self.cover_img

        if Tool.data_contains_valid_tags(data):
            self.tags = Tool.norm_tags(data['tags'])

            updated_fields['tags'] = self.tags

        updated_fields['any_updated'] = len(updated_fields.keys()) > 0

        return updated_fields