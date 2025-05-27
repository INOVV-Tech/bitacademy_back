from tests.s3.upload_flow import init_file_api
from tests.crud.vip_subscription.stripe_flow import init_stripe_webhook

from populate import populate_primary_entities

if __name__ == '__main__':
    # init_file_api()
    # init_stripe_webhook()

    populate_primary_entities(news=True)
    pass