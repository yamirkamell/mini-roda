"""API dependencies."""

from typing import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.customer_service import CustomerService


def get_customer_service(
    db: Session = Depends(get_db),
) -> Generator[CustomerService, None, None]:
    """
    Dependency to get customer service instance.
    
    Args:
        db: Database session dependency
        
    Yields:
        CustomerService instance
    """
    yield CustomerService(db)


