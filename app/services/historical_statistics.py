from statistics import mean


def calculate_historical_statistics(
    similar_jobs: list[dict],
) -> dict:

    if not similar_jobs:
        return {
            "job_count": 0,
            "average_estimation_variance": 0.0,
            "average_margin": 0.0,
            "average_quoted_price": 0.0,
        }

    estimation_variances = [
        job["estimation_variance"]
        for job in similar_jobs
        if "estimation_variance" in job
    ]

    margins = [
        job["actual_margin"]
        for job in similar_jobs
        if "actual_margin" in job
    ]

    quoted_prices = [
        job["quoted_price"]
        for job in similar_jobs
        if "quoted_price" in job
    ]

    return {
        "job_count": len(similar_jobs),

        "average_estimation_variance": round(
            mean(estimation_variances),
            4,
        ) if estimation_variances else 0.0,

        "average_margin": round(
            mean(margins),
            4,
        ) if margins else 0.0,

        "average_quoted_price": round(
            mean(quoted_prices),
            2,
        ) if quoted_prices else 0.0,
    }