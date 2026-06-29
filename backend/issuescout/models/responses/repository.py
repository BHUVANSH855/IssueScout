from pydantic import BaseModel


class RepositoryResponse(BaseModel):
    name: str
    owner: str
    stars: int
    forks: int
    open_issues: int
    default_branch: str
