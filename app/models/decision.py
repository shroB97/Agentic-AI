from typing import Literal

from pydantic import BaseModel, Field


class ProcessDecision(BaseModel):
    invoice_id: str
    exception_types: list[str]
    variance_percent: float | None = None
    risk_score: int = Field(ge=0, le=100)
    route: str
    explanation: str


class AgentRecommendation(BaseModel):
    invoice_id: str

    recommended_action: Literal[
        "APPROVE",
        "REQUEST_DOCUMENTATION",
        "AP_SPECIALIST_REVIEW",
        "SENIOR_FINANCE_REVIEW",
        "FRAUD_OR_COMPLIANCE_REVIEW",
        "REJECT",
    ]

    priority: Literal[
        "LOW",
        "MEDIUM",
        "HIGH",
        "CRITICAL",
    ]

    rationale: str

    required_actions: list[str]

    human_review_required: bool

    confidence: float = Field(ge=0, le=1)
