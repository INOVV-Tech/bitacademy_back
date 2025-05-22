import os
from populate.common import load_app_env, load_resource

load_app_env()

from src.shared.infra.repositories.repository import Repository

from src.shared.domain.entities.news import News
from src.shared.domain.entities.tag import Tag

USER_ID = os.environ.get('POPULATE_USER_ID')

def populate_news():
    repository = Repository(news_repo=True, tag_repo=True)

    tags = [ 'Mercado' ]

    template = {
        'title': 'Ethereum e Bitcoin disparam e geram otimismo no mercado.',
        'header': 'Os dois maiores criptoativos do mundo, Bitcoin (BTC) e Ethereum (ETH), registraram uma forte valorização nas últimas 24 horas, impulsionados por um crescente otimismo do mercado financeiro. O BTC ultrapassou a marca de US$ 75.000, enquanto o ETH alcançou os US$ 4.500, níveis que não eram vistos há meses.',
        'content': 'O principal fator por trás dessa alta foi a divulgação de dados econômicos positivos nos Estados Unidos, que indicam uma possível flexibilização na política monetária do Federal Reserve. A perspectiva de cortes nas taxas de juros tem levado investidores a migrarem para ativos de maior risco, como criptomoedas. Além disso, o mercado foi influenciado pelo crescimento da adoção institucional das criptos. Grandes empresas e fundos de investimento anunciaram novas aquisições de BTC e ETH para suas carteiras, reforçando a confiança dos investidores de varejo. Outro fator relevante foi o avanço nas aprovações de ETFs de Ethereum à vista, que podem trazer um novo fluxo de capital para o mercado. A Comissão de Valores Mobiliários dos EUA (SEC) sinalizou que pode aprovar tais produtos financeiros em breve, o que impulsionou ainda mais a demanda pelo ETH. Especialistas apontam que, se o atual ciclo de alta continuar, novas máximas históricas podem ser alcançadas nos próximos meses. No entanto, analistas alertam para a volatilidade do mercado cripto e recomendam cautela aos investidores. Fique ligado para mais atualizações sobre o mercado de criptomoedas!',
        'tags': tags,
        'vip_level': 1,
        'cover_img': load_resource('news-cover.png',
            encode_base64=True, base64_prefix='data:image/png;base64'),
        'card_img': load_resource('bitcoin-placeholder.png',
            encode_base64=True, base64_prefix='data:image/png;base64')
    }
    
    for i in range(20):
        (error, news) = News.from_request_data(template, USER_ID)
        
        s3_datasource = repository.get_s3_datasource()

        upload_cover_resp = news.cover_img.store_in_s3(s3_datasource)
        upload_card_resp = news.card_img.store_in_s3(s3_datasource)
        
        repository.news_repo.create(news)

        print(f'Populated {(i + 1)} news')

    tags = Tag.from_string_list(tags)

    for tag in tags:
        repository.tag_repo.create(tag)

    print('Populated all news')
