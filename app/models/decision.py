from pydantic import BaseModel, Field


class ProcessDecision(BaseModel):
    invoice_id: str
    exception_types: list[str]
    variance_percent: float | None = None
    risk_score: int = Field(ge=0, le=100)
    route: str
    explanation: str
