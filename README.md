# 🚀 Meu Primeiro API - Projeto de Portfólio (Estágio Backend)

<div align="center">

![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)
![Coverage](https://img.shields.io/badge/Coverage-100%25-brightgreen?style=for-the-badge)
![CI/CD](https://img.shields.io/badge/CI-GitHub%20Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)

</div>

---

## 🎯 Sobre o Projeto & Motivação

Este projeto foi desenvolvido com foco em **processos seletivos para vagas de Estágio em Desenvolvimento de Software / Backend**. 

O objetivo principal foi construir uma **API RESTful completa do zero**, aplicando na prática padrões e boas práticas exigidos pelo mercado de trabalho:
- **Clean Architecture & Separation of Concerns:** Separação clara entre modelos de dados, validações de requisição, regras de negócio e camada HTTP.
- **Qualidade de Software & Testes:** Suíte de testes automatizados com **100% de cobertura de código** usando `pytest` e `pytest-cov`.
- **Isolamento de Ambientes:** Testes executados em banco SQLite em memória (`StaticPool`), garantindo velocidade e zero impacto no banco de dados de desenvolvimento.
- **Automação CI/CD:** Pipeline do **GitHub Actions** configurado para validar testes a cada `push` e `pull request`.
- **Documentação Viva:** Contrato da API documentado automaticamente via OpenAPI (Swagger UI e ReDoc).

---

## 🛠️ Tecnologias e Decisões de Engenharia

| Tecnologia | Finalidade | Por que foi escolhida? |
|---|---|---|
| **Python 3** | Linguagem Principal | Sintaxe moderna, tipagem estática com type hints e ecossistema robusto. |
| **FastAPI** | Framework Web Assíncrono | Alta performance (baseada em Starlette e Pydantic), injeção de dependências e OpenAPI automático. |
| **Pydantic v2** | Validação de Dados | Validação estrita de contratos de entrada e saída, evitando corrupção de dados antes de tocar o banco. |
| **SQLAlchemy 2.0** | ORM / Persistência | Padrão da indústria para mapeamento objeto-relacional seguro e queries eficientes. |
| **SQLite** | Banco de Dados | Leve e ideal para desenvolvimento, com suporte a instâncias in-memory ultra-rápidas para testes. |
| **Pytest + Coverage** | Testes Automatizados | Padrão para testes unitários e de integração, com relatório detalhado de cobertura. |
| **GitHub Actions** | Integração Contínua (CI) | Automação que impede código quebrado de subir para produção. |

---

## 📁 Estrutura do Projeto

Organizado seguindo convenções profissionais de mercado:

```text
meu-primeiro-api/
├── .github/workflows/
│   └── ci.yml              # Pipeline de CI (GitHub Actions)
├── app/
│   ├── __init__.py
│   ├── config.py           # Configurações centralizadas com Pydantic Settings
│   ├── database.py         # Configuração de engine, sessionmaker e injeção (get_db)
│   ├── models.py           # Entidades relacionais do SQLAlchemy (Task, Enums)
│   ├── schemas.py          # Schemas Pydantic (Validação de entrada, saída e paginação)
│   ├── crud.py             # Camada de repositório (operações de dados isoladas)
│   ├── main.py             # Instância do FastAPI, middlewares (CORS) e routers
│   └── routers/
│       ├── __init__.py
│       ├── health.py       # Endpoint de monitoramento / verificação de integridade
│       └── tasks.py        # Endpoints REST (CRUD, paginação, filtros e busca)
├── tests/
│   ├── __init__.py
│   ├── conftest.py         # Fixtures do Pytest com banco SQLite in-memory isolado
│   ├── test_database.py    # Teste de conexão e ciclo de vida da sessão
│   ├── test_health.py      # Testes do endpoint de healthcheck
│   └── test_tasks.py       # 16+ testes cobrindo CRUD, validação 422, paginação e 404
├── .env.example            # Variáveis de ambiente de exemplo
├── .gitignore              # Arquivos e diretórios ignorados pelo Git
├── pytest.ini              # Configuração padrão do Pytest e cobertura
├── requirements.txt        # Dependências do projeto
├── run.sh                  # Script facilitador de execução
└── README.md               # Apresentação do projeto
```

---

## 🧪 Testes Automatizados (100% de Cobertura)

A suíte de testes cobre todos os caminhos felizes (*happy paths*), casos de borda (*edge cases*) e validações de erro:

- **Criação de tarefas:** Validação de campos obrigatórios, tipos e status `201 Created`.
- **Validação de entrada (422):** Rejeição automática de títulos vazios, campos ausentes e enums inválidos.
- **Busca por ID e 404:** Retorno `200 OK` para itens existentes e `404 Not Found` com mensagem amigável para inexistentes.
- **Paginação e Filtros:** Testes com conjuntos de dados múltiplos validando parâmetros `page`, `size`, `status`, `priority` e `search`.
- **Atualização Total (PUT) e Parcial (PATCH):** Garantia de que atualizações parciais não sobrescrevem campos não enviados.
- **Deleção (DELETE):** Validação de status `204 No Content` e verificação posterior de exclusão física.

### Como rodar os testes:

```bash
# Pelo script facilitador:
./run.sh test

# Ou diretamente pelo pytest:
.venv/bin/pytest
```

**Resultado dos Testes:**
```text
======================== 18 passed in 0.30s =========================
TOTAL COVERAGE: 100%
```

---

## 🚀 Como Executar o Projeto Localmente

### Pré-requisitos
- Python 3.10+ (testado no Python 3.14)
- Git

### 1. Clonar o repositório
```bash
git clone https://github.com/eltonshadow/meu-primeiro-api.git
cd meu-primeiro-api
```

### 2. Criar e ativar o ambiente virtual
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Iniciar o servidor
```bash
./run.sh start
```
*O servidor estará disponível em: `http://localhost:8000`*

---

## 📖 Documentação Interativa da API

Com a aplicação rodando, acesse:
- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs) (interface interativa para testar as requisições)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc) (documentação técnica detalhada)

---

## 📌 Rotas Disponíveis

| Método | Rota | Status Esperado | Descrição |
|---|---|---|---|
| `GET` | `/health` | `200 OK` | Verificação de integridade da API |
| `POST` | `/api/v1/tasks` | `201 Created` | Criar nova tarefa |
| `GET` | `/api/v1/tasks` | `200 OK` | Listar tarefas com filtros e paginação |
| `GET` | `/api/v1/tasks/{id}` | `200 OK` / `404` | Buscar tarefa por ID |
| `PUT` | `/api/v1/tasks/{id}` | `200 OK` / `404` | Atualização completa de uma tarefa |
| `PATCH` | `/api/v1/tasks/{id}` | `200 OK` / `404` | Atualização parcial (ex: status) |
| `DELETE` | `/api/v1/tasks/{id}` | `204 No Content` / `404` | Excluir uma tarefa |

---

## 💡 Exemplos de Chamadas via cURL

**1. Criar uma tarefa:**
```bash
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Estudar Arquitetura Backend",
    "description": "Praticar FastAPI, Pydantic e testes automatizados",
    "status": "in_progress",
    "priority": "high"
  }'
```

**2. Listar tarefas com filtro:**
```bash
curl "http://localhost:8000/api/v1/tasks?status=in_progress&priority=high"
```

**3. Atualizar parcialmente (concluir tarefa):**
```bash
curl -X PATCH http://localhost:8000/api/v1/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "done"}'
```

---

## 👤 Autor

Desenvolvido por **Elton**  
- **GitHub:** [@eltonshadow](https://github.com/eltonshadow)
