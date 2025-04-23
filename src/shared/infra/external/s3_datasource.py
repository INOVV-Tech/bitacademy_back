import boto3

from src.shared.environments import Environments

class S3Datasource:
    def __init__(self, bucket_name: str, region: str, endpoint_url: str = None):
        session = boto3.Session(region_name=region)

        if Environments.persist_local:
            endpoint_url = 'http://localhost:4566' # localstack

        self.s3_resource = session.resource('s3', endpoint_url=endpoint_url)

        self.bucket = self.s3_resource.Bucket(bucket_name)
        self.bucket_name = bucket_name

    def debug_bucket(self) -> None:
        result = [ f'Bucket name = {self.bucket_name}' ]

        for obj in self.bucket.objects.all():
            result.append(f'- {obj.key} ({obj.size} bytes)')
        
        print('\n'.join(result))