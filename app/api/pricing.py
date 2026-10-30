from fastapi import APIRouter, HTTPException

from app.schemas.quote import (
    QuoteCalculationRequest,
    QuoteCalculationResponse,
)

from app.services.pricing_engine import (
    PricingInput,
    calculate_quote,
)


router = APIRouter(
    prefix="/pricing",
    tags=["Pricing"],
)


@router.post(
    "/calculate",
    response_model=QuoteCalculationResponse,
)
def calculate_pricing(
    request: QuoteCalculationRequest,
):
    try:
        pricing_input = PricingInput(
            labor_hours=request.labor_hours,
            labor_rate=request.labor_rate,
            material_cost=request.material_cost,
            overhead_rate=request.overhead_rate,
            contingency_rate=request.contingency_rate,
            target_margin=request.target_margin,
        )

        result = calculate_quote(pricing_input)

        return result

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )