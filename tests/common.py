import os
import base64
import random
import string
from pathlib import Path
from dotenv import load_dotenv

from src.shared.domain.enums.role import ROLE

from src.shared.utils.entity import random_entity_id

def get_root_directory():
    return Path(__file__).parent.parent

def load_app_env(stage='DEV'):
    root_directory = get_root_directory()

    env_filepath = os.path.join(root_directory, 'iac', '.env')

    load_dotenv(env_filepath)
    
    os.environ['STAGE'] = stage

def random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def get_requester_user(admin=False):
    name = 'bit_user_' + random_string()
    email = name + '@gmail.com'

    role = ROLE.ADMIN.value if admin else ROLE.VIP.value

    return {
        'sub': random_entity_id(),
        'name': name,
        'email': email,
        'phone_number': '+5511999999999',
        'custom:role': role,
        'email_verified': True,
        'phone_verified': True
    }

def load_resource(filename, encode_base64=True, base64_prefix=''):
    root_directory = get_root_directory()

    filepath = os.path.join(root_directory, 'tests', '.resources', filename)

    data = open(filepath, 'rb').read()

    if encode_base64:
        data = base64.b64encode(data)
        data = data.decode('utf8')
        data = base64_prefix + ',' + data if len(base64_prefix) > 0 else data

    return data

def write_base64(root_directory, base64):
    with open(os.path.join(root_directory, 'tests', '.resources', 'test.txt'), 'wb') as file:
        file.write(base64.encode('utf8'))
