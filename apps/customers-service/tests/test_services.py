"""Unit tests for customer service layer."""

import pytest
from fastapi import HTTPException, status

from app.schemas.customer import CustomerCreate
from app.services.customer_service import CustomerService


def test_create_customer_service(db_session) -> None:
    """Test creating a customer through service."""
    service = CustomerService(db_session)
    customer_data = CustomerCreate(
        name="John Doe",
        email="john.doe@example.com",
        phone="+1234567890",
    )
    
    customer = service.create_customer(customer_data)
    assert customer.name == "John Doe"
    assert customer.email == "john.doe@example.com"
    assert customer.phone == "+1234567890"
    assert customer.id is not None


def test_create_customer_duplicate_email_service(db_session) -> None:
    """Test creating customer with duplicate email through service."""
    service = CustomerService(db_session)
    customer_data = CustomerCreate(
        name="John Doe",
        email="john.doe@example.com",
        phone="+1234567890",
    )
    
    # Create first customer
    service.create_customer(customer_data)
    
    # Try to create second customer with same email
    with pytest.raises(HTTPException) as exc_info:
        service.create_customer(customer_data)
    
    assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
    assert "already exists" in exc_info.value.detail


def test_get_customer_service(db_session) -> None:
    """Test getting a customer through service."""
    service = CustomerService(db_session)
    customer_data = CustomerCreate(
        name="John Doe",
        email="john.doe@example.com",
        phone="+1234567890",
    )
    
    # Create customer
    created_customer = service.create_customer(customer_data)
    
    # Get customer
    customer = service.get_customer(created_customer.id)
    assert customer.id == created_customer.id
    assert customer.name == "John Doe"


def test_get_customer_not_found_service(db_session) -> None:
    """Test getting non-existent customer through service."""
    service = CustomerService(db_session)
    
    with pytest.raises(HTTPException) as exc_info:
        service.get_customer(99999)
    
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert "not found" in exc_info.value.detail


def test_get_all_customers_service(db_session) -> None:
    """Test getting all customers through service."""
    service = CustomerService(db_session)
    
    # Create multiple customers
    for i in range(3):
        customer_data = CustomerCreate(
            name=f"Customer {i}",
            email=f"customer{i}@example.com",
            phone=f"+123456789{i}",
        )
        service.create_customer(customer_data)
    
    # Get all customers
    customers = service.get_customers()
    assert len(customers) == 3


