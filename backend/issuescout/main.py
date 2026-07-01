from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from issuescout.api.v1.routes import router
from issuescout.core.config import settings
from issuescout.core.exceptions import (
    register_exception_handlers,
)
from issuescout.middleware import (
    logging_middleware,
)

app = FastAPI(
    title="IssueScout API",
    summary=("GitHub contribution assistant for discovering and analyzing issues."),
    description=(
        "IssueScout analyzes GitHub repositories, issues, "
        "pull requests, commits, comments, and repository "
        "metadata to help contributors discover suitable "
        "issues and understand their relationships."
    ),
    version="0.1.0",
    contact={
        "name": "Bhuvansh Kataria",
        "url": "https://github.com/BHUVANSH855",
    },
    license_info={
        "name": "MIT License",
    },
)
register_exception_handlers(app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.middleware("http")(
    logging_middleware,
)


@app.get(
    "/",
    summary="Welcome",
    tags=["General"],
)
async def root():
    return {
        "message": "Welcome to IssueScout 🚀",
    }


@app.get(
    "/health",
    summary="Health Check",
    tags=["General"],
)
async def health():
    return {
        "status": "healthy",
    }


app.include_router(router)
