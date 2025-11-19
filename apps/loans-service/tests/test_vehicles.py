"""Unit tests for vehicle endpoints."""

from decimal import Decimal

from fastapi import status


def test_create_vehicle_category(client) -> None:
    """Test creating a vehicle category."""
    response = client.post(
        "/api/v1/vehicle-categories",
        json={"name": "Sedan"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Sedan"
    assert "id" in data


def test_create_vehicle(client) -> None:
    """Test creating a vehicle."""
    # Create category first
    category_response = client.post(
        "/api/v1/vehicle-categories",
        json={"name": "Sedan"},
    )
    category_id = category_response.json()["id"]
    
    # Create vehicle
    response = client.post(
        "/api/v1/vehicles",
        json={
            "category_id": category_id,
            "brand": "Toyota",
            "model": "Camry",
            "price": "25000.00",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["brand"] == "Toyota"
    assert data["model"] == "Camry"
    assert data["price"] == "25000.00"


def test_get_vehicles(client) -> None:
    """Test getting all vehicles."""
    # Create category and vehicles
    category_response = client.post(
        "/api/v1/vehicle-categories",
        json={"name": "SUV"},
    )
    category_id = category_response.json()["id"]
    
    client.post(
        "/api/v1/vehicles",
        json={
            "category_id": category_id,
            "brand": "Honda",
            "model": "CR-V",
            "price": "30000.00",
        },
    )
    
    # Get all vehicles
    response = client.get("/api/v1/vehicles")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 1


def test_get_vehicles_by_category(client) -> None:
    """Test getting vehicles filtered by category."""
    # Create categories
    cat1_response = client.post(
        "/api/v1/vehicle-categories",
        json={"name": "Sedan"},
    )
    cat1_id = cat1_response.json()["id"]
    
    cat2_response = client.post(
        "/api/v1/vehicle-categories",
        json={"name": "SUV"},
    )
    cat2_id = cat2_response.json()["id"]
    
    # Create vehicles
    client.post(
        "/api/v1/vehicles",
        json={
            "category_id": cat1_id,
            "brand": "Toyota",
            "model": "Camry",
            "price": "25000.00",
        },
    )
    client.post(
        "/api/v1/vehicles",
        json={
            "category_id": cat2_id,
            "brand": "Honda",
            "model": "CR-V",
            "price": "30000.00",
        },
    )
    
    # Get vehicles by category
    response = client.get(f"/api/v1/vehicles?category_id={cat1_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["category_id"] == cat1_id


