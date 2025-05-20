from populate.common import load_app_env, load_resource

load_app_env()

from src.shared.infra.repositories.repository import Repository

from src.shared.domain.entities.free_material import FreeMaterial
from src.shared.domain.entities.tag import Tag

USER_ID = 'e34c5a0a-e061-7081-168a-3d82472dc6c3'

def populate_free_materials():
    repository = Repository(free_material_repo=True, tag_repo=True)

    cover_img = load_resource('bitcoin-placeholder.png',
            encode_base64=True, base64_prefix='data:image/png;base64')
    
    tags = [ 'Iniciantes', 'Mercado' ]

    template = {
        'title': 'O que são criptomoedas? Realmente valem à pena?',
        'description': 'O que são Criptomoedas? Imagine uma revolução no mundo financeiro, uma nova forma de dinheiro que não só redefine como realizamos transações, mas também nos dá o poder de controle total sobre nossos ativos. Esse avanço é representado pelas criptomoedas, um tipo de dinheiro puramente digital que utiliza uma tecnologia extremamente sofisticada, conhecida como criptografia, para garantir transações seguras e, na maioria das vezes, anônimas. Ao contrário das moedas tradicionais, como o real ou o dólar, que você pode segurar em mãos, as criptomoedas existem somente no ambiente digital.',
        'cover_img': cover_img,
        'external_url': 'https://www.binance.com/pt-BR/trade/BTC_USDT?theme=dark&type=spot',
        'tags': tags
    }
    
    for i in range(20):
        (error, free_material) = FreeMaterial.from_request_data(template, USER_ID)

        s3_datasource = repository.get_s3_datasource()

        upload_resp = free_material.cover_img.store_in_s3(s3_datasource)

        repository.free_material_repo.create(free_material)

        print(f'Populated {(i + 1)} free material')

    tags = Tag.from_string_list(tags)

    for tag in tags:
        repository.tag_repo.create(tag)

    print('Populated free materials')
