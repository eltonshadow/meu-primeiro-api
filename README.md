# meu primeiro API - API REST com Testes Automatizados

API RESTful completa desenvolvida com **FastAPI**, **SQLAlchemy** e **Pydantic**, acompanhada de uma suíte robusta de testes automatizados com **pytest** e relatório de cobertura (**100% de coverage**).

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.14
- **Framework Web:** [FastAPI](https://fastapi.tiangolo.com/)
- **Servidor ASGI:** [Uvicorn](https://www.uvicorn.org/)
- **ORM / Banco de Dados:** [SQLAlchemy 2.0](https://www.sqlalchemy.org/) com SQLite
- **Validação e Serialização:** [Pydantic v2](https://docs.pydantic.dev/)
- **Testes Automatizados:** [pytest](https://docs.pytest.org/), [httpx](https://www.python-httpx.org/) e [pytest-cov](https://pytest-cov.readthedocs.io/)

---

## 📁 Estrutura do Projeto

```text
task-manager-api/
├── app/
│   ├── __init__.py
│   ├── config.py           # Configurações com Pydantic Settings
│   ├── database.py         # Conexão com banco e session dependency (get_db)
│   ├── models.py           # Modelos de dados SQLAlchemy (Task, Enums)
│   ├── schemas.py          # Schemas Pydantic (Validação de entrada/saída)
│   ├── crud.py             # Camada de persistência e regras de dados
│   ├── main.py             # Instância da aplicação FastAPI e middlewares
│   └── routers/
│       ├── __init__.py
│       ├── health.py       # Endpoint de healthcheck
│       └── tasks.py        # Endpoints REST de tarefas (CRUD + filtros)
├── tests/
│   ├── __init__.py
│   ├── conftest.py         # Fixtures do Pytest com banco SQLite in-memory isolado
│   ├── test_database.py    # Teste de conexão/gerador do banco
│   ├── test_health.py      # Testes do endpoint de healthcheck
│   └── test_tasks.py       # 16+ testes cobrindo CRUD, paginação, filtros e erros 404/422
├── .env.example            # Exemplo de variáveis de ambiente
├── .gitignore              # Arquivos ignorados pelo Git
├── pytest.ini              # Configurações do Pytest e cobertura
├── requirements.txt        # Dependências do projeto
├── run.sh                  # Script facilitador de execução
└── README.md
```

---

## 🚀 Como Executar

### 1. Rodar os Testes Automatizados

O projeto já possui os testes configurados com SQLite em memória, garantindo isolamento total (nenhum dado de teste afeta seu banco de desenvolvimento).

Execute pelo script facilitador:
```bash
./run.sh test
```

Ou diretamente pelo virtualenv:
```bash
.venv/bin/pytest
```

Você verá a saída com todos os **18 testes aprovados** e a tabela de cobertura com **100%**:

```text
======================== 18 passed, 1 warning in 0.30s =========================
TOTAL: 100% de cobertura
```

---

### 2. Iniciar a API

Para rodar o servidor em modo de desenvolvimento com recarregamento automático (*live reload*):

```bash
./run.sh start
```

Ou manualmente:
```bash
.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

A API estará disponível em: `http://localhost:8000`

---

## 📖 Documentação Interativa (OpenAPI / Swagger)

Ao rodar a API, você pode testar todos os endpoints diretamente pelo navegador:

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **OpenAPI JSON:** [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)

---

## 📌 Rotas da API

### Healthcheck
- `GET /health` - Retorna o status de integridade do serviço.

### Tarefas (`/api/v1/tasks`)

| Método | Endpoint | Status | Descrição |
|---|---|---|---|
| `POST` | `/api/v1/tasks` | `201 Created` | Cria uma nova tarefa |
| `GET` | `/api/v1/tasks` | `200 OK` | Lista tarefas com paginação (`page`, `size`) e filtros (`status`, `priority`, `search`) |
| `GET` | `/api/v1/tasks/{id}` | `200 OK` | Busca detalhes de uma tarefa por ID (ou `404 Not Found`) |
| `PUT` | `/api/v1/tasks/{id}` | `200 OK` | Atualização completa de uma tarefa (ou `404`) |
| `PATCH` | `/api/v1/tasks/{id}` | `200 OK` | Atualização parcial (ex: alterar apenas status) |
| `DELETE` | `/api/v1/tasks/{id}` | `204 No Content` | Remove uma tarefa (ou `404`) |

---

## 💡 Exemplos de Requisições via cURL

### 1. Criar uma tarefa
```bash
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Configurar pipeline CI/CD",
    "description": "Adicionar GitHub Actions para rodar pytest automaticamente",
    "status": "todo",
    "priority": "high"
  }'
```

### 2. Listar tarefas com filtros e paginação
```bash
curl "http://localhost:8000/api/v1/tasks?page=1&size=10&status=todo&priority=high"
```

### 3. Atualizar status de uma tarefa (PATCH)
```bash
curl -X PATCH http://localhost:8000/api/v1/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "done"}'
```

### 4. Deletar uma tarefa
```bash
curl -X DELETE http://localhost:8000/api/v1/tasks/1 -i
```

---

## 🛡️ Padrões e Boas Práticas Adotadas

1. **Injeção de Dependências (`Depends(get_db)`):** Facilita testes, desacopla o ciclo de vida da sessão e garante que conexões sejam sempre fechadas.
2. **Isolamento de Testes com SQLite In-Memory (`StaticPool`):** Cada teste roda em um banco limpo e rápido na memória RAM, sem deixar resíduos no disco.
3. **Separação de Camadas:**
   - `models.py`: Modelo relacional do banco.
   - `schemas.py`: Contrato de dados (Pydantic), garantindo que dados de entrada sejam validados antes de tocar o banco.
   - `crud.py`: Operações de leitura e escrita isoladas dos controladores HTTP.
   - `routers/`: Manipulação de requisições e respostas HTTP.
