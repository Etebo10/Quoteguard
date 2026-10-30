from app.services.historical_retriever import (
    find_similar_jobs,
)


def test_similar_jobs_are_ranked():

    new_job = {
        "service": "Website Development",
        "labor_hours": 50,
        "material_cost": 300000,
        "quoted_price": 1200000,
    }

    historical_jobs = [
        {
            "id": 1,
            "service": "Website Development",
            "labor_hours": 48,
            "material_cost": 290000,
            "quoted_price": 1150000,
        },
        {
            "id": 2,
            "service": "Social Media Management",
            "labor_hours": 20,
            "material_cost": 50000,
            "quoted_price": 300000,
        },
        {
            "id": 3,
            "service": "Website Development",
            "labor_hours": 100,
            "material_cost": 800000,
            "quoted_price": 2500000,
        },
    ]

    results = find_similar_jobs(
        new_job,
        historical_jobs,
        limit=2,
    )

    assert len(results) == 2

    assert results[0]["id"] == 1

    assert (
        results[0]["similarity_score"]
        >= results[1]["similarity_score"]
    )