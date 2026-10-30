import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Quote(Base):

    __tablename__ = "quotes"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    quote_number: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default=lambda: f"Q-{uuid.uuid4().hex[:8].upper()}",
    )

    customer_id: Mapped[int | None] = mapped_column(
        ForeignKey("customers.id"),
        nullable=True,
    )

    project_id: Mapped[int | None] = mapped_column(
        ForeignKey("projects.id"),
        nullable=True,
    )

    service_type: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )
    
    project_name: Mapped[str | None] = mapped_column(
    String(200),
    nullable=True,
)

    labor_hours: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    labor_rate: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    material_cost: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    overhead_rate: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    contingency_rate: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    target_margin: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    total_cost: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    recommended_price: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    proposed_price: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0,
    )

    expected_profit: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    expected_margin: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    decision: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="draft",
        nullable=False,
    )

    notes: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )