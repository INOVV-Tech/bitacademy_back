from boto3.dynamodb.conditions import Attr

from src.shared.infra.external.dynamo_datasource import DynamoDatasource

from src.shared.domain.repositories.course_repository_interface import ICourseRepository

from src.shared.domain.enums.vip_level import VIP_LEVEL
from src.shared.domain.entities.course import Course

from src.shared.infra.external.key_formatters import encode_idx_pk

class CourseRepositoryDynamo(ICourseRepository):
    dynamo: DynamoDatasource
    
    @staticmethod
    def course_partition_key_format(course: Course) -> str:
        return f'COURSE#{course.id}'
    
    @staticmethod
    def course_partition_key_format_from_id(id: str) -> str:
        return f'COURSE#{id}'
    
    @staticmethod
    def course_sort_key_format() -> str:
        return 'METADATA'

    @staticmethod
    def course_gsi_entity_get_all_pk() -> str:
        return 'INDEX#COURSE'
    
    @staticmethod
    def course_gsi_entity_get_all_sk(course: Course) -> str:
        return f'DATE#{course.created_at}'
    
    def __init__(self, dynamo: DynamoDatasource):
        self.dynamo = dynamo

    def create(self, course: Course) -> Course:
        item = course.to_dict()

        item['PK'] = self.course_partition_key_format(course)
        item['SK'] = self.course_sort_key_format()
        item[encode_idx_pk('GSI#ENTITY_GETALL#PK')] = self.course_gsi_entity_get_all_pk()
        item[encode_idx_pk('GSI#ENTITY_GETALL#SK')] = self.course_gsi_entity_get_all_sk(course)

        self.dynamo.put_item(item=item)

        return course

    def get_all(self, tags: list[str] = [], vip_level: VIP_LEVEL | None = None, \
        limit: int = 10, last_evaluated_key: str = '', sort_order: str = 'desc') -> dict:
        tags_filter_expression = None

        if len(tags) > 0:
            for tag in tags:
                if tags_filter_expression is None:
                    tags_filter_expression = Attr('tags').contains(tag)
                else:
                    tags_filter_expression |= Attr('tags').contains(tag)

        vip_filter_expression = None

        if vip_level is not None:
            vip_filter_expression = Attr('vip_level').lte(vip_level.value)

        filter_expression = None

        if tags_filter_expression is not None:
            filter_expression = tags_filter_expression

        if vip_filter_expression is not None:
            if filter_expression is None:
                filter_expression = vip_filter_expression
            else:
                filter_expression &= vip_filter_expression

        response = self.dynamo.query(
            index_name='GetAllEntities',
            partition_key=self.course_gsi_entity_get_all_pk(),
            limit=limit,
            exclusive_start_key=last_evaluated_key if last_evaluated_key != '' else None,
            filter_expression=filter_expression,
            scan_index_forward=False if sort_order == 'desc' else True
        )
        
        return {
            'courses': [ Course.from_dict_static(item) for item in response['items'] ],
            'last_evaluated_key': response.get('last_evaluated_key')
        }
    
    def get_one(self, id: str) -> Course | None:
        data = self.dynamo.get_item(
            partition_key=self.course_partition_key_format_from_id(id),
            sort_key=self.course_sort_key_format()
        )

        return Course.from_dict_static(data['Item']) if 'Item' in data else None
    
    def get_one_by_title(self, title: str) -> Course | None:
        filter_expression = Attr('title').contains(title)

        data = self.dynamo.query(
            index_name='GetAllEntities',
            partition_key=self.course_gsi_entity_get_all_pk(),
            filter_expression=filter_expression
        )
        
        items = data['items']
        
        return Course.from_dict_static(items[0]) if len(items) > 0 else None

    def update(self, course: Course) -> Course:
        item = course.to_dict()

        item['PK'] = self.course_partition_key_format(course)
        item['SK'] = self.course_sort_key_format()
        item[encode_idx_pk('GSI#ENTITY_GETALL#PK')] = self.course_gsi_entity_get_all_pk()
        item[encode_idx_pk('GSI#ENTITY_GETALL#SK')] = self.course_gsi_entity_get_all_sk(course)

        self.dynamo.put_item(item=item)
        
        return course

    def delete(self, id: str) -> Course | None:
        data = self.dynamo.delete_item(
            partition_key=self.course_partition_key_format_from_id(id),
            sort_key=self.course_sort_key_format()
        )

        if 'Attributes' not in data:
            return None

        return Course.from_dict_static(data['Attributes'])