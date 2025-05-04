from src.shared.messaging.constants import MAX_MESSAGE_CHARACTERS, \
    MESSAGE_ALPHABET_REGEX

from src.shared.messaging.sanitize import sanitize_input_msg

def parse_input_msg(input_content: str) -> tuple[str, str | None]:
    if not isinstance(input_content, str):
        return ('Tipo de conteúdo de mensagem inválido', None)

    msg_length = len(input_content)

    if msg_length == 0:
        return ('Mensagem vazia', None)
    
    if msg_length > MAX_MESSAGE_CHARACTERS:
        return (f'Mensagem muito grande ({MAX_MESSAGE_CHARACTERS} caracteres max)', None)

    alphabet_filter = MESSAGE_ALPHABET_REGEX.findall(input_content)
    input_content = ''.join([ x[0] for x in alphabet_filter ])

    if len(input_content) == 0:
        return ('Mensagem vazia', None)

    input_content = sanitize_input_msg(input_content).strip()

    if len(input_content) == 0:
        return ('Mensagem vazia', None)

    return ('', input_content)