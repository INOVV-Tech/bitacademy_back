import os
import json
import boto3
from botocore.client import Config

from src.shared.environments import Environments

from src.shared.infra.repositories.repository import Repository

from src.shared.domain.enums.role import ROLE
from src.shared.domain.enums.community_action import COMMUNITY_ACTION
from src.shared.domain.entities.community import CommunityMessage

def broadcast_msg(action: COMMUNITY_ACTION, msg_data: dict, read_roles: list[ROLE]):
    repository = Repository(community_repo=True)
    
    api_gateway = None

    try:
        WEBSOCKET_API_ID = os.environ.get('WEBSOCKET_API_ID', '')
        WEBSOCKET_STAGE = os.environ.get('WEBSOCKET_STAGE', '')

        endpoint_url = f'https://{WEBSOCKET_API_ID}.execute-api.{Environments.region}.amazonaws.com/{WEBSOCKET_STAGE}'

        api_gateway = boto3.client('apigatewaymanagementapi',
            endpoint_url=endpoint_url,
            config=Config(connect_timeout=1, retries={ 'max_attempts': 3 })
        )
    except:
        pass

    if api_gateway is None:
        return

    payload = json.dumps({
        'action': action.value,
        'message': msg_data
    }).encode('utf-8')

    for role in read_roles:
        community_sessions = repository.community_repo.get_sessions_by_role(role)
        
        for community_session in community_sessions:
            try:
                api_gateway.post_to_connection(
                    ConnectionId=community_session.connection_id,
                    Data=payload
                )
            except:
                pass

def broadcast_msg_update(msg: CommunityMessage, read_roles: list[ROLE]):
    return broadcast_msg(
        action=COMMUNITY_ACTION.CHANNEL_MESSAGE_UPDATE,
        msg_data=msg.to_public_dict(),
        read_roles=read_roles
    )

def broadcast_msg_delete(msg: CommunityMessage, read_roles: list[ROLE]):
    return broadcast_msg(
        action=COMMUNITY_ACTION.CHANNEL_MESSAGE_DELETE,
        msg_data=msg.to_delete_dict(),
        read_roles=read_roles
    )