import bleach

from src.shared.messaging.constants import BLEACH_ALLOWED_TAGS, \
    BLEACH_ALLOWED_ATTRIBUTES, BLEACH_ALLOWED_PROTOCOLS

def sanitize_input_msg(input_content: str) -> str:
    return bleach.clean(input_content,
        tags=BLEACH_ALLOWED_TAGS,
        attributes=BLEACH_ALLOWED_ATTRIBUTES,
        protocols=BLEACH_ALLOWED_PROTOCOLS,
        css_sanitizer=None,
        strip_comments=False
    )