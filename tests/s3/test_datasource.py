import json
import pytest

from tests.common import load_app_env, load_resource

load_app_env()

from src.shared.environments import Environments

from src.shared.infra.external.s3_datasource import S3Datasource

# aws s3api create-bucket --bucket bitacads3 --region us-east-1 --endpoint-url=http://localhost:4566

class Test_S3Datasource:
    def print_data(self, data: dict) -> None:
        print(json.dumps(data, indent=4, ensure_ascii=False))

    def get_datasource(self) -> S3Datasource:
        return S3Datasource(
            bucket_name=Environments.bucket_name,
            region=Environments.region
        )
    
    @pytest.mark.skip(reason='Done')
    def test_ping_bucket(self):
        s3_datasource = self.get_datasource()

        s3_datasource.debug_bucket()

        assert True

    @pytest.mark.skip(reason='Done')
    def test_upload_base64(self):
        s3_datasource = self.get_datasource()

        cover_img = load_resource('free_resource_cover_img.jpg', encode_base64=True, base64_prefix='')

        print('cover_img', cover_img[0:200])
        
        resp = s3_datasource.upload_base64_file('cover_img.jpg', cover_img, mime_type='image/jpeg')

        self.print_data(resp)

        assert 'error' not in resp

        resp = s3_datasource.read_base64_file('cover_img.jpg')

        assert 'error' not in resp

        resp = s3_datasource.upload_base64_file('cover_img.jpg', resp['data'], mime_type='image/jpeg')

        self.print_data(resp)

        assert 'error' not in resp