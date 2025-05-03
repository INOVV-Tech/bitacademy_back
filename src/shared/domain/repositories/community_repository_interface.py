from abc import ABC, abstractmethod

from src.shared.domain.enums.role import ROLE
from src.shared.domain.enums.community_type import COMMUNITY_TYPE
from src.shared.domain.entities.community import CommunityChannel

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
    def delete_channel(self, id: str) -> CommunityChannel | None:
        pass