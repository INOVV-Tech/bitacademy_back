import json
import base64

def encode_cursor(last_evaluated_key: dict | None) -> str:
    return base64.urlsafe_b64encode(json.dumps(last_evaluated_key).encode()).decode()

def decode_cursor(cursor: str) -> dict | None:
    if cursor == '':
        return None

    return json.loads(base64.urlsafe_b64decode(cursor.encode()).decode())

def encode_cursor_get_all(db_data: dict, item_key: str, limit: int, last_evaluated_key: dict | None) -> dict:
    next_cursor = encode_cursor(last_evaluated_key) if last_evaluated_key else ''

    return {
        'total': db_data['total'],
        'per_page': limit,
        'data': [ x.to_public_dict() for x in db_data[item_key] ],
        'next_cursor': next_cursor,
        'has_more': bool(next_cursor)
    }