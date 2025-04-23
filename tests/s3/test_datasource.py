import json
import pytest

from tests.common import load_app_env

load_app_env()

from src.shared.environments import Environments

from src.shared.infra.external.s3_datasource import S3Datasource

# aws s3api create-bucket --bucket bitacads3 --region us-east-1 --endpoint-url=http://localhost:4566

class Test_S3Datasource:
    def print_data(self, data: dict) -> None:
        print(json.dumps(data, indent=4, ensure_ascii=False))
    
    # @pytest.mark.skip(reason='Done')
    def test_bucket(self):
        s3_datasource = S3Datasource(
            bucket_name=Environments.bucket_name,
            region=Environments.region
        )

        s3_datasource.debug_bucket()

        assert True