"""Vehicle Pydantic schemas."""

from decimal import Decimal

from pydantic import BaseModel, Field


class VehicleBase(BaseModel):
    """Base vehicle schema with common fields."""

    category_id: int = Field(..., description="Vehicle category ID")
    brand: str = Field(..., min_length=1, max_length=255, description="Vehicle brand")
    model: str = Field(..., min_length=1, max_length=255, description="Vehicle model")
    price: Decimal = Field(..., gt=0, description="Vehicle price")


class VehicleCreate(VehicleBase):
    """Schema for creating a new vehicle."""

    pass


class VehicleResponse(VehicleBase):
    """Schema for vehicle response."""

    id: int = Field(..., description="Vehicle ID")

    model_config = {"from_attributes": True}


# Alias for backward compatibility
Vehicle = VehicleResponse


