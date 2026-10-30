from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.quote import Quote

router = APIRouter(prefix="/reports", tags=["Reports"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/summary")
def summary(db: Session = Depends(get_db)):
    total_quotes = db.query(func.count(Quote.id)).scalar() or 0
    approved_quotes = db.query(func.count(Quote.id)).filter(Quote.status == "approved").scalar() or 0
    rejected_quotes = db.query(func.count(Quote.id)).filter(Quote.status == "rejected").scalar() or 0

    by_service_type = (
        db.query(Quote.service_type, func.count(Quote.id))
        .group_by(Quote.service_type)
        .all()
    )

    return {
        "total_quotes": total_quotes,
        "approved_quotes": approved_quotes,
        "rejected_quotes": rejected_quotes,
        "by_service_type": {service: count for service, count in by_service_type},
    }
