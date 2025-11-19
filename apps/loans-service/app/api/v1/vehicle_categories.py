"""Vehicle Category API endpoints."""

from typing import List

from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_vehicle_category_service
from app.schemas.vehicle_category import VehicleCategoryCreate, VehicleCategoryResponse
from app.services.vehicle_category_service import VehicleCategoryService

router = APIRouter(prefix="/vehicle-categories", tags=["vehicle-categories"])


@router.post(
    "",
    response_model=VehicleCategoryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new vehicle category",
)
async def create_category(
    category_data: VehicleCategoryCreate,
    service: VehicleCategoryService = Depends(get_vehicle_category_service),
) -> VehicleCategoryResponse:
    """Create a new vehicle category."""
    return service.create_category(category_data)


@router.get(
    "",
    response_model=List[VehicleCategoryResponse],
    summary="Get all vehicle categories",
)
async def get_categories(
    service: VehicleCategoryService = Depends(get_vehicle_category_service),
) -> List[VehicleCategoryResponse]:
    """Get all vehicle categories."""
    return service.get_categories()


@router.get(
    "/{category_id}",
    response_model=VehicleCategoryResponse,
    summary="Get vehicle category by ID",
)
async def get_category(
    category_id: int,
    service: VehicleCategoryService = Depends(get_vehicle_category_service),
) -> VehicleCategoryResponse:
    """Get a specific vehicle category by ID."""
    return service.get_category(category_id)


@router.put(
    "/{category_id}",
    response_model=VehicleCategoryResponse,
    summary="Update a vehicle category",
)
async def update_category(
    category_id: int,
    category_data: VehicleCategoryCreate,
    service: VehicleCategoryService = Depends(get_vehicle_category_service),
) -> VehicleCategoryResponse:
    """Update a vehicle category."""
    return service.update_category(category_id, category_data)


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a vehicle category",
)
async def delete_category(
    category_id: int,
    service: VehicleCategoryService = Depends(get_vehicle_category_service),
) -> None:
    """Delete a vehicle category."""
    service.delete_category(category_id)


