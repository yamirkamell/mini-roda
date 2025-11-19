"""Payment Schedule database model."""

from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class PaymentSchedule(Base):
    """Payment Schedule model for database."""

    __tablename__ = "payment_schedules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    loan_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("loans.id"), nullable=False, index=True
    )
    due_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    paid: Mapped[bool] = mapped_column(default=False, nullable=False)
    paid_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Relationship
    loan: Mapped["Loan"] = relationship("Loan", back_populates="payment_schedules")

    def __repr__(self) -> str:
        """String representation of PaymentSchedule."""
        return f"<PaymentSchedule(id={self.id}, loan_id={self.loan_id}, due_date={self.due_date}, paid={self.paid})>"

