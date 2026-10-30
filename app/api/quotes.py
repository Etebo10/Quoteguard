from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.quote import Quote
from app.schemas.quote import QuoteRecordResponse, QuoteStatusUpdate

router = APIRouter(prefix="/quotes", tags=["Quotes"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[QuoteRecordResponse])
def list_quotes(db: Session = Depends(get_db)):
    quotes = db.query(Quote).order_by(Quote.created_at.desc()).all()
    return quotes


@router.get("/{quote_id}", response_model=QuoteRecordResponse)
def get_quote(quote_id: int, db: Session = Depends(get_db)):
    quote = db.query(Quote).filter(Quote.id == quote_id).first()
    if quote is None:
        raise HTTPException(status_code=404, detail="Quote not found")
    return quote


@router.patch("/{quote_id}/status", response_model=QuoteRecordResponse)
def update_quote_status(
    quote_id: int,
    payload: QuoteStatusUpdate,
    db: Session = Depends(get_db),
):
    quote = db.query(Quote).filter(Quote.id == quote_id).first()
    if quote is None:
        raise HTTPException(status_code=404, detail="Quote not found")

    quote.status = payload.status
    if payload.notes is not None:
        quote.notes = payload.notes

    db.commit()
    db.refresh(quote)
    return quote
