import json
import pytest

from tests.common import load_app_env, get_requester_user

load_app_env()

from src.shared.helpers.external_interfaces.http_models import HttpRequest

from src.shared.infra.repositories.repository import Repository
from src.shared.infra.repositories.dtos.auth_authorizer_dto import AuthAuthorizerDTO

from src.shared.domain.enums.vip_level import VIP_LEVEL
from src.shared.domain.entities.vip_subscription import VipSubscription

from src.shared.utils.time import now_timestamp

class Test_VipSubscriptionLambda:
    def print_data(self, data: dict) -> None:
        print(json.dumps(data, indent=4, ensure_ascii=False))

    def get_body(self):
        return {
            'requester_user': get_requester_user(admin=True)
        }
    
    def call_lambda(self, controller, body={}, headers={}, query_params={}):
        request = HttpRequest(body=body, headers=headers, query_params=query_params)

        return controller.execute(request)

    @pytest.mark.skip(reason='Done')
    def test_lambda_create(self):
        repository = Repository(vip_subscription_repo=True)

        requester_user = AuthAuthorizerDTO.from_api_gateway(get_requester_user(admin=True))

        created_at = now_timestamp()
        expire_at = created_at + 43200

        vip_subscription = VipSubscription(
            user_id=requester_user.user_id,
            vip_level=VIP_LEVEL.VIP_1,
            created_at=created_at,
            expire_at=expire_at
        )

        repository.vip_subscription_repo.create(vip_subscription)

        assert True