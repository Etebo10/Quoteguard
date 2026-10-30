from pydantic import BaseModel, Field


class AIQuoteAnalysis(BaseModel):

    overall_assessment: str

    confidence_score: float = Field(
        ge=0,
        le=1,
    )

    pricing_assessment: str

    key_concerns: list[str]

    recommendations: list[str]

    decision: str

    decision_reason: str