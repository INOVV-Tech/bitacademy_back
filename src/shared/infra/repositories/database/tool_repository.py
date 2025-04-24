from boto3.dynamodb.conditions import Attr

from src.shared.infra.external.dynamo_datasource import DynamoDatasource

from src.shared.domain.repositories.tool_repository_interface import IToolRepository

from src.shared.domain.entities.tool import Tool

from src.shared.infra.external.key_formatters import encode_idx_pk

class ToolRepositoryDynamo(IToolRepository):
    dynamo: DynamoDatasource
    
    @staticmethod
    def tool_partition_key_format(tool: Tool) -> str:
        return f'TOOL#{tool.id}'
    
    @staticmethod
    def tool_partition_key_format_from_id(id: str) -> str:
        return f'TOOL#{id}'
    
    @staticmethod
    def tool_sort_key_format() -> str:
        return 'METADATA'

    @staticmethod
    def tool_gsi_entity_get_all_pk() -> str:
        return 'INDEX#TOOL'
    
    @staticmethod
    def tool_gsi_entity_get_all_sk(tool: Tool) -> str:
        return f'DATE#{tool.created_at}'
    
    def __init__(self, dynamo: DynamoDatasource):
        self.dynamo = dynamo

    def create(self, tool: Tool) -> Tool:
        item = tool.to_dict()

        item['PK'] = self.tool_partition_key_format(tool)
        item['SK'] = self.tool_sort_key_format()
        item[encode_idx_pk('GSI#ENTITY_GETALL#PK')] = self.tool_gsi_entity_get_all_pk()
        item[encode_idx_pk('GSI#ENTITY_GETALL#SK')] = self.tool_gsi_entity_get_all_sk(tool)

        self.dynamo.put_item(item=item)

        return tool

    def get_all(self, tags: list[str] = [], limit: int = 10, \
        last_evaluated_key: str = '', sort_order: str = 'desc') -> dict:
        tags_filter_expression = None

        if len(tags) > 0:
            for tag in tags:
                if tags_filter_expression is None:
                    tags_filter_expression = Attr('tags').contains(tag)
                else:
                    tags_filter_expression |= Attr('tags').contains(tag)

        filter_expression = None

        if tags_filter_expression is not None:
            filter_expression = tags_filter_expression

        response = self.dynamo.query(
            index_name='GetAllEntities',
            partition_key=self.tool_gsi_entity_get_all_pk(),
            limit=limit,
            exclusive_start_key=last_evaluated_key if last_evaluated_key != '' else None,
            filter_expression=filter_expression,
            scan_index_forward=False if sort_order == 'desc' else True
        )
        
        return {
            'tools': [ Tool.from_dict_static(item) for item in response['items'] ],
            'last_evaluated_key': response.get('last_evaluated_key')
        }
    
    def get_one(self, id: str) -> Tool | None:
        data = self.dynamo.get_item(
            partition_key=self.tool_partition_key_format_from_id(id),
            sort_key=self.tool_sort_key_format()
        )

        return Tool.from_dict_static(data['Item']) if 'Item' in data else None
    
    def get_one_by_title(self, title: str) -> Tool | None:
        filter_expression = Attr('title').contains(title)

        data = self.dynamo.query(
            index_name='GetAllEntities',
            partition_key=self.tool_gsi_entity_get_all_pk(),
            filter_expression=filter_expression
        )
        
        items = data['items']

        return Tool.from_dict_static(items[0]) if len(items) > 0 else None

    def update(self, tool: Tool) -> Tool:
        item = tool.to_dict()

        item['PK'] = self.tool_partition_key_format(tool)
        item['SK'] = self.tool_sort_key_format()
        item[encode_idx_pk('GSI#ENTITY_GETALL#PK')] = self.tool_gsi_entity_get_all_pk()
        item[encode_idx_pk('GSI#ENTITY_GETALL#SK')] = self.tool_gsi_entity_get_all_sk(tool)

        self.dynamo.put_item(item=item)
        
        return tool

    def delete(self, id: str) -> Tool | None:
        data = self.dynamo.delete_item(
            partition_key=self.tool_partition_key_format_from_id(id),
            sort_key=self.tool_sort_key_format()
        )

        if 'Attributes' not in data:
            return None
        
        return Tool.from_dict_static(data['Attributes'])