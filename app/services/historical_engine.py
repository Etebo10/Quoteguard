from statistics import mean

from sqlalchemy.orm import Session

from app.models.job import Job
from app.models.job_cost import JobCost


def get_completed_jobs(
    db: Session,
) -> list[Job]:
    return (
        db.query(Job)
        .filter(Job.status == "completed")
        .all()
    )


def calculate_actual_job_cost(
    db: Session,
    job_id: int,
) -> float:
    costs = (
        db.query(JobCost)
        .filter(JobCost.job_id == job_id)
        .all()
    )

    return sum(cost.amount for cost in costs)


def calculate_estimation_accuracy(
    estimated_cost: float,
    actual_cost: float,
) -> float:
    if estimated_cost <= 0:
        return 0.0

    difference = actual_cost - estimated_cost

    return difference / estimated_cost