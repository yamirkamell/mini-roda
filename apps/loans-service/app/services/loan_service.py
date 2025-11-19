"""Loan service for business logic."""

from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.loan_repository import LoanRepository
from app.repositories.payment_schedule_repository import PaymentScheduleRepository
from app.schemas.loan import (
    LoanCreate,
    LoanResponse,
    LoanSimulate,
    LoanSimulateResponse,
)
from app.schemas.payment_schedule import PaymentScheduleResponse


class LoanService:
    """Service for loan business logic."""

    def __init__(self, db: Session) -> None:
        """
        Initialize service with database session.
        
        Args:
            db: SQLAlchemy database session
        """
        self.repository = LoanRepository(db)
        self.payment_repository = PaymentScheduleRepository(db)

    def simulate_loan(self, simulation_data: LoanSimulate) -> LoanSimulateResponse:
        """
        Simulate a loan to calculate monthly payment and total amount.
        
        Uses the formula: M = P * [r(1+r)^n] / [(1+r)^n - 1]
        Where:
        - M = Monthly payment
        - P = Principal (loan amount)
        - r = Monthly interest rate (annual rate / 12 / 100)
        - n = Number of months
        
        Args:
            simulation_data: Loan simulation data
            
        Returns:
            Loan simulation response with monthly payment and total amount
        """
        principal = float(simulation_data.amount)
        annual_rate = float(simulation_data.interest_rate)
        months = simulation_data.term_months

        # Calculate monthly interest rate
        monthly_rate = annual_rate / 12 / 100

        # Calculate monthly payment using amortization formula
        if monthly_rate == 0:
            monthly_payment = principal / months
        else:
            monthly_payment = principal * (
                monthly_rate * (1 + monthly_rate) ** months
            ) / ((1 + monthly_rate) ** months - 1)

        # Calculate total amount
        total_amount = monthly_payment * months

        return LoanSimulateResponse(
            monthly_payment=Decimal(str(round(monthly_payment, 2))),
            total_amount=Decimal(str(round(total_amount, 2))),
        )

    def create_loan(self, loan_data: LoanCreate) -> LoanResponse:
        """
        Create a new loan.
        
        Args:
            loan_data: Loan creation data
            
        Returns:
            Created loan response
        """
        # Calculate total amount using simulation
        simulation = LoanSimulate(
            amount=loan_data.amount,
            interest_rate=loan_data.interest_rate,
            term_months=loan_data.term_months,
        )
        simulation_result = self.simulate_loan(simulation)

        # Create loan
        db_loan = self.repository.create(loan_data, simulation_result.total_amount)
        return LoanResponse.model_validate(db_loan)

    def get_loan(self, loan_id: int) -> LoanResponse:
        """
        Get loan by ID.
        
        Args:
            loan_id: Loan ID
            
        Returns:
            Loan response
            
        Raises:
            HTTPException: If loan not found
        """
        db_loan = self.repository.get_by_id(loan_id)
        if db_loan is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Loan with id {loan_id} not found",
            )
        return LoanResponse.model_validate(db_loan)

    def get_loans(self, customer_id: int | None = None) -> List[LoanResponse]:
        """
        Get all loans, optionally filtered by customer.
        
        Args:
            customer_id: Optional customer ID to filter by
            
        Returns:
            List of loan responses
        """
        db_loans = self.repository.get_all(customer_id=customer_id)
        return [LoanResponse.model_validate(loan) for loan in db_loans]

    def approve_loan(self, loan_id: int) -> LoanResponse:
        """
        Approve a loan and generate payment schedule.
        
        Args:
            loan_id: Loan ID
            
        Returns:
            Approved loan response
            
        Raises:
            HTTPException: If loan not found or already processed
        """
        db_loan = self.repository.get_by_id(loan_id)
        if db_loan is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Loan with id {loan_id} not found",
            )

        if db_loan.status != "pending":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Loan with id {loan_id} is already {db_loan.status}",
            )

        # Update loan status
        updated_loan = self.repository.update_status(loan_id, "approved")
        if updated_loan is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update loan status",
            )

        # Generate payment schedule
        self._generate_payment_schedule(updated_loan)

        # Refresh loan
        db_loan = self.repository.get_by_id(loan_id)
        return LoanResponse.model_validate(db_loan)

    def reject_loan(self, loan_id: int, reason: str) -> LoanResponse:
        """
        Reject a loan.
        
        Args:
            loan_id: Loan ID
            reason: Rejection reason
            
        Returns:
            Rejected loan response
            
        Raises:
            HTTPException: If loan not found or already processed
        """
        db_loan = self.repository.get_by_id(loan_id)
        if db_loan is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Loan with id {loan_id} not found",
            )

        if db_loan.status != "pending":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Loan with id {loan_id} is already {db_loan.status}",
            )

        # Update loan status
        self.repository.update_status(loan_id, "rejected")

        # Refresh loan
        db_loan = self.repository.get_by_id(loan_id)
        return LoanResponse.model_validate(db_loan)

    def _generate_payment_schedule(self, loan) -> None:
        """
        Generate payment schedule for an approved loan.
        
        Args:
            loan: Loan database model instance
        """
        # Calculate monthly payment
        from decimal import Decimal
        simulation = LoanSimulate(
            amount=Decimal(str(loan.amount)),
            interest_rate=Decimal(str(loan.interest_rate)),
            term_months=loan.term_months,
        )
        simulation_result = self.simulate_loan(simulation)
        monthly_payment = simulation_result.monthly_payment

        # Generate payment schedule starting from next month
        start_date = datetime.now(timezone.utc).replace(day=1) + timedelta(days=32)
        start_date = start_date.replace(day=1)  # First day of next month

        for month in range(loan.term_months):
            due_date = start_date + timedelta(days=month * 30)  # Approximate monthly
            # Adjust to first day of the month
            due_date = due_date.replace(day=1)
            self.payment_repository.create(loan.id, due_date, monthly_payment)

    def register_payment(
        self, loan_id: int, amount: Decimal, paid_date: datetime
    ) -> PaymentScheduleResponse:
        """
        Register a payment for a loan.
        
        Args:
            loan_id: Loan ID
            amount: Payment amount
            paid_date: Date when payment was made
            
        Returns:
            Updated payment schedule response
            
        Raises:
            HTTPException: If loan not found or payment cannot be registered
        """
        db_loan = self.repository.get_by_id(loan_id)
        if db_loan is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Loan with id {loan_id} not found",
            )

        if db_loan.status != "approved":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Loan with id {loan_id} is not approved",
            )

        db_payment = self.payment_repository.register_payment(loan_id, amount, paid_date)
        if db_payment is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Payment could not be registered. Check amount and loan status.",
            )

        return PaymentScheduleResponse.model_validate(db_payment)

    def get_payment_schedule(self, loan_id: int) -> List[PaymentScheduleResponse]:
        """
        Get payment schedule for a loan.
        
        Args:
            loan_id: Loan ID
            
        Returns:
            List of payment schedule responses
            
        Raises:
            HTTPException: If loan not found
        """
        db_loan = self.repository.get_by_id(loan_id)
        if db_loan is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Loan with id {loan_id} not found",
            )

        db_payments = self.payment_repository.get_by_loan_id(loan_id)
        return [PaymentScheduleResponse.model_validate(payment) for payment in db_payments]

