from app.services.historical_statistics import (
    calculate_historical_statistics,
)


def test_historical_statistics():

    jobs = [
        {
            "quoted_price": 1000000,
            "estimation_variance": 0.10,
            "actual_margin": 0.20,
        },
        {
            "quoted_price": 1200000,
            "estimation_variance": 0.20,
            "actual_margin": 0.15,
        },
        {
            "quoted_price": 1100000,
            "estimation_variance": 0.15,
            "actual_margin": 0.18,
        },
    ]

    result = calculate_historical_statistics(
        jobs
    )

    assert result["job_count"] == 3

    assert (
        result["average_estimation_variance"]
        == 0.15
    )

    assert (
        result["average_margin"]
        == 0.1767
    )