import json
import boto3
from decimal import Decimal
from boto3.dynamodb.conditions import Key

from src.shared.environments import Environments

class DynamoDatasource:
    def __init__(self, dynamo_table_name: str, region: str, endpoint_url: str = None):
        """
        Inicializa o datasource.
        :param dynamo_table_name: Nome da tabela do DynamoDB.
        :param region: Região AWS.
        :param endpoint_url: URL opcional para endpoint local/teste.
        """
        session = boto3.Session(region_name=region)

        if Environments.persist_local:
            self.dynamo_resource = session.resource('dynamodb', 
                endpoint_url=endpoint_url,
                aws_access_key_id=Environments.dynamo_local_key_id,
                aws_secret_access_key=Environments.dynamo_local_access_key
            )
        else:
            self.dynamo_resource = session.resource('dynamodb', endpoint_url=endpoint_url)

        self.dynamo_table = self.dynamo_resource.Table(dynamo_table_name)

        self.key_mapping = {
            'main_table': { 'partition_key': 'PK', 'sort_key': 'SK' },
            'gsis': {
                'AllEntitiesMetadata': {
                    'partition_key': 'GSI#ENTITY',
                    'sort_key': 'created_at',
                }
            }
        }

    def _get_key_config(self, index_name=None):
        """
        Retorna a configuração de chave para a tabela principal ou um GSI específico.
        """
        if index_name:
            if index_name not in self.key_mapping['gsis']:
                raise ValueError(f'O índice \'{index_name}\' não está configurado.')
            
            return self.key_mapping['gsis'][index_name]
        
        return self.key_mapping['main_table']

    def put_item(self, item: dict):
        """
        Insere ou atualiza um item na tabela principal.
        """
        item = self._parse_float_to_decimal(item)

        return self.dynamo_table.put_item(Item=item)

    def get_item(self, partition_key: str, sort_key: str = None):
        """
        Busca um item pela tabela principal.
        """
        key_config = self._get_key_config()

        key = { key_config['partition_key']: partition_key }

        if sort_key:
            key[key_config['sort_key']] = sort_key

        return self.dynamo_table.get_item(Key=key)

    def query(
        self,
        partition_key: str,
        sort_key=None,
        index_name=None,
        filter_expression=None,
        limit=None,
        exclusive_start_key=None
    ):
        """
        Realiza uma consulta na tabela principal ou em um GSI com suporte a filtros e paginação.
        """
        key_config = self._get_key_config(index_name=index_name)

        key_condition = Key(key_config['partition_key']).eq(partition_key)

        if sort_key and key_config.get('sort_key'):
            key_condition &= Key(key_config['sort_key']).eq(sort_key)

        kwargs = {
            'KeyConditionExpression': key_condition,
        }

        if index_name:
            kwargs['IndexName'] = index_name
        
        if filter_expression:
            kwargs['FilterExpression'] = filter_expression

        if limit:
            kwargs['Limit'] = limit
        
        if exclusive_start_key:
            kwargs['ExclusiveStartKey'] = exclusive_start_key

        response = self.dynamo_table.query(**kwargs)

        return {
            'items': response.get('Items', []),
            'last_evaluated_key': response.get('LastEvaluatedKey')
        }

    def scan_items(self, filter_expression=None, limit=None, exclusive_start_key=None):
        """
        Faz um scan na tabela principal com suporte a filtros e paginação.
        """
        kwargs = {}

        if filter_expression:
            kwargs['FilterExpression'] = filter_expression
        
        if limit:
            kwargs['Limit'] = limit
        
        if exclusive_start_key:
            kwargs['ExclusiveStartKey'] = exclusive_start_key

        response = self.dynamo_table.scan(**kwargs)

        return {
            'items': response.get('Items', []),
            'last_evaluated_key': response.get('LastEvaluatedKey')
        }

    def delete_item(self, partition_key: str, sort_key: str = None):
        """
        Remove um item da tabela principal.
        """
        key_config = self._get_key_config()
        
        key = { key_config['partition_key']: partition_key }

        if sort_key:
            key[key_config['sort_key']] = sort_key
        
        return self.dynamo_table.delete_item(Key=key)

    @staticmethod
    def _parse_float_to_decimal(item):
        """
        Converte valores float para Decimal.
        """
        return json.loads(json.dumps(item), parse_float=Decimal)