import math


def normalize(value: float, minimum: float, maximum: float) -> float:
    """
    Convert a value into a 0-1 range.
    """

    if maximum == minimum:
        return 0.0

    return (value - minimum) / (maximum - minimum)


def calculate_numeric_similarity(
    value_a: float,
    value_b: float,
) -> float:
    """
    Calculate similarity between two positive numeric values.

    Returns:
        1.0 = identical
        0.0 = very different
    """

    if value_a == value_b:
        return 1.0

    larger = max(
        abs(value_a),
        abs(value_b),
    )

    if larger == 0:
        return 1.0

    difference = abs(
        value_a - value_b
    )

    similarity = 1 - (
        difference / larger
    )

    return max(
        0.0,
        min(1.0, similarity),
    )


def calculate_job_similarity(
    new_job: dict,
    historical_job: dict,
) -> float:

    labor_similarity = calculate_numeric_similarity(
        new_job["labor_hours"],
        historical_job["labor_hours"],
    )

    material_similarity = calculate_numeric_similarity(
        new_job["material_cost"],
        historical_job["material_cost"],
    )

    price_similarity = calculate_numeric_similarity(
        new_job["quoted_price"],
        historical_job["quoted_price"],
    )

    service_similarity = (
        1.0
        if new_job["service"].lower()
        == historical_job["service"].lower()
        else 0.0
    )

    score = (
        labor_similarity * 0.30
        + material_similarity * 0.25
        + price_similarity * 0.20
        + service_similarity * 0.25
    )

    return round(score, 4)