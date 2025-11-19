"""Unit tests for customer endpoints."""

from fastapi import status


def test_create_customer(client) -> None:
    """Test creating a new customer."""
    response = client.post(
        "/api/v1/customers",
        json={
            "name": "John Doe",
            "email": "john.doe@example.com",
            "phone": "+1234567890",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "John Doe"
    assert data["email"] == "john.doe@example.com"
    assert data["phone"] == "+1234567890"
    assert "id" in data
    assert "created_at" in data


def test_create_customer_duplicate_email(client) -> None:
    """Test creating a customer with duplicate email."""
    # Create first customer
    client.post(
        "/api/v1/customers",
        json={
            "name": "John Doe",
            "email": "john.doe@example.com",
            "phone": "+1234567890",
        },
    )
    
    # Try to create second customer with same email
    response = client.post(
        "/api/v1/customers",
        json={
            "name": "Jane Doe",
            "email": "john.doe@example.com",
            "phone": "+0987654321",
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already exists" in response.json()["detail"]


def test_get_customer(client) -> None:
    """Test getting a customer by ID."""
    # Create a customer
    create_response = client.post(
        "/api/v1/customers",
        json={
            "name": "John Doe",
            "email": "john.doe@example.com",
            "phone": "+1234567890",
        },
    )
    customer_id = create_response.json()["id"]
    
    # Get the customer
    response = client.get(f"/api/v1/customers/{customer_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == customer_id
    assert data["name"] == "John Doe"
    assert data["email"] == "john.doe@example.com"


def test_get_customer_not_found(client) -> None:
    """Test getting a non-existent customer."""
    response = client.get("/api/v1/customers/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "not found" in response.json()["detail"]


def test_get_all_customers(client) -> None:
    """Test getting all customers."""
    # Create multiple customers
    client.post(
        "/api/v1/customers",
        json={
            "name": "John Doe",
            "email": "john.doe@example.com",
            "phone": "+1234567890",
        },
    )
    client.post(
        "/api/v1/customers",
        json={
            "name": "Jane Smith",
            "email": "jane.smith@example.com",
            "phone": "+0987654321",
        },
    )
    
    # Get all customers
    response = client.get("/api/v1/customers")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] in ["John Doe", "Jane Smith"]
    assert data[1]["name"] in ["John Doe", "Jane Smith"]


def test_get_all_customers_pagination(client) -> None:
    """Test getting customers with pagination."""
    # Create multiple customers
    for i in range(5):
        client.post(
            "/api/v1/customers",
            json={
                "name": f"Customer {i}",
                "email": f"customer{i}@example.com",
                "phone": f"+123456789{i}",
            },
        )
    
    # Get customers with limit
    response = client.get("/api/v1/customers?skip=0&limit=3")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 3


def test_health_endpoint(client) -> None:
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "healthy"}


def test_root_endpoint(client) -> None:
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["service"] == "customers-service"
    assert data["status"] == "running"


