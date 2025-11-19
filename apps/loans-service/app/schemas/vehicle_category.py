"""Vehicle Category Pydantic schemas."""

from pydantic import BaseModel, Field


class VehicleCategoryBase(BaseModel):
    """Base vehicle category schema with common fields."""

    name: str = Field(..., min_length=1, max_length=255, description="Category name")


class VehicleCategoryCreate(VehicleCategoryBase):
    """Schema for creating a new vehicle category."""

    pass


class VehicleCategoryResponse(VehicleCategoryBase):
    """Schema for vehicle category response."""

    id: int = Field(..., description="Category ID")

    model_config = {"from_attributes": True}


# Alias for backward compatibility
VehicleCategory = VehicleCategoryResponse


