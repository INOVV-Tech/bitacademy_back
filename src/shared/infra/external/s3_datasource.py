import boto3
import base64

from src.shared.environments import Environments

class S3Datasource:
    def __init__(self, bucket_name: str, region: str, endpoint_url: str = None):
        self.region = region
        
        session = boto3.Session(region_name=region)

        if Environments.persist_local:
            endpoint_url = 'http://localhost:4566' # localstack

        self.endpoint_url = endpoint_url

        self.s3_resource = session.resource('s3', endpoint_url=endpoint_url)

        self.bucket = self.s3_resource.Bucket(bucket_name)
        self.bucket_name = bucket_name

    def debug_bucket(self) -> None:
        result = [ f'Bucket name = {self.bucket_name}' ]

        for obj in self.bucket.objects.all():
            result.append(f'- {obj.key} ({obj.size} bytes)')
        
        print('\n'.join(result))

    def get_s3_object(self, s3_key: str):
        return self.s3_resource.Object(self.bucket_name, s3_key)

    def upload_base64_file(self, s3_key: str, base64_data: str, mime_type: str = '') -> dict:
        try:
            response = self.get_s3_object(s3_key).put(
                Body=base64.b64decode(base64_data), 
                ContentType=mime_type
            )

            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                return { 'url': self.get_file_url(s3_key) }
        except:
            pass
        
        return { 'error': f'S3 "upload_base64_file" falhou com a chave "{s3_key}"' }

    def get_file_url(self, s3_key: str) -> str:
        if self.endpoint_url is not None:
            return f'{self.endpoint_url}/{self.bucket_name}/{s3_key}'

        return f'https://{self.bucket_name}.s3.{self.region}.amazonaws.com/{s3_key}'
    
    def read_base64_file(self, s3_key: str) -> dict:
        try:
            s3_obj = self.get_s3_object(s3_key)

            base64_bytes = s3_obj.get()['Body'].read()
            base64_bytes = base64.b64encode(base64_bytes)
            
            return { 'data': base64_bytes.decode('utf8') }
        except:
            pass

        return { 'error': f'S3 "read_base64_file" falhou com a chave "{s3_key}"' }