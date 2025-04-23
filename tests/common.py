import os
import base64
import random
import string
from pathlib import Path
from dotenv import load_dotenv

from src.shared.domain.enums.role import ROLE
from src.shared.domain.enums.user_status import USER_STATUS

from src.shared.domain.entities.user import User

from src.shared.utils.time import now_timestamp
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

    role = ROLE.ADMIN.value if admin else ROLE.CLIENT.value
    user_status = USER_STATUS.CONFIRMED.value
    
    now = now_timestamp()

    user = User.from_dict_static({
        'user_id': random_entity_id(),
        'name': name,
        'email': email,
        'role': role,
        'user_status': user_status,
        'created_at': now,
        'updated_at': now,
        'email_verified': True,
        'enabled': True,
        'phone': '51000000000'
    })

    return user.to_api_dto()

def load_resource(filename, encode_base64=True, base64_prefix=''):
    root_directory = get_root_directory()

    filepath = os.path.join(root_directory, 'tests', '.resources', filename)

    data = open(filepath, 'rb').read()

    if encode_base64:
        data = base64.b64encode(data)
        data = data.decode('utf8')
        data = base64_prefix + ',' + data if len(base64_prefix) > 0 else data

    return data

