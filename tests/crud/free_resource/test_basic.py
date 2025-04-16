import pytest

from src.shared.infra.repositories.repository import Repository

from tests.common import get_requester_user

class Test_FreeResource:
    def get_body(self):
        return {
            'requests_user': get_requester_user()
        }

    def test_lambda_create(self):
        body = self.get_body()

        print('body', body)

        assert True

    def test_lambda_get_all(self):
        assert True

    def test_lambda_get_one(self):
        assert True

    def test_lambda_update(self):
        assert True

    def test_lambda_delete(self):
        assert True