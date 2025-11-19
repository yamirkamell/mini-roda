"""Unit tests for customer repository layer."""

from app.models.customer import Customer
from app.repositories.customer_repository import CustomerRepository
from app.schemas.customer import CustomerCreate


def test_create_customer_repository(db_session) -> None:
    """Test creating a customer through repository."""
    repository = CustomerRepository(db_session)
    customer_data = CustomerCreate(
        name="John Doe",
        email="john.doe@example.com",
        phone="+1234567890",
    )
    
    customer = repository.create(customer_data)
    assert isinstance(customer, Customer)
    assert customer.name == "John Doe"
    assert customer.email == "john.doe@example.com"
    assert customer.id is not None


def test_get_by_id_repository(db_session) -> None:
    """Test getting customer by ID through repository."""
    repository = CustomerRepository(db_session)
    customer_data = CustomerCreate(
        name="John Doe",
        email="john.doe@example.com",
        phone="+1234567890",
    )
    
    # Create customer
    created_customer = repository.create(customer_data)
    
    # Get by ID
    customer = repository.get_by_id(created_customer.id)
    assert customer is not None
    assert customer.id == created_customer.id
    assert customer.name == "John Doe"


def test_get_by_id_not_found_repository(db_session) -> None:
    """Test getting non-existent customer by ID through repository."""
    repository = CustomerRepository(db_session)
    customer = repository.get_by_id(99999)
    assert customer is None


def test_get_by_email_repository(db_session) -> None:
    """Test getting customer by email through repository."""
    repository = CustomerRepository(db_session)
    customer_data = CustomerCreate(
        name="John Doe",
        email="john.doe@example.com",
        phone="+1234567890",
    )
    
    # Create customer
    repository.create(customer_data)
    
    # Get by email
    customer = repository.get_by_email("john.doe@example.com")
    assert customer is not None
    assert customer.email == "john.doe@example.com"


def test_get_all_repository(db_session) -> None:
    """Test getting all customers through repository."""
    repository = CustomerRepository(db_session)
    
    # Create multiple customers
    for i in range(3):
        customer_data = CustomerCreate(
            name=f"Customer {i}",
            email=f"customer{i}@example.com",
            phone=f"+123456789{i}",
        )
        repository.create(customer_data)
    
    # Get all customers
    customers = repository.get_all()
    assert len(customers) == 3


def test_get_all_with_pagination_repository(db_session) -> None:
    """Test getting customers with pagination through repository."""
    repository = CustomerRepository(db_session)
    
    # Create multiple customers
    for i in range(5):
        customer_data = CustomerCreate(
            name=f"Customer {i}",
            email=f"customer{i}@example.com",
            phone=f"+123456789{i}",
        )
        repository.create(customer_data)
    
    # Get with pagination
    customers = repository.get_all(skip=0, limit=3)
    assert len(customers) == 3
    
    customers = repository.get_all(skip=3, limit=3)
    assert len(customers) == 2


