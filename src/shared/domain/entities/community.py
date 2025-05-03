from pydantic import BaseModel, ConfigDict, Field

from src.shared.utils.time import now_timestamp
from src.shared.utils.entity import random_entity_id, is_valid_entity_uuid, \
    is_valid_entity_string, is_valid_entity_string_enum, is_valid_entity_base64_string, \
    is_valid_entity_dict

from src.shared.infra.object_storage.file import ObjectStorageFile

from src.shared.domain.enums.community_type import COMMUNITY_TYPE
from src.shared.domain.enums.community_permission import COMMUNITY_PERMISSION

class CommunityChannelPermissions:
    @staticmethod
    def data_contains_valid_permissions(data: dict) -> bool:
        if not is_valid_entity_string_enum(data, 'GUEST', COMMUNITY_PERMISSION):
            return False
        
        if not is_valid_entity_string_enum(data, 'AFFILIATE', COMMUNITY_PERMISSION):
            return False
        
        if not is_valid_entity_string_enum(data, 'VIP', COMMUNITY_PERMISSION):
            return False
        
        if not is_valid_entity_string_enum(data, 'TEACHER', COMMUNITY_PERMISSION):
            return False
        
        if not is_valid_entity_string_enum(data, 'ADMIN', COMMUNITY_PERMISSION):
            return False
        
        return True

    @staticmethod
    def from_dict_static(data: dict) -> 'CommunityChannelPermissions':
        return CommunityChannelPermissions(
            GUEST=COMMUNITY_PERMISSION[data['GUEST']],
            AFFILIATE=COMMUNITY_PERMISSION[data['AFFILIATE']],
            VIP=COMMUNITY_PERMISSION[data['VIP']],
            TEACHER=COMMUNITY_PERMISSION[data['TEACHER']],
            ADMIN=COMMUNITY_PERMISSION[data['ADMIN']]
        )

    def __init__(self,
        GUEST: COMMUNITY_PERMISSION = COMMUNITY_PERMISSION.FORBIDDEN,
        AFFILIATE: COMMUNITY_PERMISSION = COMMUNITY_PERMISSION.FORBIDDEN,
        VIP: COMMUNITY_PERMISSION = COMMUNITY_PERMISSION.READ,
        TEACHER: COMMUNITY_PERMISSION = COMMUNITY_PERMISSION.READ_WRITE,
        ADMIN: COMMUNITY_PERMISSION = COMMUNITY_PERMISSION.READ_WRITE_EDIT
    ):
        self.GUEST = GUEST
        self.AFFILIATE = AFFILIATE
        self.VIP = VIP
        self.TEACHER = TEACHER
        self.ADMIN = ADMIN

    def to_dict(self) -> dict:
        return {
            'GUEST': self.GUEST.value,
            'AFFILIATE': self.AFFILIATE.value,
            'VIP': self.VIP.value,
            'TEACHER': self.TEACHER.value,
            'ADMIN': self.ADMIN.value
        }
    
    def to_public_dict(self) -> dict:
        return self.to_dict()
    
    def update_from_dict(self, data: dict) -> dict:
        updated_fields = {}

        return updated_fields

class CommunityChannel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    id: str
    title: str
    type: COMMUNITY_TYPE
    icon_img: ObjectStorageFile
    permissions: CommunityChannelPermissions
    created_at: int = Field(..., gt=0, description='Timestamp in seconds')
    user_id: str

    @staticmethod
    def data_contains_valid_id(data: dict) -> bool:
        return is_valid_entity_uuid(data, 'id', version=4)
    
    @staticmethod
    def data_contains_valid_title(data: dict) -> bool:
        return is_valid_entity_string(data, 'title', min_length=2, max_length=512)
    
    @staticmethod
    def data_contains_valid_type(data: dict) -> bool:
        return is_valid_entity_string_enum(data, 'type', COMMUNITY_TYPE)
    
    @staticmethod
    def data_contains_valid_icon_img(data: dict) -> bool:
        return is_valid_entity_base64_string(data, 'icon_img')
    
    @staticmethod
    def data_contains_valid_permissions(data: dict) -> bool:
        if not is_valid_entity_dict(data, 'permissions'):
            return False

        return CommunityChannelPermissions.data_contains_valid_permissions(data['permissions'])

    @staticmethod
    def from_request_data(data: dict, user_id: str) -> 'tuple[str, CommunityChannel | None]':
        if not CommunityChannel.data_contains_valid_title(data):
            return ('Título inválido', None)
        
        if not CommunityChannel.data_contains_valid_type(data):
            return ('Tipo de canal de comunidade inválido', None)
        
        if not CommunityChannel.data_contains_valid_icon_img(data):
            return ('Imagem de ícone inválida', None)
        
        if not CommunityChannel.data_contains_valid_permissions(data):
            return ('Permissões de canal de comunidade inválidas', None)

        community_channel = CommunityChannel(
            id=random_entity_id(),
            title=data['title'].strip(),
            type=COMMUNITY_TYPE[data['type']],
            icon_img=ObjectStorageFile.from_base64_data(data['icon_img']),
            permissions=CommunityChannelPermissions.from_dict_static(data),
            created_at=now_timestamp(),
            user_id=user_id
        )

        return ('', community_channel)

    @staticmethod
    def from_dict_static(data: dict) -> 'CommunityChannel':
        return CommunityChannel(
            id=data['id'],
            title=data['title'],
            type=COMMUNITY_TYPE[data['type']],
            icon_img=ObjectStorageFile.from_dict_static(data['icon_img']),
            permissions=CommunityChannelPermissions.from_dict_static(data['permissions']),
            created_at=int(data['created_at']),
            user_id=data['user_id']
        )

    def to_dict(self) -> dict:
        return {}
    
    def from_dict(self, data: dict) -> 'CommunityChannel':
        return self.from_dict_static(data)
    
    def to_public_dict(self) -> dict:
        result = self.to_dict()

        del result['user_id']

        return result
    
    def update_from_dict(self, data: dict) -> dict:
        updated_fields = {}

        if CommunityChannel.data_contains_valid_title(data):
            self.title = data['title'].strip()

            updated_fields['title'] = self.title
        
        if CommunityChannel.data_contains_valid_icon_img(data):
            self.icon_img = ObjectStorageFile.from_base64_data(data['icon_img'])

            updated_fields['icon_img'] = self.icon_img
        
        if CommunityChannel.data_contains_valid_permissions(data):
            self.permissions = CommunityChannelPermissions.from_dict_static(data['permissions'])

            updated_fields['permissions'] = self.permissions
        
        updated_fields['any_updated'] = len(updated_fields.keys()) > 0

        return updated_fields