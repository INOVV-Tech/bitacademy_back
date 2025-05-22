import os
from populate.common import load_app_env, load_resource

load_app_env()

from src.shared.infra.repositories.repository import Repository

from src.shared.domain.entities.tool import Tool
from src.shared.domain.entities.tag import Tag

USER_ID = os.environ.get('POPULATE_USER_ID')

def populate_tools():
    repository = Repository(tool_repo=True, tag_repo=True)

    tags = [ 'App' ]

    template = {
        'title': 'Ferramenta 1',
        'description': 'Ferramenta inovadora para o monitoramento e gestão de criptomoedas, oferecendo dados em tempo real sobre preços, variações de mercado e tendências. Com uma interface intuitiva, permite que usuários acompanhem gráficos detalhados, configurem alertas personalizados e gerenciem seus portfólios de investimentos com segurança. Ideal para traders e investidores, a plataforma facilita a tomada de decisões estratégicas no dinâmico mercado de criptoativos.App com segurança e efetividade garantida.',
        'external_url': 'https://www.youtube.com/',
        'cover_img': load_resource('tool-cover.jpg',
            encode_base64=True, base64_prefix='data:image/jpg;base64'),
        'tags': tags
    }
    
    for i in range(20):
        (error, tool) = Tool.from_request_data(template, USER_ID)
        
        s3_datasource = repository.get_s3_datasource()

        upload_cover_resp = tool.cover_img.store_in_s3(s3_datasource)
        
        repository.tool_repo.create(tool)

        print(f'Populated {(i + 1)} tool')

    tags = Tag.from_string_list(tags)

    for tag in tags:
        repository.tag_repo.create(tag)

    print('Populated tools')
