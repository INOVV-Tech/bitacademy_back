import json
import boto3
from botocore.client import Config

from src.shared.infra.repositories.repository import Repository

from src.shared.domain.enums.role import ROLE
from src.shared.domain.enums.community_type import COMMUNITY_TYPE
from src.shared.domain.enums.community_action import COMMUNITY_ACTION
from src.shared.domain.entities.community import CommunityChannel, \
    CommunityForumTopic, CommunityMessage

from src.shared.messaging.parser import parse_input_msg

from src.shared.utils.time import now_timestamp
from src.shared.utils.entity import random_entity_id

def fail_resp(error: str, code: int = 400):
    return { 'statusCode': code, 'body': error }

def ok_resp():
    return { 'statusCode': 200 }

def lambda_handler(event, context) -> dict:
    request_context = event.get('requestContext', {})
    connection_id = request_context.get('connectionId', '')
    
    body = json.loads(event.get('body', '{}'))

    message = body.get('message', None)
    channel_id = body.get('channel_id', None)
    forum_topic_id = body.get('forum_topic_id', None)

    if message is None:
        return fail_resp(f'Campo "message" não foi encontrado')
    
    (error, raw_content) = parse_input_msg(message)

    if error != '':
        return fail_resp(error)
    
    repository = Repository(community_repo=True)
    
    if CommunityChannel.data_contains_valid_id({ 'id': channel_id }):
        return push_chat_msg(request_context, repository, connection_id, channel_id, raw_content)
    
    if CommunityForumTopic.data_contains_valid_id({ 'id': forum_topic_id }):
        return push_forum_msg(request_context, repository, connection_id, forum_topic_id, raw_content)
    
    return fail_resp('Nenhum identificador de canal encontrado')

def push_chat_msg(request_context: dict, repository: Repository, connection_id: str, \
    channel_id: str, raw_content: str) -> dict:
    community_session = repository.community_repo.get_one_session(connection_id)

    if community_session is None:
        return fail_resp('Sessão não foi encontrada', 401)
    
    community_channel = repository.community_repo.get_one_channel(channel_id)

    if community_channel is None:
        return fail_resp('Canal de comunidade não foi encontrado')
    
    if community_channel.comm_type != COMMUNITY_TYPE.CHAT:
        return fail_resp('Canal de comunidade não é um chat')
    
    if not community_channel.permissions.is_write_role(community_session.user_role):
        return fail_resp('Usuário não tem permissão para escrever no canal')

    now = now_timestamp()

    msg = CommunityMessage(
        id=random_entity_id(),
        channel_id=channel_id,
        forum_topic_id=None,
        raw_content=raw_content,
        created_at=now,
        updated_at=now,
        user_id=community_session.user_id
    )

    msg_data = msg.to_public_dict()
    read_roles = community_channel.permissions.get_all_read_roles()

    if len(read_roles) > 0:
        broadcast_msg(request_context, repository, read_roles, msg_data)

    repository.community_repo.create_message(msg)
    
    return ok_resp()

def push_forum_msg(request_context: dict, repository: Repository, connection_id: str, \
    forum_topic_id: str, raw_content: str) -> dict:
    community_session = repository.community_repo.get_one_session(connection_id)

    if community_session is None:
        return fail_resp('Sessão não foi encontrada', 401)
    
    community_forum_topic = repository.community_repo.get_one_forum_topic(forum_topic_id)

    if community_forum_topic is None:
        return fail_resp('Fórum de comunidade não foi encontrado')
    
    community_channel = repository.community_repo.get_one_channel(community_forum_topic.channel_id)

    if not community_channel.permissions.is_write_role(community_session.user_role):
        return fail_resp('Usuário não tem permissão para escrever no canal')
    
    now = now_timestamp()

    msg = CommunityMessage(
        id=random_entity_id(),
        channel_id=community_forum_topic.channel_id,
        forum_topic_id=community_forum_topic.id,
        raw_content=raw_content,
        created_at=now,
        updated_at=now,
        user_id=community_session.user_id
    )
    
    msg_data = msg.to_public_dict()
    read_roles = community_channel.permissions.get_all_read_roles()

    if len(read_roles) > 0:
        broadcast_msg(request_context, repository, read_roles, msg_data)

    repository.community_repo.create_message(msg)
    
    return ok_resp()

def broadcast_msg(request_context: dict, repository: Repository, read_roles: list[ROLE], \
    msg_data: dict):
    api_gateway = None

    try:
        stage = request_context.get('stage', '')
        domain_name = request_context.get('domainName', '')

        api_gateway = boto3.client('apigatewaymanagementapi',
            endpoint_url=f'https://{domain_name}/{stage}',
            config=Config(connect_timeout=1, retries={ 'max_attempts': 3 })
        )
    except:
        pass

    if api_gateway is None:
        return

    payload = json.dumps({
        'action': COMMUNITY_ACTION.CHANNEL_MESSAGE_CREATE.value,
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