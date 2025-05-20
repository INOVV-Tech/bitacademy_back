import re
import base64
import hashlib
import filetype

from src.shared.utils.time import now_timestamp

from src.shared.infra.external.s3_datasource import S3Datasource

from src.shared.infra.object_storage.constants import ALLOWED_IMAGE_MIME_TYPES, \
    ALLOWED_VIDEO_MIME_TYPES, ALLOWED_DOCUMENT_MIME_TYPES

class ObjectStorageFile:
    name: str
    mime_type: str
    external_url: str
    base64_data: str
    created_at: int
    
    @staticmethod
    def from_base64_data(data: str, name: str = '', mime_type: str = '') -> 'ObjectStorageFile':
        base64_parts = data.split(',')

        if len(base64_parts) == 1:
            base64_data = base64_parts[0]
        else:
            mime_regex = re.match(r'^data:(.*?);', base64_parts[0])
            mime_type = mime_regex.group(1)
            base64_data = base64_parts[1]

        return ObjectStorageFile(
            name=name,
            mime_type=mime_type,
            external_url='',
            base64_data=base64_data,
            created_at=now_timestamp()
        )

    @staticmethod
    def from_dict_static(data: dict) -> 'ObjectStorageFile':
        return ObjectStorageFile(
            name=data['name'],
            mime_type=data['mime_type'],
            external_url=data['external_url'],
            base64_data=data['base64_data'],
            created_at=int(data['created_at'])
        )
    
    def __init__(self, name: str, mime_type: str, external_url: str, \
        base64_data: str, created_at: int):
        self.name = name
        self.mime_type = mime_type
        self.external_url = external_url
        self.base64_data = base64_data
        self.created_at = created_at

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'mime_type': self.mime_type,
            'external_url': self.external_url,
            'base64_data': self.base64_data,
            'created_at': self.created_at
        }
    
    def from_dict(self, data: dict) -> 'ObjectStorageFile':
        return self.from_dict_static(data)
    
    def to_public_dict(self) -> dict:
        return self.to_dict()
    
    def contains_external_url(self) -> bool:
        return len(self.external_url) > 0
    
    def is_pending(self) -> bool:
        return len(self.base64_data) > 0
    
    def store_in_s3(self, s3_datasource: S3Datasource) -> dict:
        if self.contains_external_url():
            self.base64_data = ''
            
            return {}
        
        s3_key = hashlib.sha256(self.base64_data.encode('utf8')).hexdigest()

        resp = s3_datasource.upload_base64_file(s3_key, self.base64_data, self.mime_type)

        if 'error' in resp:
            return resp

        self.name = s3_key
        self.external_url = resp['url']
        self.base64_data = ''
        self.created_at = now_timestamp()

        return {}
    
    def verify_base64_type(self, allowed_mime_types) -> bool:
        if self.contains_external_url():
            return False
        
        if self.mime_type not in allowed_mime_types:
            return False

        binary_data = base64.b64decode(self.base64_data)

        prob_mime_type = None

        try:
            kind = filetype.guess(binary_data)

            if not kind:
                return False
            
            prob_mime_type = kind.mime
        except:
            return False
        
        if prob_mime_type not in allowed_mime_types:
            return False
        
        self.mime_type = prob_mime_type

        return True
    
    def verify_base64_image(self) -> bool:
        return self.verify_base64_type(ALLOWED_IMAGE_MIME_TYPES)
    
    def verify_base64_video(self) -> bool:
        return self.verify_base64_type(ALLOWED_VIDEO_MIME_TYPES)

    def verify_base64_document(self) -> bool:
        return self.verify_base64_type(ALLOWED_DOCUMENT_MIME_TYPES)
    
    def verify_base64_all(self) -> bool:
        allowed_mime_types = ALLOWED_IMAGE_MIME_TYPES
        allowed_mime_types += ALLOWED_VIDEO_MIME_TYPES
        allowed_mime_types += ALLOWED_DOCUMENT_MIME_TYPES

        return self.verify_base64_type(allowed_mime_types)