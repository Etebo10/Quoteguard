from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Project(Base):

    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    customer_id: Mapped[int | None] = mapped_column(
        ForeignKey("customers.id"),
        nullable=True,
    )

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    service_type: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    estimated_labor_hours: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    actual_labor_hours: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    estimated_material_cost: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    actual_material_cost: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    quoted_price: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    final_price: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="active",
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    customer = relationship("Customer", back_populates="projects")