import re

MAX_MESSAGE_CHARACTERS = 3500

MESSAGE_ALPHABET_PATTERNS = [
    r'A-Za-z0-9À-ÿØ-öø-ÿ \:\<\>@\[\]\/\\\`\"\'\(\)\.\,\;\?\!\~\+\-\=\_\#\$\%\^\&\*\|\{\}', # Default
    r'\U0001F600-\U0001F64F', # Emoticons
    r'\U0001F300-\U0001F5FF', # Misc Symbols and Pictographs
    r'\U0001F680-\U0001F6FF', # Transport & Map
    r'\U0001F1E6-\U0001F1FF', # Regional country flags (A-Z)
    r'\U00002700-\U000027BF', # Dingbats
    r'\U00002600-\U000026FF', # Misc symbols
    r'\U0001F900-\U0001F9FF', # Supplemental Symbols and Pictographs
    r'\U0001FA70-\U0001FAFF', # Extended symbols
]

TMP_ALPHABET_REGEX = ''.join(MESSAGE_ALPHABET_PATTERNS)

MESSAGE_ALPHABET_REGEX = re.compile(f'([{TMP_ALPHABET_REGEX}])')