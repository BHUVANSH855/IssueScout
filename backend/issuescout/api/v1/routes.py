from fastapi import (
    APIRouter,
    Depends,
)

from issuescout.core.config import settings
from issuescout.models.responses import (
    IssueResponse,
    RepositoryResponse,
)
from issuescout.scanner.engine import ScannerEngine
from issuescout.services.issue_service import IssueService
from issuescout.services.repository_service import RepositoryService

router = APIRouter(
    tags=["GitHub"],
)


def get_repository_service() -> RepositoryService:
    return RepositoryService()


def get_issue_service() -> IssueService:
    return IssueService()


def get_scanner_engine() -> ScannerEngine:
    return ScannerEngine()


@router.get(
    "/github",
    response_model=RepositoryResponse,
    summary="Repository Information",
    description=("Retrieve metadata for the configured GitHub repository."),
)
async def github(
    service: RepositoryService = Depends(
        get_repository_service,
    ),
):
    repo = await service.get_repository(
        settings.DEFAULT_OWNER,
        settings.DEFAULT_REPOSITORY,
    )

    await service.close()

    return RepositoryResponse(
        name=repo["name"],
        owner=repo["owner"]["login"],
        stars=repo["stargazers_count"],
        forks=repo["forks_count"],
        open_issues=repo["open_issues_count"],
        default_branch=repo["default_branch"],
    )


@router.get(
    "/issues",
    response_model=list[IssueResponse],
    summary="List Open Issues",
    description=("Retrieve all currently open issues from the configured repository."),
)
async def issues(
    service: IssueService = Depends(
        get_issue_service,
    ),
):
    issues = await service.list_open_issues(
        settings.DEFAULT_OWNER,
        settings.DEFAULT_REPOSITORY,
    )

    await service.close()

    return [
        IssueResponse(
            number=issue["number"],
            title=issue["title"],
            assignee=(issue["assignee"]["login"] if issue["assignee"] else None),
        )
        for issue in issues
    ]


@router.get(
    "/scan/{owner}/{repo}",
    summary="Scan Repository",
    description=(
        "Analyze a GitHub repository and "
        "predict pull request relationships "
        "for open issues."
    ),
)
async def scan_repository(
    owner: str,
    repo: str,
    engine: ScannerEngine = Depends(
        get_scanner_engine,
    ),
):
    return await engine.scan_repository(owner, repo)
