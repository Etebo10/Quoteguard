from app.services.similarity_engine import (
    calculate_job_similarity,
)


def find_similar_jobs(
    new_job: dict,
    historical_jobs: list[dict],
    limit: int = 5,
) -> list[dict]:

    scored_jobs = []

    for job in historical_jobs:

        score = calculate_job_similarity(
            new_job,
            job,
        )

        scored_jobs.append(
            {
                **job,
                "similarity_score": score,
            }
        )

    scored_jobs.sort(
        key=lambda job: job["similarity_score"],
        reverse=True,
    )

    return scored_jobs[:limit]