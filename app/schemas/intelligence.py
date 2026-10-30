from pydantic import BaseModel, ConfigDict, Field


class QuoteIntelligenceRequest(BaseModel):
    customer_name: str
    customer_email: str | None = None

    project_name: str
    service_type: str

    labor_hours: float
    labor_rate: float
    material_cost: float

    overhead_rate: float
    contingency_rate: float
    target_margin: float

    historical_estimation_variance: float = 0.0


class RiskResponse(BaseModel):
    risk_type: str
    severity: str
    message: str
    recommendation: str


class QuoteIntelligenceResponse(BaseModel):
    labor_cost: float
    material_cost: float
    base_cost: float
    overhead_cost: float
    contingency_cost: float
    total_cost: float
    recommended_price: float
    expected_profit: float
    expected_margin: float
    risks: list[RiskResponse] = Field(default_factory=list)
    ai_analysis: dict = Field(default_factory=dict)

    model_config = ConfigDict(from_attributes=True)