import os
from populate.common import load_app_env, load_resource

load_app_env()

from src.shared.infra.repositories.repository import Repository
from src.shared.infra.repositories.dtos.auth_authorizer_dto import AuthAuthorizerDTO

from src.shared.domain.enums.role import ROLE
from src.shared.domain.enums.community_type import COMMUNITY_TYPE
from src.shared.domain.entities.community import CommunityChannel
from src.shared.domain.entities.community import CommunityChannelPermissions

requester_user = AuthAuthorizerDTO(
    user_id=os.environ.get('POPULATE_USER_ID'),
    name=os.environ.get('POPULATE_USER_NAME'),
    email='',
    phone='',
    role=ROLE.ADMIN,
    email_verified=True,
    phone_verified=True,
    vip_subscription=None
)

def populate_community_channels():
    repository = Repository(community_repo=True)

    comm_channels = [
        {
            'title': 'Sinais',
            'comm_type': COMMUNITY_TYPE.FORUM.value,
            'icon_img': load_resource('comm-channel-icon.png',
                encode_base64=True, base64_prefix='data:image/png;base64'),
            'permissions': CommunityChannelPermissions().to_dict()
        },
        {
            'title': 'Airdrops',
            'comm_type': COMMUNITY_TYPE.CHAT.value,
            'icon_img': load_resource('comm-channel-icon-2.png',
                encode_base64=True, base64_prefix='data:image/png;base64'),
            'permissions': CommunityChannelPermissions().to_dict()
        },
        {
            'title': 'DeFi',
            'comm_type': COMMUNITY_TYPE.FORUM.value,
            'icon_img': load_resource('comm-channel-icon-3.png',
                encode_base64=True, base64_prefix='data:image/png;base64'),
            'permissions': CommunityChannelPermissions().to_dict()
        },
        {
            'title': 'Onchain',
            'comm_type': COMMUNITY_TYPE.CHAT.value,
            'icon_img': load_resource('comm-channel-icon-4.png',
                encode_base64=True, base64_prefix='data:image/png;base64'),
            'permissions': CommunityChannelPermissions().to_dict()
        }
    ]

    for i in range(4):
        (error, community_channel) = CommunityChannel.from_request_data(comm_channels[i], requester_user)

        s3_datasource = repository.get_s3_datasource()

        upload_resp = community_channel.icon_img.store_in_s3(s3_datasource)

        repository.community_repo.create_channel(community_channel)

        print(f'Populated {(i + 1)} community channel')

    print('Populated community channels')