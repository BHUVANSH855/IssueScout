from pydantic import BaseModel


class PredictionResponse(BaseModel):
    issue_number: int
    pull_request_number: int | None
    confidence: float
    accepted: bool
