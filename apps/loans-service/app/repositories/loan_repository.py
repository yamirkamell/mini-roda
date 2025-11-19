"""Loan repository for database operations."""

from decimal import Decimal
from typing import List

from sqlalchemy.orm import Session

from app.models.loan import Loan
from app.schemas.loan import LoanCreate


class LoanRepository:
    """Repository for loan data access operations."""

    def __init__(self, db: Session) -> None:
        """
        Initialize repository with database session.
        
        Args:
            db: SQLAlchemy database session
        """
        self.db = db

    def create(self, loan_data: LoanCreate, total_amount: Decimal) -> Loan:
        """
        Create a new loan.
        
        Args:
            loan_data: Loan creation data
            total_amount: Calculated total amount
            
        Returns:
            Created loan instance
        """
        db_loan = Loan(
            customer_id=loan_data.customer_id,
            amount=loan_data.amount,
            interest_rate=loan_data.interest_rate,
            term_months=loan_data.term_months,
            total_amount=total_amount,
            status="pending",
        )
        self.db.add(db_loan)
        self.db.commit()
        self.db.refresh(db_loan)
        return db_loan

    def get_by_id(self, loan_id: int) -> Loan | None:
        """
        Get loan by ID.
        
        Args:
            loan_id: Loan ID
            
        Returns:
            Loan instance or None if not found
        """
        return self.db.query(Loan).filter(Loan.id == loan_id).first()

    def get_all(self, customer_id: int | None = None) -> List[Loan]:
        """
        Get all loans, optionally filtered by customer.
        
        Args:
            customer_id: Optional customer ID to filter by
            
        Returns:
            List of loan instances
        """
        query = self.db.query(Loan)
        if customer_id is not None:
            query = query.filter(Loan.customer_id == customer_id)
        return query.all()

    def update_status(self, loan_id: int, status: str) -> Loan | None:
        """
        Update loan status.
        
        Args:
            loan_id: Loan ID
            status: New status
            
        Returns:
            Updated loan instance or None if not found
        """
        db_loan = self.get_by_id(loan_id)
        if db_loan is None:
            return None
        db_loan.status = status
        self.db.commit()
        self.db.refresh(db_loan)
        return db_loan


