def test_health():
    from fastapi.testclient import TestClient
    from apps.gateway.main import app

    client = TestClient(app)
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
