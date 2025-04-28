from boto3.dynamodb.conditions import Attr

from src.shared.infra.external.dynamo_datasource import DynamoDatasource

from src.shared.domain.repositories.free_material_repository_interface import IFreeMaterialRepository
from src.shared.domain.entities.free_material import FreeMaterial

from src.shared.infra.external.key_formatters import encode_idx_pk

class FreeMaterialRepositoryDynamo(IFreeMaterialRepository):
    dynamo: DynamoDatasource

    @staticmethod
    def free_material_partition_key_format(free_material: FreeMaterial) -> str:
        return f'FREE_MATERIAL#{free_material.id}'
    
    @staticmethod
    def free_material_partition_key_format_from_id(id: str) -> str:
        return f'FREE_MATERIAL#{id}'
    
    @staticmethod
    def free_material_sort_key_format() -> str:
        return 'METADATA'
    
    @staticmethod
    def free_material_gsi_entity_get_all_pk() -> str:
        return 'INDEX#FREE_MATERIAL'
    
    @staticmethod
    def free_material_gsi_entity_get_all_sk(free_material: FreeMaterial) -> str:
        return f'DATE#{free_material.created_at}'
    
    def __init__(self, dynamo: DynamoDatasource):
        self.dynamo = dynamo

    def create(self, free_material: FreeMaterial) -> FreeMaterial:
        item = free_material.to_dict()

        item['PK'] = self.free_material_partition_key_format(free_material)
        item['SK'] = self.free_material_sort_key_format()
        item[encode_idx_pk('GSI#ENTITY_GETALL#PK')] = self.free_material_gsi_entity_get_all_pk()
        item[encode_idx_pk('GSI#ENTITY_GETALL#SK')] = self.free_material_gsi_entity_get_all_sk(free_material)

        self.dynamo.put_item(item=item)

        return free_material

    def get_all(self, title: str = '', tags: list[str] = [], limit: int = 10, last_evaluated_key: str = '', \
        sort_order: str = 'desc') -> dict:
        filter_expressions = []

        if title != '':
            filter_expressions.append(Attr('title').contains(title))

        if len(tags) > 0:
            tags_filter_expression = None

            for tag in tags:
                if tags_filter_expression is None:
                    tags_filter_expression = Attr('tags').contains(tag)
                else:
                    tags_filter_expression |= Attr('tags').contains(tag)

            filter_expressions.append(tags_filter_expression)

        filter_expression= None

        if len(filter_expressions) > 0:
            for f_exp in filter_expressions:
                if filter_expression is None:
                    filter_expression = f_exp
                else:
                    filter_expression &= f_exp

        response = self.dynamo.query(
            index_name='GetAllEntities',
            partition_key=self.free_material_gsi_entity_get_all_pk(),
            limit=limit,
            exclusive_start_key=last_evaluated_key if last_evaluated_key != '' else None,
            filter_expression=filter_expression,
            scan_index_forward=False if sort_order == 'desc' else True
        )
        
        return {
            'free_materials': [ FreeMaterial.from_dict_static(item) for item in response['items'] ],
            'last_evaluated_key': response.get('last_evaluated_key')
        }
    
    def get_one(self, id: str) -> FreeMaterial | None:
        data = self.dynamo.get_item(
            partition_key=self.free_material_partition_key_format_from_id(id),
            sort_key=self.free_material_sort_key_format()
        )

        return FreeMaterial.from_dict_static(data['Item']) if 'Item' in data else None
    
    def get_one_by_title(self, title: str) -> FreeMaterial | None:
        filter_expression = Attr('title').contains(title)

        data = self.dynamo.query(
            index_name='GetAllEntities',
            partition_key=self.free_material_gsi_entity_get_all_pk(),
            filter_expression=filter_expression
        )

        items = data['items']

        return FreeMaterial.from_dict_static(items[0]) if len(items) > 0 else None

    def update(self, free_material: FreeMaterial) -> FreeMaterial:
        item = free_material.to_dict()

        item['PK'] = self.free_material_partition_key_format(free_material)
        item['SK'] = self.free_material_sort_key_format()
        item[encode_idx_pk('GSI#ENTITY_GETALL#PK')] = self.free_material_gsi_entity_get_all_pk()
        item[encode_idx_pk('GSI#ENTITY_GETALL#SK')] = self.free_material_gsi_entity_get_all_sk(free_material)

        self.dynamo.put_item(item=item)

        return free_material

    def delete(self, id: str) -> FreeMaterial | None:
        data = self.dynamo.delete_item(
            partition_key=self.free_material_partition_key_format_from_id(id),
            sort_key=self.free_material_sort_key_format()
        )

        if 'Attributes' not in data:
            return None

        return FreeMaterial.from_dict_static(data['Attributes'])