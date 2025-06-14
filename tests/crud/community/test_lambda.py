import json
import pytest

from tests.common import load_app_env, get_requester_user, \
    load_resource

load_app_env()

from src.shared.helpers.external_interfaces.http_models import HttpRequest

from src.shared.infra.repositories.repository import Repository

from src.routes.create_community_channel.create_community_channel import Controller as CreateChannelController
from src.routes.get_all_community_channels.get_all_community_channels import Controller as GetAllChannelsController
from src.routes.get_one_community_channel.get_one_community_channel import Controller as GetOneChannelController
from src.routes.update_community_channel.update_community_channel import Controller as UpdateChannelController
from src.routes.delete_community_channel.delete_community_channel import Controller as DeleteChannelController
from src.routes.create_community_forum_topic.create_community_forum_topic import Controller as CreateForumTopicController
from src.routes.get_community_channel_forum_topics.get_community_channel_forum_topics import Controller as GetChannelForumTopicsController
from src.routes.delete_community_forum_topic.delete_community_forum_topic import Controller as DeleteForumTopicController
from src.routes.get_community_channel_messages.get_community_channel_messages import Controller as GetCommunityCHannelMessages

from src.shared.domain.enums.community_type import COMMUNITY_TYPE
from src.shared.domain.enums.community_permission import COMMUNITY_PERMISSION
from src.shared.domain.entities.community import CommunityChannelPermissions

from src.shared.domain.entities.community import CommunityMessage

from src.shared.utils.time import now_timestamp
from src.shared.utils.entity import random_entity_id

class Test_CommunityLambda:
    def print_data(self, data: dict) -> None:
        print(json.dumps(data, indent=4, ensure_ascii=False))

    def get_body(self):
        return {
            'requester_user': get_requester_user(admin=True)
        }
    
    def call_lambda(self, controller, body={}, headers={}, query_params={}):
        request = HttpRequest(body=body, headers=headers, query_params=query_params)

        return controller.execute(request)

    ### CHANNEL ###
    @pytest.mark.skip(reason='Done')
    def test_lambda_create_channel(self):
        body = self.get_body()

        icon_img = load_resource('catbeach.png',
            encode_base64=True, base64_prefix='data:image/png;base64')

        body['community_channel'] = {
            'title': 'Airdrops',
            'comm_type': COMMUNITY_TYPE.FORUM.value,
            'icon_img': icon_img,
            'permissions': CommunityChannelPermissions().to_dict()
        }

        controller = CreateChannelController()

        response = self.call_lambda(controller, body)

        self.print_data(response.data)

        assert response.status_code == 201

    @pytest.mark.skip(reason='Done')
    def test_lambda_get_all_channels(self):
        body = self.get_body()
        
        query_params = {
            'title': 'Air',
            'limit': 10,
            'next_cursor': '',
            'sort_order': 'desc'
        }

        controller = GetAllChannelsController()

        response = self.call_lambda(controller, body, query_params=query_params)

        self.print_data(response.data)

        assert response.status_code == 200

    @pytest.mark.skip(reason='Done')
    def test_lambda_get_one_channel(self):
        body = self.get_body()

        query_params = {
            'id': 'd283d22a-2386-4e05-8a46-e8b1fa4a9ba9'
        }

        controller = GetOneChannelController()

        response = self.call_lambda(controller, body, query_params=query_params)

        self.print_data(response.data)

        assert response.status_code == 200

    @pytest.mark.skip(reason='Done')
    def test_lambda_get_one_channel_by_title(self):
        body = self.get_body()

        query_params = {
            'title': 'Air'
        }

        controller = GetOneChannelController()

        response = self.call_lambda(controller, body, query_params=query_params)

        self.print_data(response.data)
        
        assert response.status_code == 200

    @pytest.mark.skip(reason='Done')
    def test_lambda_update_channel(self):
        body = self.get_body()

        icon_img = load_resource('catbeach.png',
            encode_base64=True, base64_prefix='data:image/png;base64')

        body['community_channel'] = {
            'id': '4d5d9c1f-841e-471a-8f21-c6e104765393',
            'title': 'Airdrops UPDATED',
            'icon_img': icon_img,
            'permissions': CommunityChannelPermissions(GUEST=COMMUNITY_PERMISSION.READ).to_dict()
        }
        
        controller = UpdateChannelController()

        response = self.call_lambda(controller, body)

        self.print_data(response.data)
        
        assert response.status_code == 200

    @pytest.mark.skip(reason='Done')
    def test_lambda_delete_channel(self):
        body = self.get_body()

        body['id'] = 'a934dadf-0cca-4fb5-ad04-79c68ade7d61'

        controller = DeleteChannelController()

        response = self.call_lambda(controller, body)

        self.print_data(response.data)

        assert response.status_code == 200

    ### FORUM ###
    @pytest.mark.skip(reason='Done')
    def test_lambda_create_forum_topic(self):
        body = self.get_body()

        icon_img = load_resource('catbeach.png',
            encode_base64=True, base64_prefix='data:image/png;base64')

        body['community_forum_topic'] = {
            'title': 'PORTAL TO BITCOIN',
            'channel_id': '9bfeec54-0a66-4392-887b-ef61ff1af3e7',
            'icon_img': icon_img,
            'first_message': 'bitcoinbitcoinbitcoinbitcoin'
        }

        controller = CreateForumTopicController()

        response = self.call_lambda(controller, body)

        self.print_data(response.data)

        assert response.status_code == 201

    @pytest.mark.skip(reason='Done')
    def test_lambda_get_channel_forum_topics(self):
        body = self.get_body()

        query_params = {
            'channel_id': 'a934dadf-0cca-4fb5-ad04-79c68ade7d61',
            'title': 'PORTAL',
            'limit': 10,
            'next_cursor': '',
            'sort_order': 'desc'
        }

        controller = GetChannelForumTopicsController()

        response = self.call_lambda(controller, body, query_params=query_params)

        self.print_data(response.data)
        
        assert response.status_code == 200

    @pytest.mark.skip(reason='Done')
    def test_lambda_delete_forum_topic(self):
        body = self.get_body()

        body['id'] = 'ee8674ee-caa4-45d8-9f56-91a70a562260'

        controller = DeleteForumTopicController()

        response = self.call_lambda(controller, body)

        self.print_data(response.data)

        assert response.status_code == 200

    @pytest.mark.skip(reason='Done')
    def test_lambda_create_message(self):
        repository = Repository(community_repo=True)

        user = get_requester_user(admin=True)

        community_forum_topic = repository.community_repo.get_one_forum_topic('56bfae93-f92a-4fbe-b95c-d90e06d9af1a')

        now = now_timestamp()

        for i in range(0, 10):
            msg = CommunityMessage(
                id=random_entity_id(),
                channel_id=community_forum_topic.channel_id,
                forum_topic_id=community_forum_topic.id,
                raw_content=f'MSG {str(i)} for {community_forum_topic.id}',
                created_at=now,
                updated_at=now,
                user_id=user['sub']
            )

            repository.community_repo.create_message(msg)

    @pytest.mark.skip(reason='Done')
    def test_lambda_get_forum_topic_message(self):
        body = self.get_body()

        query_params = {
            'channel_id': 'a934dadf-0cca-4fb5-ad04-79c68ade7d61',
            'forum_topic_id': 'ee8674ee-caa4-45d8-9f56-91a70a562260',
            'limit': 100,
            'next_cursor': '',
            'sort_order': 'desc'
        }

        controller = GetCommunityCHannelMessages()

        response = self.call_lambda(controller, body, query_params=query_params)

        self.print_data(response.data)
        
        assert response.status_code == 200