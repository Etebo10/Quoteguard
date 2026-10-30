from app.services.project_intelligence import (
    build_historical_evidence,
    calculate_project_variance,
    calculate_service_benchmarks,
)


def test_calculate_project_variance():
    projects = [
        {
            "estimated_labor_hours": 40,
            "actual_labor_hours": 48,
            "estimated_material_cost": 100000,
            "actual_material_cost": 112000,
            "quoted_price": 800000,
            "final_price": 860000,
            "expected_profit": 120000,
            "actual_profit": 90000,
            "expected_margin": 0.15,
            "actual_margin": 0.1047,
        },
        {
            "estimated_labor_hours": 50,
            "actual_labor_hours": 52,
            "estimated_material_cost": 200000,
            "actual_material_cost": 214000,
            "quoted_price": 1000000,
            "final_price": 1060000,
            "expected_profit": 200000,
            "actual_profit": 180000,
            "expected_margin": 0.20,
            "actual_margin": 0.1698,
        },
    ]

    result = calculate_project_variance(projects)

    assert result["labor_variance"] == 0.12
    assert result["material_variance"] == 0.095
    assert result["total_cost_variance"] == 0.0675
    assert result["profit_variance"] == -0.175
    assert result["margin_variance"] == -0.2265


def test_calculate_service_benchmarks():
    projects = [
        {
            "service_type": "Website Development",
            "estimated_labor_hours": 40,
            "actual_labor_hours": 48,
        },
        {
            "service_type": "Website Development",
            "estimated_labor_hours": 50,
            "actual_labor_hours": 56,
        },
        {
            "service_type": "SEO",
            "estimated_labor_hours": 30,
            "actual_labor_hours": 32,
        },
    ]

    result = calculate_service_benchmarks(projects)

    assert "Website Development" in result
    assert result["Website Development"]["avg_labor_variance"] == 0.16
    assert "SEO" in result
    assert result["SEO"]["avg_labor_variance"] == 0.0667


def test_build_historical_evidence_from_completed_projects():
    projects = [
        {
            "service_type": "Website Development",
            "estimated_labor_hours": 40,
            "actual_labor_hours": 48,
            "estimated_material_cost": 100000,
            "actual_material_cost": 112000,
            "quoted_price": 800000,
            "final_price": 860000,
            "customer_id": 12,
            "status": "completed",
        },
        {
            "service_type": "Website Development",
            "estimated_labor_hours": 50,
            "actual_labor_hours": 54,
            "estimated_material_cost": 120000,
            "actual_material_cost": 130000,
            "quoted_price": 900000,
            "final_price": 960000,
            "customer_id": 7,
            "status": "completed",
        },
    ]

    result = build_historical_evidence(projects, service_type="Website Development")

    assert result["service_type"] == "Website Development"
    assert result["project_count"] == 2
    assert result["avg_labor_variance"] == 0.14
    assert result["avg_material_variance"] == 0.1017
    assert result["avg_total_cost_variance"] == 0.0708
