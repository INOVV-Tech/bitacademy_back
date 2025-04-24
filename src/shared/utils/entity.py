import re
import uuid
import base64
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

def is_valid_entity_int(data: dict, field_key: str, min_value = 0, max_value = 1000) -> bool:
    if field_key not in data:
        return False
    
    if not isinstance(data[field_key], int):
        return False
    
    if data[field_key] < min_value or data[field_key] > max_value:
        return False
    
    return True

def is_valid_entity_dict(data: dict, field_key: str, valid_keys: list[str] | None = None) -> bool:
    if field_key not in data:
        return False
    
    if not isinstance(data[field_key], dict):
        return False
    
    if valid_keys is not None:
        for valid_key in valid_keys:
            if valid_key not in data[field_key]:
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

def is_valid_getall_object(data: dict) -> bool:
    if not is_valid_entity_int(data, 'limit', 1, 1000):
        return False
    
    if 'last_evaluated_key' in data:
        if not is_valid_entity_string(data, 'last_evaluated_key', min_length=0, max_length=256):
            return False
    else:
        data['last_evaluated_key'] = ''

    if 'sort_order' in data:
        if not isinstance(data['sort_order'], str) \
            or data['sort_order'] not in [ 'asc', 'desc' ]:
            return False
    else:
        data['sort_order'] = 'desc'
    
    return True

def is_valid_uuid(data: dict, field_key: str, version: int = 4) -> bool:
    try:
        uuid_obj = uuid.UUID(data[field_key], version=version)

        return str(uuid_obj) == data[field_key].lower()
    except:
        return False

def is_valid_entity_base64_string(data: dict, field_key: str, max_length: int = 2900000) -> bool:
    if not is_valid_entity_string(data, field_key, min_length=4, max_length=max_length):
        return False
    
    try:
        base64_parts = data[field_key].split(',')

        base64_data = base64_parts[-1]
        byte_string = base64_data.encode('utf8')

        base64.b64decode(byte_string, validate=True)

        return True
    except:
        pass
    
    return False