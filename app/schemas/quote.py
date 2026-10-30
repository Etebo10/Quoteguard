from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class QuoteStatusUpdate(BaseModel):
    status: str = Field(default="draft")
    notes: str | None = None


class QuoteRecordResponse(BaseModel):
    id: int
    quote_number: str
    customer_id: int | None = None
    project_id: int | None = None
    service_type: str
    project_name: str | None = None
    labor_hours: float
    labor_rate: float
    material_cost: float
    overhead_rate: float
    contingency_rate: float
    target_margin: float
    total_cost: float
    recommended_price: float
    expected_profit: float
    expected_margin: float
    decision: str | None = None
    status: str = "draft"
    notes: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class QuoteCalculationRequest(BaseModel):

    labor_hours: float = Field(
        ge=0
    )

    labor_rate: float = Field(
        ge=0
    )

    material_cost: float = Field(
        ge=0
    )

    overhead_rate: float = Field(
        ge=0,
        le=1
    )

    contingency_rate: float = Field(
        ge=0,
        le=1
    )

    target_margin: float = Field(
        gt=0,
        lt=1
    )


class QuoteCalculationResponse(BaseModel):

    labor_cost: float

    material_cost: float

    base_cost: float

    overhead_cost: float

    contingency_cost: float

    total_cost: float

    recommended_price: float

    expected_profit: float

    expected_margin: float