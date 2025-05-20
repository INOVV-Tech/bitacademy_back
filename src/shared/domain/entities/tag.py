from pydantic import BaseModel, ConfigDict, Field

from src.shared.utils.time import now_timestamp
from src.shared.utils.entity import is_valid_entity_string

class Tag(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    title: str
    created_at: int = Field(..., gt=0, description='Timestamp in seconds')

    @staticmethod
    def from_string_list(tags: list[str]) -> 'list[Tag]':
        result = []

        tag_dict = {}

        now = now_timestamp()

        for tag_str in tags:
            if tag_str in tag_dict:
                continue

            tag_dict[tag_str] = True

            result.append(Tag(
                title=Tag.norm_title(tag_str),
                created_at=now
            ))
        
        return result
    
    @staticmethod
    def data_contains_valid_title(data: dict) -> bool:
        return is_valid_entity_string(data, 'title', min_length=2, max_length=256)
    
    @staticmethod
    def norm_title(title: str) -> str:
        return title.strip().lower()

    @staticmethod
    def from_dict_static(data: dict) -> 'Tag':
        return Tag(
            title=data['title'],
            created_at=int(data['created_at'])
        )

    def to_dict(self) -> dict:
        return {
            'title': self.title,
            'created_at': self.created_at
        }
    
    def from_dict(self, data: dict) -> 'Tag':
        return self.from_dict_static(data)
    
    def to_public_dict(self) -> dict:
        return self.to_dict()