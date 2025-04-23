from enum import Enum

class OBJECT_STORAGE_FILE_TYPE(Enum):
    DOCUMENT = 'DOCUMENT'
    VIDEO = 'VIDEO'
    IMAGE = 'IMAGE'

    @staticmethod
    def contains(value: str) -> bool:
        return value in [ x.value for x in OBJECT_STORAGE_FILE_TYPE ]