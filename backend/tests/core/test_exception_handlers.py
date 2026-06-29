from fastapi import (
    FastAPI,
    HTTPException,
)
from fastapi.testclient import TestClient

from issuescout.core.exceptions.handlers import (
    register_exception_handlers,
)


def create_app() -> TestClient:
    app = FastAPI()

    register_exception_handlers(app)

    @app.get("/http-error")
    async def http_error():
        raise HTTPException(
            status_code=404,
            detail="Not Found",
        )

    @app.get("/server-error")
    async def server_error():
        raise RuntimeError(
            "Something went wrong",
        )

    return TestClient(
        app,
        raise_server_exceptions=False,
    )


def test_http_exception_handler():
    client = create_app()

    response = client.get(
        "/http-error",
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Not Found",
    }


def test_unhandled_exception_handler():
    client = create_app()

    response = client.get(
        "/server-error",
    )

    assert response.status_code == 500
    assert response.json() == {
        "detail": "Internal server error",
    }
