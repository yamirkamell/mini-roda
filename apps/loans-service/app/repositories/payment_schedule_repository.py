"""Payment Schedule repository for database operations."""

from datetime import datetime
from decimal import Decimal
from typing import List

from sqlalchemy.orm import Session

from app.models.payment_schedule import PaymentSchedule


class PaymentScheduleRepository:
    """Repository for payment schedule data access operations."""

    def __init__(self, db: Session) -> None:
        """
        Initialize repository with database session.
        
        Args:
            db: SQLAlchemy database session
        """
        self.db = db

    def create(self, loan_id: int, due_date: datetime, amount: Decimal) -> PaymentSchedule:
        """
        Create a new payment schedule entry.
        
        Args:
            loan_id: Loan ID
            due_date: Payment due date
            amount: Payment amount
            
        Returns:
            Created payment schedule instance
        """
        db_payment = PaymentSchedule(
            loan_id=loan_id,
            due_date=due_date,
            amount=amount,
            paid=False,
        )
        self.db.add(db_payment)
        self.db.commit()
        self.db.refresh(db_payment)
        return db_payment

    def get_by_loan_id(self, loan_id: int) -> List[PaymentSchedule]:
        """
        Get all payment schedules for a loan.
        
        Args:
            loan_id: Loan ID
            
        Returns:
            List of payment schedule instances
        """
        return (
            self.db.query(PaymentSchedule)
            .filter(PaymentSchedule.loan_id == loan_id)
            .order_by(PaymentSchedule.due_date)
            .all()
        )

    def get_by_id(self, payment_id: int) -> PaymentSchedule | None:
        """
        Get payment schedule by ID.
        
        Args:
            payment_id: Payment schedule ID
            
        Returns:
            Payment schedule instance or None if not found
        """
        return (
            self.db.query(PaymentSchedule).filter(PaymentSchedule.id == payment_id).first()
        )

    def mark_as_paid(self, payment_id: int, paid_date: datetime) -> PaymentSchedule | None:
        """
        Mark a payment schedule as paid.
        
        Args:
            payment_id: Payment schedule ID
            paid_date: Date when payment was made
            
        Returns:
            Updated payment schedule instance or None if not found
        """
        db_payment = self.get_by_id(payment_id)
        if db_payment is None:
            return None
        db_payment.paid = True
        db_payment.paid_date = paid_date
        self.db.commit()
        self.db.refresh(db_payment)
        return db_payment

    def register_payment(
        self, loan_id: int, amount: Decimal, paid_date: datetime
    ) -> PaymentSchedule | None:
        """
        Register a payment for a loan (marks the next unpaid schedule as paid).
        
        Args:
            loan_id: Loan ID
            amount: Payment amount
            paid_date: Date when payment was made
            
        Returns:
            Updated payment schedule instance or None if not found
        """
        # Find the next unpaid payment schedule
        unpaid_payment = (
            self.db.query(PaymentSchedule)
            .filter(PaymentSchedule.loan_id == loan_id, PaymentSchedule.paid == False)
            .order_by(PaymentSchedule.due_date)
            .first()
        )
        
        if unpaid_payment is None:
            return None
        
        # Check if payment amount matches
        if unpaid_payment.amount != amount:
            return None
        
        return self.mark_as_paid(unpaid_payment.id, paid_date)


