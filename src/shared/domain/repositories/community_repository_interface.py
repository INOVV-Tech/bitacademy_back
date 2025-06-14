from abc import ABC, abstractmethod

from src.shared.domain.enums.role import ROLE
from src.shared.domain.enums.community_type import COMMUNITY_TYPE
from src.shared.domain.entities.community import CommunityChannel, \
    CommunityForumTopic, CommunitySessionLock, CommunitySession, CommunityMessage

class ICommunityRepository(ABC):
    ### CHANNEL ###
    @abstractmethod
    def create_channel(self, community_channel: CommunityChannel) -> CommunityChannel:
        pass

    @abstractmethod
    def get_all_channels(self,
        title: str = '',
        comm_types: list[COMMUNITY_TYPE] = [],
        user_role: ROLE | None = None,
        limit: int = 10, last_evaluated_key: dict | None = None, sort_order: str = 'desc') -> dict:
        pass
    
    @abstractmethod
    def get_one_channel(self, id: str) -> CommunityChannel | None:
        pass
    
    @abstractmethod
    def get_one_channel_by_title(self, title: str) -> CommunityChannel | None:
        pass

    @abstractmethod
    def update_channel(self, community_channel: CommunityChannel) -> CommunityChannel:
        pass

    @abstractmethod
    def delete_channel(self, id: str) -> int:
        pass

    @abstractmethod
    def role_can_read_channel(self, channel_id: str, user_role: ROLE) -> bool:
        pass

    @abstractmethod
    def role_can_edit_channel(self, channel_id: str, user_role: ROLE) -> bool:
        pass

    ### FORUM ###
    @abstractmethod
    def create_forum_topic(self, community_forum_topic: CommunityForumTopic) -> CommunityForumTopic:
        pass

    @abstractmethod
    def get_channel_forum_topics(self,
        channel_id: str,
        title: str = '',
        limit: int = 10, last_evaluated_key: dict | None = None, sort_order: str = 'desc') -> dict:
        pass
    
    @abstractmethod
    def get_one_forum_topic(self, id: str) -> CommunityForumTopic | None:
        pass

    @abstractmethod
    def delete_forum_topic(self, id: str) -> int:
        pass

    @abstractmethod
    def delete_all_forum_topics(self, channel_id: str) -> int | None:
        pass
    
    ### SESSION ###
    @abstractmethod
    def acquire_session_lock(self, user_id: str, expire_seconds: int = 15) -> CommunitySessionLock | None:
        pass
    
    @abstractmethod
    def release_session_lock(self, user_id: str) -> int:
        pass
    
    @abstractmethod
    def create_session(self, community_session: CommunitySession) -> CommunitySession:
        pass
    
    @abstractmethod
    def get_one_session(self, connection_id: str) -> CommunitySession | None:
        pass
    
    @abstractmethod
    def get_user_sessions(self, user_id: str) -> list[CommunitySession]:
        pass

    @abstractmethod
    def get_sessions_by_role(self, user_role: ROLE) -> list[CommunitySession]:
        pass

    @abstractmethod
    def count_user_sessions(self, user_id: str) -> int:
        pass

    @abstractmethod
    def delete_session(self, connection_id: str) -> int:
        pass

    ### MESSAGE ###
    @abstractmethod
    def create_message(self, community_message: CommunityMessage) -> CommunityMessage:
        pass

    @abstractmethod
    def get_channel_messages(self,
        channel_id: str,
        forum_topic_id: str | None = None,
        ini_timestamp: int | None = None,
        end_timestamp: int | None = None,
        limit: int = 10, last_evaluated_key: dict | None = None, sort_order: str = 'desc') -> dict:
        pass

    @abstractmethod
    def get_one_message(self, id: str) -> CommunityMessage | None:
        pass

    @abstractmethod
    def update_message(self, community_message: CommunityMessage) -> CommunityMessage:
        pass

    @abstractmethod
    def delete_message(self, id: str) -> int:
        pass

    @abstractmethod
    def delete_all_messages(self, channel_id: str, forum_topic_id: str | None = None) -> int | None:
        pass
