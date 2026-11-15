from fastapi.testclient import TestClient


def test_health_check_returns_200_and_ok(client: TestClient):
    """Testa se o endpoint de saúde responde com 200 OK e dados da aplicação."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "app_name" in data
    assert "version" in data
