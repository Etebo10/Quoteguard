from __future__ import annotations

from statistics import mean


def _safe_ratio(numerator: float, denominator: float) -> float:
    if denominator == 0:
        return 0.0
    return numerator / denominator


def build_historical_evidence(projects: list[dict], service_type: str | None = None) -> dict:
    filtered = [project for project in projects if project.get("status") == "completed"]

    if service_type:
        filtered = [
            project for project in filtered if str(project.get("service_type", "")).lower() == service_type.lower()
        ]

    if not filtered:
        return {
            "service_type": service_type,
            "project_count": 0,
            "avg_labor_variance": 0.0,
            "avg_material_variance": 0.0,
            "avg_total_cost_variance": 0.0,
            "customer_count": 0,
        }

    labor_variances = []
    material_variances = []
    total_cost_variances = []

    for project in filtered:
        estimated_labor = project.get("estimated_labor_hours", 0) or 0
        actual_labor = project.get("actual_labor_hours", 0) or 0
        if estimated_labor:
            labor_variances.append((actual_labor - estimated_labor) / estimated_labor)

        estimated_material = project.get("estimated_material_cost", 0) or 0
        actual_material = project.get("actual_material_cost", 0) or 0
        if estimated_material:
            material_variances.append((actual_material - estimated_material) / estimated_material)

        quoted_price = project.get("quoted_price")
        final_price = project.get("final_price")
        if quoted_price and final_price:
            total_cost_variances.append((final_price - quoted_price) / quoted_price)

    return {
        "service_type": service_type,
        "project_count": len(filtered),
        "avg_labor_variance": round(mean(labor_variances), 4) if labor_variances else 0.0,
        "avg_material_variance": round(mean(material_variances), 4) if material_variances else 0.0,
        "avg_total_cost_variance": round(mean(total_cost_variances), 4) if total_cost_variances else 0.0,
        "customer_count": len({project.get("customer_id") for project in filtered if project.get("customer_id") is not None}),
    }


def calculate_project_variance(projects: list[dict]) -> dict:
    if not projects:
        return {
            "labor_variance": 0.0,
            "material_variance": 0.0,
            "total_cost_variance": 0.0,
            "profit_variance": 0.0,
            "margin_variance": 0.0,
        }

    labor_variances = []
    material_variances = []
    total_cost_variances = []
    profit_variances = []
    margin_variances = []

    for project in projects:
        estimated_labor = project.get("estimated_labor_hours", 0) or 0
        actual_labor = project.get("actual_labor_hours", 0) or 0
        if estimated_labor:
            labor_variances.append((actual_labor - estimated_labor) / estimated_labor)

        estimated_material = project.get("estimated_material_cost", 0) or 0
        actual_material = project.get("actual_material_cost", 0) or 0
        if estimated_material:
            material_variances.append((actual_material - estimated_material) / estimated_material)

        estimated_total = project.get("estimated_total_cost")
        actual_total = project.get("actual_total_cost")
        if estimated_total is not None and actual_total is not None and estimated_total:
            total_cost_variances.append((actual_total - estimated_total) / estimated_total)
        elif project.get("quoted_price") and project.get("final_price"):
            total_cost_variances.append((project["final_price"] - project["quoted_price"]) / project["quoted_price"])

        expected_profit = project.get("expected_profit")
        actual_profit = project.get("actual_profit")
        if expected_profit not in (None, 0) and actual_profit is not None:
            profit_variances.append((actual_profit - expected_profit) / expected_profit)

        expected_margin = project.get("expected_margin")
        actual_margin = project.get("actual_margin")
        if expected_margin is not None and actual_margin is not None:
            margin_variances.append((actual_margin - expected_margin) / expected_margin if expected_margin else 0.0)

    return {
        "labor_variance": round(mean(labor_variances), 4) if labor_variances else 0.0,
        "material_variance": round(mean(material_variances), 4) if material_variances else 0.0,
        "total_cost_variance": round(mean(total_cost_variances), 4) if total_cost_variances else 0.0,
        "profit_variance": round(mean(profit_variances), 4) if profit_variances else 0.0,
        "margin_variance": round(mean(margin_variances), 4) if margin_variances else 0.0,
    }


def calculate_service_benchmarks(projects: list[dict]) -> dict:
    grouped: dict[str, list[dict]] = {}
    for project in projects:
        service = project.get("service_type")
        if not service:
            continue
        grouped.setdefault(service, []).append(project)

    benchmarks: dict[str, dict] = {}
    for service, items in grouped.items():
        variances = []
        for item in items:
            estimated = item.get("estimated_labor_hours", 0) or 0
            actual = item.get("actual_labor_hours", 0) or 0
            if estimated:
                variances.append((actual - estimated) / estimated)

        benchmarks[service] = {
            "project_count": len(items),
            "avg_labor_variance": round(mean(variances), 4) if variances else 0.0,
            "avg_material_variance": 0.0,
        }

    return benchmarks
