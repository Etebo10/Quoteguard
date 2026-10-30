from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(
        Integer,
        ForeignKey("customers.id"),
        nullable=False,
    )

    title = Column(String(200), nullable=False)

    description = Column(Text, nullable=True)

    job_type = Column(String(100), nullable=True)

    status = Column(
        String(50),
        default="planned",
        nullable=False,
    )

    estimated_hours = Column(Integer, nullable=True)

    actual_hours = Column(Integer, nullable=True)

    scheduled_date = Column(DateTime, nullable=True)

    completed_at = Column(DateTime, nullable=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    customer = relationship("Customer", back_populates="jobs")