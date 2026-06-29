from pydantic import BaseModel


class ScanResponse(BaseModel):
    repository: str
    total_issues: int
