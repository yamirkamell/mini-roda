"""Customer API endpoints."""

from typing import List

from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_customer_service
from app.schemas.customer import CustomerCreate, CustomerResponse
from app.services.customer_service import CustomerService

router = APIRouter(prefix="/customers", tags=["customers"])


@router.post(
    "",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new customer",
    description="Create a new customer with name, email, and optional phone number",
)
async def create_customer(
    customer_data: CustomerCreate,
    service: CustomerService = Depends(get_customer_service),
) -> CustomerResponse:
    """
    Create a new customer.
    
    Args:
        customer_data: Customer creation data
        service: Customer service dependency
        
    Returns:
        Created customer response
    """
    return service.create_customer(customer_data)


@router.get(
    "",
    response_model=List[CustomerResponse],
    summary="Get all customers",
    description="Retrieve a list of all customers with optional pagination",
)
async def get_customers(
    skip: int = 0,
    limit: int = 100,
    service: CustomerService = Depends(get_customer_service),
) -> List[CustomerResponse]:
    """
    Get all customers.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        service: Customer service dependency
        
    Returns:
        List of customer responses
    """
    return service.get_customers(skip=skip, limit=limit)


@router.get(
    "/{customer_id}",
    response_model=CustomerResponse,
    summary="Get customer by ID",
    description="Retrieve a specific customer by their ID",
)
async def get_customer(
    customer_id: int,
    service: CustomerService = Depends(get_customer_service),
) -> CustomerResponse:
    """
    Get customer by ID.
    
    Args:
        customer_id: Customer ID
        service: Customer service dependency
        
    Returns:
        Customer response
    """
    return service.get_customer(customer_id)


