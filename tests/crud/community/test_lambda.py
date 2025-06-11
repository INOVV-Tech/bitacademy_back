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

        body['id'] = '27e00ce9-b2ba-4344-9737-65e7b0d9dbcd'

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
            'channel_id': 'edd8c552-d089-471b-8662-1dd8aa42e282',
            'icon_img': icon_img
        }

        controller = CreateForumTopicController()

        response = self.call_lambda(controller, body)

        self.print_data(response.data)

        assert response.status_code == 201

    @pytest.mark.skip(reason='Done')
    def test_lambda_get_channel_forum_topics(self):
        body = self.get_body()

        query_params = {
            'channel_id': 'edd8c552-d089-471b-8662-1dd8aa42e282',
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

        body['id'] = '3da9ee73-e006-4a8c-8c14-5960cd00ac74'

        controller = DeleteForumTopicController()

        response = self.call_lambda(controller, body)

        self.print_data(response.data)

        assert response.status_code == 200

    @pytest.mark.skip(reason='Done')
    def test_lambda_create_message(self):
        repository = Repository(community_repo=True)

        user = get_requester_user(admin=True)

        community_forum_topic = repository.community_repo.get_one_forum_topic('382a34b9-9267-4574-96b9-e77814ce1a42')

        now = now_timestamp()

        msg = CommunityMessage(
            id=random_entity_id(),
            channel_id=community_forum_topic.channel_id,
            forum_topic_id=community_forum_topic.id,
            raw_content='testettestetstestetestee',
            created_at=now,
            updated_at=now,
            user_id=user['sub']
        )

        repository.community_repo.create_message(msg)