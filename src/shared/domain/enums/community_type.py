from enum import Enum

class COMMUNITY_TYPE(Enum):
    FORUM = 'FORUM'
    CHAT = 'CHAT'

    @staticmethod
    def length() -> int:
        return len(COMMUNITY_TYPE)