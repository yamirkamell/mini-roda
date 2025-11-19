"""Loan Pydantic schemas."""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class LoanBase(BaseModel):
    """Base loan schema with common fields."""

    customer_id: int = Field(..., description="Customer ID")
    amount: Decimal = Field(..., gt=0, description="Loan amount")
    interest_rate: Decimal = Field(..., gt=0, le=100, description="Interest rate percentage")
    term_months: int = Field(..., gt=0, le=360, description="Loan term in months")


class LoanCreate(LoanBase):
    """Schema for creating a new loan."""

    pass


class LoanSimulate(BaseModel):
    """Schema for loan simulation."""

    amount: Decimal = Field(..., gt=0, description="Loan amount")
    interest_rate: Decimal = Field(..., gt=0, le=100, description="Interest rate percentage")
    term_months: int = Field(..., gt=0, le=360, description="Loan term in months")


class LoanSimulateResponse(BaseModel):
    """Schema for loan simulation response."""

    monthly_payment: Decimal = Field(..., description="Monthly payment amount")
    total_amount: Decimal = Field(..., description="Total amount to be paid")


class LoanResponse(LoanBase):
    """Schema for loan response."""

    id: int = Field(..., description="Loan ID")
    total_amount: Decimal = Field(..., description="Total amount to be paid")
    status: str = Field(..., description="Loan status")
    created_at: datetime = Field(..., description="Loan creation timestamp")

    model_config = {"from_attributes": True}


class LoanApprove(BaseModel):
    """Schema for loan approval."""

    pass


class LoanReject(BaseModel):
    """Schema for loan rejection."""

    reason: str = Field(..., min_length=1, description="Rejection reason")


# Alias for backward compatibility
Loan = LoanResponse


