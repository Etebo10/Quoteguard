from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text

from app.database.database import Base


class QuoteRisk(Base):
    __tablename__ = "quote_risks"

    id = Column(Integer, primary_key=True, index=True)

    quote_id = Column(
        Integer,
        ForeignKey("quotes.id"),
        nullable=False,
    )

    risk_type = Column(
        String(100),
        nullable=False,
    )

    severity = Column(
        String(20),
        nullable=False,
    )

    description = Column(
        Text,
        nullable=False,
    )

    recommendation = Column(
        Text,
        nullable=True,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )