import json
import pytest

from tests.common import load_app_env, load_resource

load_app_env()

from src.shared.infra.object_storage.file import ObjectStorageFile

class Test_S3File:
    def print_data(self, data: dict) -> None:
        print(json.dumps(data, indent=4, ensure_ascii=False))
    
    # @pytest.mark.skip(reason='Done')
    def test_file_verification(self):
        cover_img = load_resource('catbeach.png',
            encode_base64=True, base64_prefix='data:image/png;base64')

        file = ObjectStorageFile.from_base64_data(cover_img)

        is_valid_img = file.verify_base64_image()

        print('is valid IMG', is_valid_img)
        print('mime type', file.mime_type)

        is_valid_video = file.verify_base64_video()

        print('is valid VIDEO', is_valid_video)
        print('mime type', file.mime_type)

        assert True