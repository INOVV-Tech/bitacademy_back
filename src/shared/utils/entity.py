import re
import uuid
from urllib.parse import urlparse

def random_entity_id() -> str:
    return str(uuid.uuid4())

def is_valid_entity_string(data: dict, field_key: str, min_length: int = 2, max_length: int = 256) -> bool:
    if field_key not in data:
        return False
    
    if not isinstance(data[field_key], str):
        return False
    
    if len(data[field_key]) < min_length or len(data[field_key]) > max_length:
        return False

    return True

def is_valid_entity_url(data: dict, field_key: str) -> bool:
    if not is_valid_entity_string(data, field_key, min_length=10, max_length=1024):
        return False

    try:
        parsed = urlparse(data[field_key])

        if parsed.scheme not in ('http', 'https') or not parsed.netloc:
            return False
    except:
        return False

    unsafe_pattern = re.compile(r"[\x00-\x1F\x7F<>\"'`;]")

    if unsafe_pattern.search(data[field_key]):
        return False

    return True

def is_valid_entity_string_list(data: dict, field_key: str, min_length: int = 0, \
    max_length: int = 128, min_str_length: int = 2, max_str_length: int = 256) -> bool:
    if field_key not in data:
        return False
    
    if not isinstance(data[field_key], list):
        return False

    if len(data[field_key]) < min_length or len(data[field_key]) > max_length:
        return False
    
    for item in data[field_key]:
        if not isinstance(item, str):
            return False
        
        if len(item) < min_str_length or len(item) > max_str_length:
            return False

    return True