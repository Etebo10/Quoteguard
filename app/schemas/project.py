from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProjectCreate(BaseModel):
    customer_id: int | None = None
    name: str
    service_type: str
    estimated_labor_hours: float = Field(ge=0)
    actual_labor_hours: float | None = Field(default=None, ge=0)
    estimated_material_cost: float = Field(ge=0)
    actual_material_cost: float | None = Field(default=None, ge=0)
    quoted_price: float = Field(ge=0)
    final_price: float | None = Field(default=None, ge=0)
    status: str = "active"
    completed_at: datetime | None = None


class ProjectResponse(BaseModel):
    id: int
    customer_id: int | None = None
    name: str
    service_type: str
    estimated_labor_hours: float
    actual_labor_hours: float | None = None
    estimated_material_cost: float
    actual_material_cost: float | None = None
    quoted_price: float
    final_price: float | None = None
    status: str
    completed_at: datetime | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
