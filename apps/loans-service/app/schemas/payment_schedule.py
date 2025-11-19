"""Payment Schedule Pydantic schemas."""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class PaymentScheduleBase(BaseModel):
    """Base payment schedule schema with common fields."""

    due_date: datetime = Field(..., description="Payment due date")
    amount: Decimal = Field(..., gt=0, description="Payment amount")


class PaymentScheduleCreate(BaseModel):
    """Schema for creating a payment registration."""

    amount: Decimal = Field(..., gt=0, description="Payment amount")
    paid_date: datetime = Field(..., description="Payment date")


class PaymentScheduleResponse(PaymentScheduleBase):
    """Schema for payment schedule response."""

    id: int = Field(..., description="Payment schedule ID")
    loan_id: int = Field(..., description="Loan ID")
    paid: bool = Field(..., description="Whether payment has been made")
    paid_date: datetime | None = Field(None, description="Date when payment was made")

    model_config = {"from_attributes": True}


# Alias for backward compatibility
PaymentSchedule = PaymentScheduleResponse


