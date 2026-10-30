from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String

from app.database.database import Base


class Material(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(200), nullable=False)

    unit = Column(String(50), nullable=False)

    unit_cost = Column(Float, nullable=False)

    supplier = Column(String(200), nullable=True)

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