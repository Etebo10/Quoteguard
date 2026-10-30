from app.services.pricing_engine import (
    PricingInput,
    calculate_quote,
)


def test_quote_calculation():

    pricing_input = PricingInput(
        labor_hours=40,
        labor_rate=10000,
        material_cost=400000,
        overhead_rate=0.10,
        contingency_rate=0.05,
        target_margin=0.25,
    )

    result = calculate_quote(
        pricing_input
    )

    assert result.labor_cost == 400000
    assert result.material_cost == 400000
    assert result.base_cost == 800000
    assert result.overhead_cost == 80000
    assert result.contingency_cost == 44000
    assert result.total_cost == 924000

    assert result.recommended_price == 1232000
    assert result.expected_profit == 308000
    assert result.expected_margin == 0.25


def test_quote_calculation_accepts_percentage_input():
    pricing_input = PricingInput(
        labor_hours=40,
        labor_rate=80,
        material_cost=1000,
        overhead_rate=15,
        contingency_rate=10,
        target_margin=20,
    )

    result = calculate_quote(pricing_input)

    assert result.overhead_cost == 880
    assert result.contingency_cost == 484
    assert result.expected_margin == 0.2
    assert result.recommended_price == 13200.0