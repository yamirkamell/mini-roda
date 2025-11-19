"""Customer repository for database operations."""

from typing import List

from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.schemas.customer import CustomerCreate


class CustomerRepository:
    """Repository for customer data access operations."""

    def __init__(self, db: Session) -> None:
        """
        Initialize repository with database session.
        
        Args:
            db: SQLAlchemy database session
        """
        self.db = db

    def create(self, customer_data: CustomerCreate) -> Customer:
        """
        Create a new customer.
        
        Args:
            customer_data: Customer creation data
            
        Returns:
            Created customer instance
        """
        db_customer = Customer(
            name=customer_data.name,
            email=customer_data.email,
            phone=customer_data.phone,
        )
        self.db.add(db_customer)
        self.db.commit()
        self.db.refresh(db_customer)
        return db_customer

    def get_by_id(self, customer_id: int) -> Customer | None:
        """
        Get customer by ID.
        
        Args:
            customer_id: Customer ID
            
        Returns:
            Customer instance or None if not found
        """
        return self.db.query(Customer).filter(Customer.id == customer_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Customer]:
        """
        Get all customers with pagination.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of customer instances
        """
        return self.db.query(Customer).offset(skip).limit(limit).all()

    def get_by_email(self, email: str) -> Customer | None:
        """
        Get customer by email.
        
        Args:
            email: Customer email
            
        Returns:
            Customer instance or None if not found
        """
        return self.db.query(Customer).filter(Customer.email == email).first()


