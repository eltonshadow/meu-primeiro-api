from fastapi.testclient import TestClient


def test_create_task_success(client: TestClient, sample_task_data: dict):
    """Testa criação bem-sucedida de tarefa (201 Created)."""
    response = client.post("/api/v1/tasks", json=sample_task_data)
    assert response.status_code == 201

    data = response.json()
    assert data["id"] is not None
    assert data["title"] == sample_task_data["title"]
    assert data["description"] == sample_task_data["description"]
    assert data["status"] == sample_task_data["status"]
    assert data["priority"] == sample_task_data["priority"]
    assert "created_at" in data
    assert "updated_at" in data


def test_create_task_validation_missing_title(client: TestClient):
    """Testa validação de erro quando campo obrigatório 'title' não é enviado (422)."""
    response = client.post("/api/v1/tasks", json={"description": "Sem título"})
    assert response.status_code == 422


def test_create_task_validation_empty_title(client: TestClient):
    """Testa que título com string vazia é rejeitado (min_length=1)."""
    response = client.post("/api/v1/tasks", json={"title": ""})
    assert response.status_code == 422


def test_create_task_invalid_status(client: TestClient):
    """Testa que valor de status inválido é rejeitado pela validação do Pydantic (422)."""
    response = client.post(
        "/api/v1/tasks",
        json={"title": "Tarefa com status inválido", "status": "invalid_status"},
    )
    assert response.status_code == 422


def test_get_task_by_id_success(client: TestClient, sample_task_data: dict):
    """Testa recuperação de uma tarefa por ID (200 OK)."""
    created = client.post("/api/v1/tasks", json=sample_task_data).json()
    task_id = created["id"]

    response = client.get(f"/api/v1/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == sample_task_data["title"]


def test_get_task_by_id_not_found(client: TestClient):
    """Testa busca por ID inexistente retornando 404 Not Found."""
    response = client.get("/api/v1/tasks/99999")
    assert response.status_code == 404
    assert "não encontrada" in response.json()["detail"]


def test_list_tasks_empty(client: TestClient):
    """Testa listagem de tarefas com banco vazio."""
    response = client.get("/api/v1/tasks")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["items"] == []
    assert data["page"] == 1
    assert data["size"] == 10


def test_list_tasks_pagination(client: TestClient):
    """Testa paginação criando múltiplos registros."""
    for i in range(15):
        client.post(
            "/api/v1/tasks",
            json={"title": f"Tarefa {i + 1}", "priority": "low"},
        )

    # Página 1 com 10 itens
    resp_p1 = client.get("/api/v1/tasks?page=1&size=10")
    assert resp_p1.status_code == 200
    data_p1 = resp_p1.json()
    assert data_p1["total"] == 15
    assert len(data_p1["items"]) == 10

    # Página 2 com os 5 restantes
    resp_p2 = client.get("/api/v1/tasks?page=2&size=10")
    assert resp_p2.status_code == 200
    data_p2 = resp_p2.json()
    assert data_p2["total"] == 15
    assert len(data_p2["items"]) == 5


def test_list_tasks_filter_by_status_and_priority(client: TestClient):
    """Testa filtros por status e prioridade."""
    client.post(
        "/api/v1/tasks",
        json={"title": "Fazer café", "status": "done", "priority": "high"},
    )
    client.post(
        "/api/v1/tasks",
        json={"title": "Comprar leite", "status": "todo", "priority": "low"},
    )
    client.post(
        "/api/v1/tasks",
        json={"title": "Escrever documentação", "status": "todo", "priority": "high"},
    )

    # Filtro por status=todo
    resp_todo = client.get("/api/v1/tasks?status=todo")
    assert resp_todo.json()["total"] == 2

    # Filtro por status=todo AND priority=high
    resp_filtered = client.get("/api/v1/tasks?status=todo&priority=high")
    assert resp_filtered.json()["total"] == 1
    assert resp_filtered.json()["items"][0]["title"] == "Escrever documentação"


def test_list_tasks_search(client: TestClient):
    """Testa busca textual no título."""
    client.post("/api/v1/tasks", json={"title": "Relatório Financeiro Q3"})
    client.post("/api/v1/tasks", json={"title": "Revisar código frontend"})

    response = client.get("/api/v1/tasks?search=Financeiro")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["title"] == "Relatório Financeiro Q3"


def test_put_update_task_success(client: TestClient, sample_task_data: dict):
    """Testa atualização completa via PUT (200 OK)."""
    created = client.post("/api/v1/tasks", json=sample_task_data).json()
    task_id = created["id"]

    updated_payload = {
        "title": "Título Atualizado Totalmente",
        "description": "Nova descrição completa",
        "status": "in_progress",
        "priority": "low",
    }
    response = client.put(f"/api/v1/tasks/{task_id}", json=updated_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Título Atualizado Totalmente"
    assert data["description"] == "Nova descrição completa"
    assert data["status"] == "in_progress"
    assert data["priority"] == "low"


def test_put_update_task_not_found(client: TestClient, sample_task_data: dict):
    """Testa PUT para tarefa inexistente (404)."""
    response = client.put("/api/v1/tasks/99999", json=sample_task_data)
    assert response.status_code == 404


def test_patch_update_task_partial(client: TestClient, sample_task_data: dict):
    """Testa atualização parcial via PATCH modificando apenas o status."""
    created = client.post("/api/v1/tasks", json=sample_task_data).json()
    task_id = created["id"]

    patch_payload = {"status": "done"}
    response = client.patch(f"/api/v1/tasks/{task_id}", json=patch_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "done"
    # Campos não enviados permanecem inalterados
    assert data["title"] == sample_task_data["title"]
    assert data["description"] == sample_task_data["description"]


def test_patch_update_task_not_found(client: TestClient):
    """Testa PATCH para tarefa inexistente (404)."""
    response = client.patch("/api/v1/tasks/99999", json={"status": "done"})
    assert response.status_code == 404


def test_delete_task_success(client: TestClient, sample_task_data: dict):
    """Testa deleção de tarefa (204 No Content) e validação posterior de que foi removida."""
    created = client.post("/api/v1/tasks", json=sample_task_data).json()
    task_id = created["id"]

    delete_resp = client.delete(f"/api/v1/tasks/{task_id}")
    assert delete_resp.status_code == 204

    # Confirma que não existe mais
    get_resp = client.get(f"/api/v1/tasks/{task_id}")
    assert get_resp.status_code == 404


def test_delete_task_not_found(client: TestClient):
    """Testa tentativa de remoção de tarefa inexistente (404)."""
    response = client.delete("/api/v1/tasks/99999")
    assert response.status_code == 404
