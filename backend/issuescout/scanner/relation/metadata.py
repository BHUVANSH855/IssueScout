from pydantic import BaseModel


class AnalyzerMetadata(BaseModel):
    name: str

    weight: int

    enabled: bool = True

    description: str = ""
