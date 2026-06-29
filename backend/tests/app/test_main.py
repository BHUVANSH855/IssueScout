from fastapi.testclient import TestClient

from issuescout.main import app


client = TestClient(app)


def test_app_metadata():
    assert app.title == "IssueScout API"

    assert app.version == "0.1.0"

    assert app.summary == (
        "GitHub contribution assistant for discovering and analyzing issues."
    )

    assert app.description == (
        "IssueScout analyzes GitHub repositories, issues, "
        "pull requests, commits, comments, and repository "
        "metadata to help contributors discover suitable "
        "issues and understand their relationships."
    )

    assert app.contact == {
        "name": "Bhuvansh Kataria",
        "url": "https://github.com/BHUVANSH855",
    }

    assert app.license_info == {
        "name": "MIT License",
    }


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
