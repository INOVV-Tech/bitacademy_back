from pydantic import BaseModel, ConfigDict, Field

from src.shared.utils.time import now_timestamp
from src.shared.utils.entity import random_entity_id, is_valid_entity_uuid, \
    is_valid_entity_string, is_valid_entity_string_enum, is_valid_entity_base64_string, \
    is_valid_entity_dict

from src.shared.infra.object_storage.file import ObjectStorageFile

from src.shared.domain.enums.role import ROLE
from src.shared.domain.enums.community_type import COMMUNITY_TYPE
from src.shared.domain.enums.community_permission import COMMUNITY_PERMISSION

from src.shared.messaging.parser import parse_input_msg

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
    
    def to_public_dict(self, role: ROLE | None = None) -> dict:
        result = self.to_dict()

        if role is not None and not self.is_edit_role(role):
            for role_field in ROLE:
                if role_field != role:
                    del result[role_field.value]

        return result
    
    def is_forbidden(self, role: ROLE) -> bool:
        return getattr(self, role.value) == COMMUNITY_PERMISSION.FORBIDDEN
    
    def is_edit_role(self, role: ROLE) -> bool:
        return getattr(self, role.value) == COMMUNITY_PERMISSION.READ_WRITE_EDIT
    
    def is_read_role(self, role: ROLE) -> bool:
        return not self.is_forbidden(role)
    
    def is_write_role(self, role: ROLE) -> bool:
        perm_value = getattr(self, role.value)

        return perm_value == COMMUNITY_PERMISSION.READ_WRITE or perm_value == COMMUNITY_PERMISSION.READ_WRITE_EDIT
    
    def get_all_read_roles(self) -> list[ROLE]:
        return [ x for x in ROLE if self.is_read_role(x) ]

class CommunityChannel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    id: str
    title: str
    comm_type: COMMUNITY_TYPE
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
    def data_contains_valid_comm_type(data: dict) -> bool:
        return is_valid_entity_string_enum(data, 'comm_type', COMMUNITY_TYPE)
    
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
        
        if not CommunityChannel.data_contains_valid_comm_type(data):
            return ('Tipo de canal de comunidade inválido', None)
        
        if not CommunityChannel.data_contains_valid_icon_img(data):
            return ('Imagem de ícone inválida', None)
        
        if not CommunityChannel.data_contains_valid_permissions(data):
            return ('Permissões de canal de comunidade inválidas', None)

        community_channel = CommunityChannel(
            id=random_entity_id(),
            title=data['title'].strip(),
            comm_type=COMMUNITY_TYPE[data['comm_type']],
            icon_img=ObjectStorageFile.from_base64_data(data['icon_img']),
            permissions=CommunityChannelPermissions.from_dict_static(data['permissions']),
            created_at=now_timestamp(),
            user_id=user_id
        )

        if not community_channel.icon_img.verify_base64_image():
            return ('Imagem de ícone inválida', None)

        return ('', community_channel)

    @staticmethod
    def from_dict_static(data: dict) -> 'CommunityChannel':
        return CommunityChannel(
            id=data['id'],
            title=data['title'],
            comm_type=COMMUNITY_TYPE[data['comm_type']],
            icon_img=ObjectStorageFile.from_dict_static(data['icon_img']),
            permissions=CommunityChannelPermissions.from_dict_static(data['permissions']),
            created_at=int(data['created_at']),
            user_id=data['user_id']
        )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'comm_type': self.comm_type.value,
            'icon_img': self.icon_img.to_dict(),
            'permissions': self.permissions.to_dict(),
            'created_at': self.created_at,
            'user_id': self.user_id
        }
    
    def from_dict(self, data: dict) -> 'CommunityChannel':
        return self.from_dict_static(data)
    
    def to_public_dict(self, role: ROLE | None = None) -> dict:
        result = self.to_dict()

        del result['user_id']

        if role is not None:
            result['permissions'] = self.permissions.to_public_dict(role)

        return result
    
    def update_from_dict(self, data: dict) -> dict:
        updated_fields = {}

        if CommunityChannel.data_contains_valid_title(data):
            self.title = data['title'].strip()

            updated_fields['title'] = self.title
        
        if CommunityChannel.data_contains_valid_icon_img(data):
            icon_img = ObjectStorageFile.from_base64_data(data['icon_img'])

            if icon_img.verify_base64_image():
                self.icon_img = icon_img
                
                updated_fields['icon_img'] = self.icon_img
        
        if CommunityChannel.data_contains_valid_permissions(data):
            self.permissions = CommunityChannelPermissions.from_dict_static(data['permissions'])

            updated_fields['permissions'] = self.permissions
        
        updated_fields['any_updated'] = len(updated_fields.keys()) > 0

        return updated_fields
    
