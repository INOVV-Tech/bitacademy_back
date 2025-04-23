from src.shared.domain.enums.object_storage_file_type import OBJECT_STORAGE_FILE_TYPE

class ObjectStorageFile:
    name: str
    file_type: OBJECT_STORAGE_FILE_TYPE
    external_url: str
    created_at: int

    @staticmethod
    def from_request_data(data: dict) -> 'tuple[str, ObjectStorageFile | None]':
        pass

    @staticmethod
    def from_dict_static(data: dict) -> 'ObjectStorageFile':
        return ObjectStorageFile(
            name=data['name'],
            file_type=OBJECT_STORAGE_FILE_TYPE[data['file_type']],
            external_url=data['external_url'],
            created_at=int(data['created_at'])
        )

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'file_type': self.file_type.value,
            'external_url': self.external_url,
            'created_at': self.created_at
        }
    
    def from_dict(self, data: dict) -> 'ObjectStorageFile':
        return self.from_dict_static(data)
    
    def to_public_dict(self) -> dict:
        return self.to_dict()