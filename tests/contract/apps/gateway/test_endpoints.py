def test_workspace_endpoint():
    from fastapi.testclient import TestClient
    from apps.gateway.main import app

    client = TestClient(app)
    r = client.get("/workspaces/1")
    assert r.status_code == 200
    body = r.json()
    assert body["id"] == 1
    assert body["name"]

def test_workspace_endpoint_denied():
    from fastapi.testclient import TestClient
    from apps.gateway.main import app

    client = TestClient(app)
    r = client.get("/workspaces/1", headers={"X-Debug-Auth": "anon"})
    assert r.status_code == 403
    assert "access_denied" in r.json()["detail"]

def test_workspace_endpoint_not_found():
    from fastapi.testclient import TestClient
    from apps.gateway.main import app

    client = TestClient(app)
    r = client.get("/workspaces/999")
    assert r.status_code == 404
    assert "workspace_not_found" in r.json()["detail"]
