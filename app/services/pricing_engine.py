from dataclasses import dataclass


def _normalize_rate(value: float) -> float:
    if value is None:
        return 0.0
    if 0 <= value <= 1:
        return value
    if 1 < value <= 100:
        return value / 100
    return value


@dataclass
class PricingInput:
    labor_hours: float
    labor_rate: float
    material_cost: float
    overhead_rate: float
    contingency_rate: float
    target_margin: float


@dataclass
class PricingResult:
    labor_cost: float
    material_cost: float
    base_cost: float
    overhead_cost: float
    contingency_cost: float
    total_cost: float
    recommended_price: float
    expected_profit: float
    expected_margin: float


def calculate_quote(data: PricingInput) -> PricingResult:
    """
    Calculate a quote using deterministic business rules.

    Accepts either decimal percentages (0.10 for 10%) or whole-number
    percentages from the browser UI (10 for 10%).
    """

    overhead_rate = _normalize_rate(data.overhead_rate)
    contingency_rate = _normalize_rate(data.contingency_rate)
    target_margin = _normalize_rate(data.target_margin)

    labor_cost = data.labor_hours * data.labor_rate

    material_cost = data.material_cost

    base_cost = labor_cost + material_cost

    overhead_cost = base_cost * overhead_rate

    cost_before_contingency = base_cost + overhead_cost

    contingency_cost = (
        cost_before_contingency * contingency_rate
    )

    total_cost = (
        cost_before_contingency + contingency_cost
    )

    if not 0 <= target_margin < 1:
        raise ValueError(
            "Target margin must be between 0 and 1."
        )

    recommended_price = (
        total_cost / (1 - target_margin)
    )

    expected_profit = (
        recommended_price - total_cost
    )

    expected_margin = (
        expected_profit / recommended_price
    )

    return PricingResult(
        labor_cost=round(labor_cost, 2),
        material_cost=round(material_cost, 2),
        base_cost=round(base_cost, 2),
        overhead_cost=round(overhead_cost, 2),
        contingency_cost=round(contingency_cost, 2),
        total_cost=round(total_cost, 2),
        recommended_price=round(recommended_price, 2),
        expected_profit=round(expected_profit, 2),
        expected_margin=round(expected_margin, 4),
    )