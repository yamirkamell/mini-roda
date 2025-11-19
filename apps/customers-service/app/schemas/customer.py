"""Customer Pydantic schemas."""

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class CustomerBase(BaseModel):
    """Base customer schema with common fields."""

    name: str = Field(..., min_length=1, max_length=255, description="Customer name")
    email: EmailStr = Field(..., description="Customer email address")
    phone: str | None = Field(None, max_length=50, description="Customer phone number")


class CustomerCreate(CustomerBase):
    """Schema for creating a new customer."""

    pass


class CustomerResponse(CustomerBase):
    """Schema for customer response."""

    id: int = Field(..., description="Customer ID")
    created_at: datetime = Field(..., description="Customer creation timestamp")

    model_config = {"from_attributes": True}


# Alias for backward compatibility
Customer = CustomerResponse


