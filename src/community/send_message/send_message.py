import json

from src.shared.infra.repositories.repository import Repository

from src.shared.domain.enums.community_type import COMMUNITY_TYPE
from src.shared.domain.entities.community import CommunityChannel, \
    CommunityForumTopic, CommunitySession

from src.shared.messaging.parser import parse_input_msg

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

    if message is None:
        return fail_resp(f'Campo "message" não foi encontrado')

    if not CommunityChannel.data_contains_valid_id({ 'id': channel_id }):
        return fail_resp(f'Campo "channel_id" não foi encontrado')
    
    (error, raw_content) = parse_input_msg(message)

    if error != '':
        return fail_resp(error)
    
    repository = Repository(community_repo=True)

    community_session = repository.community_repo.get_one_session(connection_id)

    if community_session is None:
        return fail_resp('Sessão não foi encontrada', 401)
    
    community_channel = repository.community_repo.get_one_channel(channel_id)

    if community_channel is None:
        return fail_resp('Canal de comunidade não foi encontrado')
    
    if community_channel.comm_type == COMMUNITY_TYPE.FORUM:
        forum_topic_id = body.get('forum_topic_id', None)

        if not CommunityForumTopic.data_contains_valid_id({ 'id': forum_topic_id }):
            return fail_resp(f'Campo "forum_topic_id" não foi encontrado')
        
        community_forum_topic = repository.community_repo.get_one_forum_topic(forum_topic_id)

        if community_forum_topic is None:
            return fail_resp('Fórum de comunidade não foi encontrado')
        
        return push_forum_msg(repository, community_session, community_channel, \
            community_forum_topic, raw_content)

    return push_chat_msg(repository, community_session, community_channel, raw_content)

def push_forum_msg(repository: Repository, community_session: CommunitySession, \
    community_channel: CommunityChannel, community_forum_topic: CommunityForumTopic, raw_content: str) -> dict:
    pass

def push_chat_msg(repository: Repository, community_session: CommunitySession, \
    community_channel: CommunityChannel, raw_content: str) -> dict:
    if not community_channel.permissions.is_write_role(community_session.user_role):
        return fail_resp('Usuário não tem permissão para escrever no canal')
    
    read_roles = community_channel.permissions.get_all_read_roles()

    for role in read_roles:
        pass
    
    return ok_resp()