class CommunityForumTopic(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    id: str
    channel_id: str
    title: str
    icon_img: ObjectStorageFile
    created_at: int = Field(..., gt=0, description='Timestamp in seconds')
    user_id: str

    @staticmethod
    def data_contains_valid_id(data: dict) -> bool:
        return is_valid_entity_uuid(data, 'id', version=4)
    
    @staticmethod
    def data_contains_valid_channel_id(data: dict) -> bool:
        return is_valid_entity_uuid(data, 'channel_id', version=4)
    
    @staticmethod
    def data_contains_valid_title(data: dict) -> bool:
        return is_valid_entity_string(data, 'title', min_length=2, max_length=512)
    
    @staticmethod
    def data_contains_valid_icon_img(data: dict) -> bool:
        return is_valid_entity_base64_string(data, 'icon_img')

    @staticmethod
    def from_request_data(data: dict, user_id: str) -> 'tuple[str, CommunityForumTopic | None]':
        if not CommunityForumTopic.data_contains_valid_title(data):
            return ('Título inválido', None)
        
        if not CommunityForumTopic.data_contains_valid_channel_id(data):
            return ('Identificador de canal de comunidade inválido', None)
        
        if not CommunityForumTopic.data_contains_valid_icon_img(data):
            return ('Imagem de ícone inválida', None)

        community_forum_topic = CommunityForumTopic(
            id=random_entity_id(),
            channel_id=data['channel_id'],
            title=data['title'].strip(),
            icon_img=ObjectStorageFile.from_base64_data(data['icon_img']),
            created_at=now_timestamp(),
            user_id=user_id
        )

        if not community_forum_topic.icon_img.verify_base64_image():
            return ('Imagem de ícone inválida', None)

        return ('', community_forum_topic)

    @staticmethod
    def from_dict_static(data: dict) -> 'CommunityForumTopic':
        return CommunityForumTopic(
            id=data['id'],
            channel_id=data['channel_id'],
            title=data['title'],
            icon_img=ObjectStorageFile.from_dict_static(data['icon_img']),
            created_at=int(data['created_at']),
            user_id=data['user_id']
        )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'channel_id': self.channel_id,
            'title': self.title,
            'icon_img': self.icon_img.to_dict(),
            'created_at': self.created_at,
            'user_id': self.user_id
        }
    
    def to_public_dict(self) -> dict:
        result = self.to_dict()

        del result['user_id']

        return result

class CommunitySession(BaseModel):
    connection_id: str
    user_id: str
    user_name: str
    user_role: ROLE
    created_at: int = Field(..., gt=0, description='Timestamp in seconds')

    @staticmethod
    def from_dict_static(data: dict) -> 'CommunitySession':
        return CommunitySession(
            connection_id=data['connection_id'],
            user_id=data['user_id'],
            user_name=data['user_name'],
            user_role=ROLE[data['user_role']],
            created_at=int(data['created_at'])
        )

    def to_dict(self) -> dict:
        return {
            'connection_id': self.connection_id,
            'user_id': self.user_id,
            'user_name': self.user_name,
            'user_role': self.user_role.value,
            'created_at': self.created_at
        }
    
    def to_public_dict(self) -> dict:
        return self.to_dict()
    
class CommunitySessionLock(BaseModel):
    expire_timestamp: int = Field(..., description='Timestamp in milliseconds', gt=0)

    @staticmethod
    def from_dict_static(data: dict) -> 'CommunitySessionLock':
        return CommunitySessionLock(
            expire_timestamp=int(data['expire_timestamp'])
        )
    
    def to_dict(self) -> dict:
        return {
            'expire_timestamp': self.expire_timestamp
        }

class CommunityMessage(BaseModel):
    id: str
    channel_id: str
    forum_topic_id: str | None
    raw_content: str
    created_at: int = Field(..., gt=0, description='Timestamp in seconds')
    updated_at: int = Field(..., gt=0, description='Timestamp in seconds')
    user_id: str

    @staticmethod
    def data_contains_valid_id(data: dict) -> bool:
        return is_valid_entity_uuid(data, 'id', version=4)

    @staticmethod
    def from_dict_static(data: dict) -> 'CommunityMessage':
        return CommunityMessage(
            id=data['id'],
            channel_id=data['channel_id'],
            forum_topic_id=data['forum_topic_id'] if 'forum_topic_id' in data else None,
            raw_content=data['raw_content'],
            created_at=int(data['created_at']),
            updated_at=int(data['updated_at']),
            user_id=data['user_id']
        )
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'channel_id': self.channel_id,
            'forum_topic_id': self.forum_topic_id,
            'raw_content': self.raw_content,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'user_id': self.user_id
        }
    
    def to_public_dict(self, extra_data: dict = {}) -> dict:
        result = self.to_dict()

        for key, value in extra_data.items():
            result[key] = value
        
        return result
    
    def update_from_dict(self, data: dict) -> dict:
        updated_fields = {}

        if 'raw_content' in data:
            (error, raw_content) = parse_input_msg(data['raw_content'])

            if error != '':
                self.raw_content = raw_content
                updated_fields['raw_content'] = self.raw_content
        
        updated_fields['any_updated'] = len(updated_fields.keys()) > 0
        
        return updated_fields
    
    def to_delete_dict(self) -> dict:
        return {
            'id': self.id,
            'channel_id': self.channel_id,
            'forum_topic_id': self.forum_topic_id,
            'user_id': self.user_id
        }