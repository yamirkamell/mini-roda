"""API dependencies."""

from typing import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.loan_service import LoanService
from app.services.vehicle_category_service import VehicleCategoryService
from app.services.vehicle_service import VehicleService


def get_vehicle_category_service(
    db: Session = Depends(get_db),
) -> Generator[VehicleCategoryService, None, None]:
    """
    Dependency to get vehicle category service instance.
    
    Args:
        db: Database session dependency
        
    Yields:
        VehicleCategoryService instance
    """
    yield VehicleCategoryService(db)


def get_vehicle_service(
    db: Session = Depends(get_db),
) -> Generator[VehicleService, None, None]:
    """
    Dependency to get vehicle service instance.
    
    Args:
        db: Database session dependency
        
    Yields:
        VehicleService instance
    """
    yield VehicleService(db)


def get_loan_service(
    db: Session = Depends(get_db),
) -> Generator[LoanService, None, None]:
    """
    Dependency to get loan service instance.
    
    Args:
        db: Database session dependency
        
    Yields:
        LoanService instance
    """
    yield LoanService(db)


