"""Loan API endpoints."""

from datetime import datetime
from decimal import Decimal
from typing import List

from fastapi import APIRouter, Depends, Query, status

from app.api.dependencies import get_loan_service
from app.schemas.loan import (
    LoanCreate,
    LoanReject,
    LoanResponse,
    LoanSimulate,
    LoanSimulateResponse,
)
from app.schemas.payment_schedule import PaymentScheduleCreate, PaymentScheduleResponse
from app.services.loan_service import LoanService

router = APIRouter(prefix="/loans", tags=["loans"])


@router.post(
    "/simulate",
    response_model=LoanSimulateResponse,
    summary="Simulate a loan",
    description="Calculate monthly payment and total amount for a loan",
)
async def simulate_loan(
    simulation_data: LoanSimulate,
    service: LoanService = Depends(get_loan_service),
) -> LoanSimulateResponse:
    """Simulate a loan to calculate monthly payment and total amount."""
    return service.simulate_loan(simulation_data)


@router.post(
    "",
    response_model=LoanResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new loan",
)
async def create_loan(
    loan_data: LoanCreate,
    service: LoanService = Depends(get_loan_service),
) -> LoanResponse:
    """Create a new loan."""
    return service.create_loan(loan_data)


@router.get(
    "",
    response_model=List[LoanResponse],
    summary="Get all loans",
)
async def get_loans(
    customer_id: int | None = Query(None, description="Filter by customer ID"),
    service: LoanService = Depends(get_loan_service),
) -> List[LoanResponse]:
    """Get all loans, optionally filtered by customer."""
    return service.get_loans(customer_id=customer_id)


@router.get(
    "/{loan_id}",
    response_model=LoanResponse,
    summary="Get loan by ID",
)
async def get_loan(
    loan_id: int,
    service: LoanService = Depends(get_loan_service),
) -> LoanResponse:
    """Get a specific loan by ID."""
    return service.get_loan(loan_id)


@router.post(
    "/{loan_id}/approve",
    response_model=LoanResponse,
    summary="Approve a loan",
    description="Approve a pending loan and generate payment schedule",
)
async def approve_loan(
    loan_id: int,
    service: LoanService = Depends(get_loan_service),
) -> LoanResponse:
    """Approve a loan and generate payment schedule."""
    return service.approve_loan(loan_id)


@router.post(
    "/{loan_id}/reject",
    response_model=LoanResponse,
    summary="Reject a loan",
)
async def reject_loan(
    loan_id: int,
    rejection_data: LoanReject,
    service: LoanService = Depends(get_loan_service),
) -> LoanResponse:
    """Reject a loan."""
    return service.reject_loan(loan_id, rejection_data.reason)


@router.post(
    "/{loan_id}/payments",
    response_model=PaymentScheduleResponse,
    summary="Register a payment",
    description="Register a payment for an approved loan",
)
async def register_payment(
    loan_id: int,
    payment_data: PaymentScheduleCreate,
    service: LoanService = Depends(get_loan_service),
) -> PaymentScheduleResponse:
    """Register a payment for a loan."""
    return service.register_payment(loan_id, payment_data.amount, payment_data.paid_date)


@router.get(
    "/{loan_id}/payment-schedule",
    response_model=List[PaymentScheduleResponse],
    summary="Get payment schedule",
    description="Get payment schedule for a loan",
)
async def get_payment_schedule(
    loan_id: int,
    service: LoanService = Depends(get_loan_service),
) -> List[PaymentScheduleResponse]:
    """Get payment schedule for a loan."""
    return service.get_payment_schedule(loan_id)


