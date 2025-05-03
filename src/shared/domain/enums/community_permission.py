from enum import Enum

class COMMUNITY_PERMISSION(Enum):
    FORBIDDEN = 'FORBIDDEN'
    READ = 'READ'
    READ_WRITE = 'READ_WRITE'
    READ_WRITE_EDIT = 'READ_WRITE_EDIT'

    @staticmethod
    def length() -> int:
        return len(COMMUNITY_PERMISSION)