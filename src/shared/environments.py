import os
from enum import Enum
from dotenv import load_dotenv

class STAGE(Enum):
    TEST = 'TEST'
    DEV = 'DEV'
    HOMOLOG = 'HOMOLOG'
    PROD = 'PROD'

class Environments:
    load_dotenv()
    
    stage: STAGE = STAGE(os.environ.get('STAGE', STAGE.TEST.value))
    region: str = os.environ.get('AWS_REGION', 'sa-east-1')
    user_pool_id: str = os.environ.get('USER_POOL_ID', '')
    user_pool_arn: str = os.environ.get('USER_POOL_ARN', '')
    app_client_id: str = os.environ.get('APP_CLIENT_ID', '')
    bucket_name: str = os.environ.get('BUCKET_NAME', '')
    dynamo_table_name: str = os.environ.get('DYNAMO_TABLE_NAME', '')

    persist_local: str = int(os.environ.get('PERSIST_LOCAL', '0')) == 1
    dynamo_local_key_id: str = os.environ.get('DYNAMO_LOCAL_KEY_ID', '')
    dynamo_local_access_key: str = os.environ.get('DYNAMO_LOCAL_ACCESS_KEY', '')

    cmc_api_key: str = os.environ.get('CMC_API_KEY', '')

    stripe_pubkey: str = os.environ.get('STRIPE_PUBKEY', '')
    stripe_privkey: str = os.environ.get('STRIPE_PRIVKEY', '')
    stripe_webhook_privkey: str = os.environ.get('STRIPE_WEBHOOK_PRIVKEY', '')

    @staticmethod
    def reload():
        Environments.stage = STAGE(os.environ.get('STAGE', STAGE.TEST.value))
        Environments.region = os.environ.get('AWS_REGION', 'sa-east-1')
        Environments.user_pool_id = os.environ.get('USER_POOL_ID', '')
        Environments.user_pool_arn = os.environ.get('USER_POOL_ARN', '')
        Environments.app_client_id = os.environ.get('APP_CLIENT_ID', '')
        Environments.bucket_name = os.environ.get('BUCKET_NAME', '')
        Environments.dynamo_table_name = os.environ.get('DYNAMO_TABLE_NAME', '')

        Environments.persist_local = int(os.environ.get('PERSIST_LOCAL', '0')) == 1
        Environments.dynamo_local_key_id = os.environ.get('DYNAMO_LOCAL_KEY_ID', '')
        Environments.dynamo_local_access_key = os.environ.get('DYNAMO_LOCAL_ACCESS_KEY', '')

        Environments.cmc_api_key = os.environ.get('CMC_API_KEY', '')

        Environments.stripe_pubkey = os.environ.get('STRIPE_PUBKEY', '')
        Environments.stripe_privkey = os.environ.get('STRIPE_PRIVKEY', '')
        Environments.stripe_webhook_privkey = os.environ.get('STRIPE_WEBHOOK_PRIVKEY', '')