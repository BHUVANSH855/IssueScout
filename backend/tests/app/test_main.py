from fastapi.testclient import TestClient

from issuescout.main import app


client = TestClient(app)


def test_app_metadata():
    assert app.title == "IssueScout API"
    assert app.version == "0.1.0"
    assert app.description == "GitHub Contribution Assistant"


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to IssueScout 🚀",
    }


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
    }