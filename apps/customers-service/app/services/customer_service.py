"""Customer service for business logic."""

from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.customer_repository import CustomerRepository
from app.schemas.customer import CustomerCreate, CustomerResponse


class CustomerService:
    """Service for customer business logic."""

    def __init__(self, db: Session) -> None:
        """
        Initialize service with database session.
        
        Args:
            db: SQLAlchemy database session
        """
        self.repository = CustomerRepository(db)

    def create_customer(self, customer_data: CustomerCreate) -> CustomerResponse:
        """
        Create a new customer with validation.
        
        Args:
            customer_data: Customer creation data
            
        Returns:
            Created customer response
            
        Raises:
            HTTPException: If customer with email already exists
        """
        # Check if customer with email already exists
        existing_customer = self.repository.get_by_email(customer_data.email)
        if existing_customer:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Customer with email {customer_data.email} already exists",
            )

        db_customer = self.repository.create(customer_data)
        return CustomerResponse.model_validate(db_customer)

    def get_customer(self, customer_id: int) -> CustomerResponse:
        """
        Get customer by ID.
        
        Args:
            customer_id: Customer ID
            
        Returns:
            Customer response
            
        Raises:
            HTTPException: If customer not found
        """
        db_customer = self.repository.get_by_id(customer_id)
        if db_customer is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Customer with id {customer_id} not found",
            )
        return CustomerResponse.model_validate(db_customer)

    def get_customers(self, skip: int = 0, limit: int = 100) -> List[CustomerResponse]:
        """
        Get all customers with pagination.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of customer responses
        """
        db_customers = self.repository.get_all(skip=skip, limit=limit)
        return [CustomerResponse.model_validate(customer) for customer in db_customers]


