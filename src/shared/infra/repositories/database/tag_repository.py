from boto3.dynamodb.conditions import Attr

from src.shared.infra.external.dynamo_datasource import DynamoDatasource

from src.shared.domain.repositories.tag_repository_interface import ITagRepository

from src.shared.domain.entities.tag import Tag

from src.shared.infra.external.key_formatters import encode_idx_pk

class TagRepositoryDynamo(ITagRepository):
    dynamo: DynamoDatasource
    
    @staticmethod
    def tag_partition_key_format(tag: Tag) -> str:
        return f'TAG#{tag.title}'
    
    @staticmethod
    def tag_partition_key_format_from_title(title: str) -> str:
        return f'TAG#{title}'
    
    @staticmethod
    def tag_sort_key_format() -> str:
        return 'METADATA'

    @staticmethod
    def tag_gsi_entity_get_all_pk() -> str:
        return 'INDEX#TAG'
    
    @staticmethod
    def tag_gsi_entity_get_all_sk(tag: Tag) -> str:
        return f'DATE#{tag.created_at}'
    
    def __init__(self, dynamo: DynamoDatasource):
        self.dynamo = dynamo

    def create(self, tag: Tag) -> Tag:
        item = tag.to_dict()

        item['PK'] = self.tag_partition_key_format(tag)
        item['SK'] = self.tag_sort_key_format()
        item[encode_idx_pk('GSI#ENTITY_GETALL#PK')] = self.tag_gsi_entity_get_all_pk()
        item[encode_idx_pk('GSI#ENTITY_GETALL#SK')] = self.tag_gsi_entity_get_all_sk(tag)

        self.dynamo.put_item(item=item)

        return tag

    def get_all(self, title: str = '', limit: int = 10, \
        last_evaluated_key: str = '', sort_order: str = 'desc') -> dict:
        filter_expression = None

        if title != '':
            filter_expression = Attr('title').contains(title)

        response = self.dynamo.query(
            index_name='GetAllEntities',
            partition_key=self.tag_gsi_entity_get_all_pk(),
            limit=limit,
            exclusive_start_key=last_evaluated_key if last_evaluated_key != '' else None,
            filter_expression=filter_expression,
            scan_index_forward=False if sort_order == 'desc' else True
        )
        
        return {
            'tags': [ Tag.from_dict_static(item) for item in response['items'] ],
            'last_evaluated_key': response.get('last_evaluated_key')
        }