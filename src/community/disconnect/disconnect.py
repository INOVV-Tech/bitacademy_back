class Controller:
    pass

class Usecase:
    pass

def lambda_handler(event, context) -> dict:
    connection_id = event.get('requestContext', {}) \
        .get('connectionId', '')

    print(f'Disconnecting: {connection_id}')
    
    return { 'statusCode': 200 }