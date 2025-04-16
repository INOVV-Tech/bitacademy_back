import random
import string

from src.shared.domain.enums.role import ROLE
from src.shared.domain.enums.user_status import USER_STATUS

from src.shared.domain.entities.user import User
from src.shared.infra.repositories.dtos.auth_authorizer_dto import AuthAuthorizerDTO

from src.shared.utils.time import now_timestamp

def random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def get_requester_user():
    name = 'bit_user_' + random_string()
    email = name + '@gmail.com'

    role = ROLE.CLIENT.value
    user_status = USER_STATUS.CONFIRMED.value
    
    now = now_timestamp()

    user = User.from_dict_static({
        'user_id': 0,
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


    