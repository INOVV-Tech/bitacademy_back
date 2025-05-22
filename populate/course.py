import os
from populate.common import load_app_env, load_resource

load_app_env()

from src.shared.infra.repositories.repository import Repository

from src.shared.domain.entities.course import Course
from src.shared.domain.entities.tag import Tag

USER_ID = os.environ.get('POPULATE_USER_ID')

def populate_courses():
    repository = Repository(course_repo=True, tag_repo=True)

    tags = [ 'Investimentos', 'Iniciantes' ]

    template = {
        'title': 'Curso Investimento do Zero ao Avançado',
        'description': 'Domine os principais conceitos do mercado financeiro, conheça diferentes tipos de ativos e descubra estratégias para potencializar seus ganhos em renda fixa, variável e criptomoedas. Fundamentos do mercado financeiro Investimentos em renda fixa e variável Introdução às criptomoedas (Bitcoin, Ethereum e altcoins).',
        'teachers': [ 'Rogério Silva' ],
        'duration': '3 meses',
        'external_url': 'https://www.youtube.com/',
        'tags': tags,
        'vip_level': 1,
        'cover_img': load_resource('course-cover-1.jpg',
            encode_base64=True, base64_prefix='data:image/jpg;base64'),
        'card_img': load_resource('course-card-1.jpg',
            encode_base64=True, base64_prefix='data:image/jpg;base64')
    }
    
    for i in range(20):
        (error, course) = Course.from_request_data(template, USER_ID)
        
        s3_datasource = repository.get_s3_datasource()

        upload_cover_resp = course.cover_img.store_in_s3(s3_datasource)
        upload_card_resp = course.card_img.store_in_s3(s3_datasource)
        
        repository.course_repo.create(course)

        print(f'Populated {(i + 1)} course')

    tags = Tag.from_string_list(tags)

    for tag in tags:
        repository.tag_repo.create(tag)

    print('Populated courses')
