from unittest.mock import AsyncMock

from fastapi import FastAPI
from fastapi.testclient import TestClient

from issuescout.api.v1.routes import (
    get_issue_service,
    get_repository_service,
    get_scanner_engine,
    router,
)


app = FastAPI()
app.include_router(router)


def test_github_endpoint():
    service = AsyncMock()

    service.get_repository.return_value = {
        "name": "cpython",
        "owner": {
            "login": "python",
        },
        "stargazers_count": 100,
        "forks_count": 20,
        "open_issues_count": 30,
        "default_branch": "main",
    }

    app.dependency_overrides[get_repository_service] = lambda: service

    client = TestClient(app)

    response = client.get("/github")

    assert response.status_code == 200

    assert response.json() == {
        "name": "cpython",
        "owner": "python",
        "stars": 100,
        "forks": 20,
        "open_issues": 30,
        "default_branch": "main",
    }

    service.get_repository.assert_awaited_once_with(
        "python",
        "cpython",
    )

    service.close.assert_awaited_once()

    app.dependency_overrides.clear()


def test_issues_endpoint():
    service = AsyncMock()

    service.list_open_issues.return_value = [
        {
            "number": 1,
            "title": "Issue One",
            "assignee": {
                "login": "alice",
            },
        },
        {
            "number": 2,
            "title": "Issue Two",
            "assignee": None,
        },
    ]

    app.dependency_overrides[get_issue_service] = lambda: service

    client = TestClient(app)

    response = client.get("/issues")

    assert response.status_code == 200

    assert response.json() == [
        {
            "number": 1,
            "title": "Issue One",
            "assignee": "alice",
        },
        {
            "number": 2,
            "title": "Issue Two",
            "assignee": None,
        },
    ]

    service.list_open_issues.assert_awaited_once_with(
        "python",
        "cpython",
    )

    service.close.assert_awaited_once()

    app.dependency_overrides.clear()


def test_scan_repository_endpoint():
    engine = AsyncMock()

    engine.scan_repository.return_value = {
        "repository": "python/cpython",
        "total_issues": 5,
    }

    app.dependency_overrides[get_scanner_engine] = lambda: engine

    client = TestClient(app)

    response = client.get(
        "/scan/python/cpython",
    )

    assert response.status_code == 200

    assert response.json() == {
        "repository": "python/cpython",
        "total_issues": 5,
    }

    engine.scan_repository.assert_awaited_once_with(
        "python",
        "cpython",
    )

    app.dependency_overrides.clear()
