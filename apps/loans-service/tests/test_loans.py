"""Unit tests for loan endpoints."""

from datetime import datetime
from decimal import Decimal

from fastapi import status


def test_simulate_loan(client) -> None:
    """Test loan simulation."""
    response = client.post(
        "/api/v1/loans/simulate",
        json={
            "amount": "10000.00",
            "interest_rate": "5.5",
            "term_months": 12,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "monthly_payment" in data
    assert "total_amount" in data
    assert Decimal(data["monthly_payment"]) > 0
    assert Decimal(data["total_amount"]) > Decimal("10000.00")


def test_create_loan(client) -> None:
    """Test creating a new loan."""
    response = client.post(
        "/api/v1/loans",
        json={
            "customer_id": 1,
            "amount": "10000.00",
            "interest_rate": "5.5",
            "term_months": 12,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["customer_id"] == 1
    assert data["amount"] == "10000.00"
    assert data["status"] == "pending"
    assert "id" in data
    assert "total_amount" in data


def test_get_loan(client) -> None:
    """Test getting a loan by ID."""
    # Create a loan
    create_response = client.post(
        "/api/v1/loans",
        json={
            "customer_id": 1,
            "amount": "10000.00",
            "interest_rate": "5.5",
            "term_months": 12,
        },
    )
    loan_id = create_response.json()["id"]
    
    # Get the loan
    response = client.get(f"/api/v1/loans/{loan_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == loan_id


def test_approve_loan(client) -> None:
    """Test approving a loan."""
    # Create a loan
    create_response = client.post(
        "/api/v1/loans",
        json={
            "customer_id": 1,
            "amount": "10000.00",
            "interest_rate": "5.5",
            "term_months": 12,
        },
    )
    loan_id = create_response.json()["id"]
    
    # Approve the loan
    response = client.post(f"/api/v1/loans/{loan_id}/approve")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "approved"
    
    # Check payment schedule was generated
    schedule_response = client.get(f"/api/v1/loans/{loan_id}/payment-schedule")
    assert schedule_response.status_code == status.HTTP_200_OK
    schedule_data = schedule_response.json()
    assert len(schedule_data) == 12  # 12 months


def test_reject_loan(client) -> None:
    """Test rejecting a loan."""
    # Create a loan
    create_response = client.post(
        "/api/v1/loans",
        json={
            "customer_id": 1,
            "amount": "10000.00",
            "interest_rate": "5.5",
            "term_months": 12,
        },
    )
    loan_id = create_response.json()["id"]
    
    # Reject the loan
    response = client.post(
        f"/api/v1/loans/{loan_id}/reject",
        json={"reason": "Insufficient credit score"},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "rejected"


def test_register_payment(client) -> None:
    """Test registering a payment."""
    # Create and approve a loan
    create_response = client.post(
        "/api/v1/loans",
        json={
            "customer_id": 1,
            "amount": "10000.00",
            "interest_rate": "5.5",
            "term_months": 12,
        },
    )
    loan_id = create_response.json()["id"]
    client.post(f"/api/v1/loans/{loan_id}/approve")
    
    # Get payment schedule
    schedule_response = client.get(f"/api/v1/loans/{loan_id}/payment-schedule")
    schedule_data = schedule_response.json()
    payment_amount = schedule_data[0]["amount"]
    
    # Register payment
    response = client.post(
        f"/api/v1/loans/{loan_id}/payments",
        json={
            "amount": payment_amount,
            "paid_date": datetime.utcnow().isoformat(),
        },
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["paid"] is True


def test_get_payment_schedule(client) -> None:
    """Test getting payment schedule."""
    # Create and approve a loan
    create_response = client.post(
        "/api/v1/loans",
        json={
            "customer_id": 1,
            "amount": "10000.00",
            "interest_rate": "5.5",
            "term_months": 6,
        },
    )
    loan_id = create_response.json()["id"]
    client.post(f"/api/v1/loans/{loan_id}/approve")
    
    # Get payment schedule
    response = client.get(f"/api/v1/loans/{loan_id}/payment-schedule")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 6  # 6 months
    assert all("due_date" in item for item in data)
    assert all("amount" in item for item in data)


