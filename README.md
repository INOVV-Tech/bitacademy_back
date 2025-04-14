# template_simple_mss_python 🐘🌐

Template para repositórios de microsserviços baseado em Clean Architecture com PostgreSQL e Python.

## O Projeto 📽

### Introdução e Objetivos ⁉

Este projeto tem como objetivo fornecer um template para repositórios de microsserviços, utilizando uma arquitetura limpa e organizada.

### Razões 🔑

O projeto busca simplificar o início de novos projetos, garantindo uma base sólida com boas práticas arquiteturais. Isso é ideal para equipes que procuram iniciar rapidamente um projeto mantendo a escalabilidade e a manutenibilidade.

### Clean Architecture 🧼🏛️

A arquitetura deste template é baseada nos princípios de Clean Architecture, incluindo os conceitos do livro "Clean Architecture: A Craftsman's Guide to Software Structure and Design" de Robert C. Martin. O design se baseia nos princípios SOLID para promover separação de responsabilidades e baixo acoplamento.

### Estrutura de Pastas 🎄🌴🌲🌳

A estrutura de pastas foi cuidadosamente desenhada para acomodar a arquitetura limpa e os requisitos do GCP, como a necessidade de zips individuais para cada Cloud Function. Cada rota dentro de `src/modules` representa uma Cloud Function separada.

```bash
.
├── .env
├── .gitignore
├── requirements.txt
├── requirements-dev.txt
└── src
    ├── routes
    │   ├── create_user.py
    │   ├── get_user.py
    │   ├── delete_user.py
    │   ├── update_user.py
    │   └── get_all_users.py
    ├── domain
    │   ├── entities
    │   │   ├── user.py
    │   │   └── address.py
    │   ├── repositories
    │   │   ├── user_repository_interface.py
    │   │   └── address_repository_interface.py
    │   └── enums
    │       └── stage_enum.py
    ├── helpers
    │   ├── errors
    │   │   ├── errors.py
    │   └── http
    │       ├── http_codes.py
    │       ├── http_models.py
    │       └── http_lambda_requests.py # Parsing Cloud Function requests
    └── infra
        ├── external
        │   └── postgre_datasource.py
        ├── models
        │   └── models.py
        └── repositories
            ├── database
            │   └── user_repository_db.py
            ├── mocks
            │   └── user_repository_mock.py
            └── repository.py # Repository init abstraction
```

---

## Formato de Nome 📛

- **Arquivos**: `snake_case` (ex.: `user_model.py`)
- **Classes**: `CamelCase` (ex.: `UserModel`)
- **Métodos**: `snake_case` (ex.: `create_user`, `update_user`)

---

## Variáveis de Ambiente 🌍

As variáveis de ambiente utilizadas no projeto são configuradas no pipeline de CI/CD e incluem:

- `STAGE`: Nome do stage (`dev`, `qa`, `hmg`, `prod`).
- `POSTGRES_URL`: URL de conexão com o banco de dados PostgreSQL.

---

## Execução do Projeto 🚀

### Clone o Repositório:

```bash
git clone https://github.com/user/clean_mss_template_postgres.git
cd clean_mss_template_postgres
```

### Configure o Ambiente Virtual:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Como posso rodar o projeto localmente⁉️⁉️

- Lembre-se de alterar o "NOME_DA_ROTA" para o nome da pasta criada dentro de src/modules

```bash
python -m src.routes.NOME_DA_ROTA.main
```

<!-- ### Crie os arquivos ZIP:

```bash
python main_script_generate_zips.py
```

## Configuração do Pulumi 🛠️

### Instale o Pulumi:

```bash
curl -fsSL https://get.pulumi.com | sh
```

### Configure o Pulumi:

```bash
pulumi login
```

### Crie uma nova stack:

```bash
pulumi stack init dev # ou outro nome de stack
```

### Garanta que o Pulumi irá poder realizar as implantações com o Preview:

```bash
pulumi preview -s dev # ou outro nome de stack
```

### Implante a infraestrutura no GCP:

```bash
pulumi up -s dev # ou outro nome de stack
``` -->
