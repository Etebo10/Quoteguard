from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String

from app.database.database import Base


class LaborRate(Base):
    __tablename__ = "labor_rates"

    id = Column(Integer, primary_key=True, index=True)

    role = Column(
        String(100),
        nullable=False,
    )

    hourly_rate = Column(
        Float,
        nullable=False,
    )

    description = Column(
        String(300),
        nullable=True,
    )

    active = Column(
        Integer,
        default=1,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )