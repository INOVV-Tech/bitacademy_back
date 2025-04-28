from boto3.dynamodb.conditions import Attr

from src.shared.infra.external.dynamo_datasource import DynamoDatasource

from src.shared.domain.repositories.news_repository_interface import INewsRepository

from src.shared.domain.enums.vip_level import VIP_LEVEL
from src.shared.domain.entities.news import News

from src.shared.infra.external.key_formatters import encode_idx_pk

class NewsRepositoryDynamo(INewsRepository):
    dynamo: DynamoDatasource
    
    @staticmethod
    def news_partition_key_format(news: News) -> str:
        return f'NEWS#{news.id}'
    
    @staticmethod
    def news_partition_key_format_from_id(id: str) -> str:
        return f'NEWS#{id}'
    
    @staticmethod
    def news_sort_key_format() -> str:
        return 'METADATA'
    
    @staticmethod
    def news_gsi_entity_get_all_pk() -> str:
        return 'INDEX#NEWS'
    
    @staticmethod
    def news_gsi_entity_get_all_sk(news: News) -> str:
        return f'DATE#{news.created_at}'
    
    def __init__(self, dynamo: DynamoDatasource):
        self.dynamo = dynamo

    def create(self, news: News) -> News:
        item = news.to_dict()

        item['PK'] = self.news_partition_key_format(news)
        item['SK'] = self.news_sort_key_format()
        item[encode_idx_pk('GSI#ENTITY_GETALL#PK')] = self.news_gsi_entity_get_all_pk()
        item[encode_idx_pk('GSI#ENTITY_GETALL#SK')] = self.news_gsi_entity_get_all_sk(news)

        self.dynamo.put_item(item=item)

        return news

    def get_all(self, title: str = '', tags: list[str] = [], vip_level: VIP_LEVEL | None = None, \
        limit: int = 10, last_evaluated_key: str = '', sort_order: str = 'desc') -> dict:
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

        if vip_level is not None:
            filter_expressions.append(Attr('vip_level').lte(vip_level.value))

        filter_expression= None

        if len(filter_expressions) > 0:
            for f_exp in filter_expressions:
                if filter_expression is None:
                    filter_expression = f_exp
                else:
                    filter_expression &= f_exp

        response = self.dynamo.query(
            index_name='GetAllEntities',
            partition_key=self.news_gsi_entity_get_all_pk(),
            limit=limit,
            exclusive_start_key=last_evaluated_key if last_evaluated_key != '' else None,
            filter_expression=filter_expression,
            scan_index_forward=False if sort_order == 'desc' else True
        )
        
        return {
            'news_list': [ News.from_dict_static(item) for item in response['items'] ],
            'last_evaluated_key': response.get('last_evaluated_key')
        }
    
    def get_one(self, id: str) -> News | None:
        data = self.dynamo.get_item(
            partition_key=self.news_partition_key_format_from_id(id),
            sort_key=self.news_sort_key_format()
        )

        return News.from_dict_static(data['Item']) if 'Item' in data else None
    
    def get_one_by_title(self, title: str) -> News | None:
        filter_expression = Attr('title').contains(title)

        data = self.dynamo.query(
            index_name='GetAllEntities',
            partition_key=self.news_gsi_entity_get_all_pk(),
            filter_expression=filter_expression
        )

        items = data['items']

        return News.from_dict_static(items[0]) if len(items) > 0 else None

    def update(self, news: News) -> News:
        item = news.to_dict()

        item['PK'] = self.news_partition_key_format(news)
        item['SK'] = self.news_sort_key_format()
        item[encode_idx_pk('GSI#ENTITY_GETALL#PK')] = self.news_gsi_entity_get_all_pk()
        item[encode_idx_pk('GSI#ENTITY_GETALL#SK')] = self.news_gsi_entity_get_all_sk(news)

        self.dynamo.put_item(item=item)
        
        return news

    def delete(self, id: str) -> News | None:
        data = self.dynamo.delete_item(
            partition_key=self.news_partition_key_format_from_id(id),
            sort_key=self.news_sort_key_format()
        )

        if 'Attributes' not in data:
            return None

        return News.from_dict_static(data['Attributes'])