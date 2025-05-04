from src.shared.domain.entities.community import CommunityMessage

from src.shared.utils.time import now_timestamp

from src.shared.messaging.constants import MAX_MESSAGE_CHARACTERS, \
    MESSAGE_ALPHABET_REGEX

def parse_input_msg(input_content: str) -> CommunityMessage | None:
    if not isinstance(input_content, str):
        return None

    if len(input_content) == 0:
        return None
    
    input_content = input_content[:MAX_MESSAGE_CHARACTERS]

    alphabet_filter = MESSAGE_ALPHABET_REGEX.findall(input_content)
    input_content = ''.join([ x[0] for x in alphabet_filter ])
    
    if len(input_content) == 0:
        return None

    # apply sanitation
        # remove invalid patterns

    input_content = input_content.strip()

    if len(input_content) == 0:
        return None

    return CommunityMessage(
        raw_content=input_content,
        created_at=now_timestamp()
    )