"""Vehicle API endpoints."""

from typing import List

from fastapi import APIRouter, Depends, Query, status

from app.api.dependencies import get_vehicle_service
from app.schemas.vehicle import VehicleCreate, VehicleResponse
from app.services.vehicle_service import VehicleService

router = APIRouter(prefix="/vehicles", tags=["vehicles"])


@router.post(
    "",
    response_model=VehicleResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new vehicle",
)
async def create_vehicle(
    vehicle_data: VehicleCreate,
    service: VehicleService = Depends(get_vehicle_service),
) -> VehicleResponse:
    """Create a new vehicle."""
    return service.create_vehicle(vehicle_data)


@router.get(
    "",
    response_model=List[VehicleResponse],
    summary="Get all vehicles",
)
async def get_vehicles(
    category_id: int | None = Query(None, description="Filter by category ID"),
    service: VehicleService = Depends(get_vehicle_service),
) -> List[VehicleResponse]:
    """Get all vehicles, optionally filtered by category."""
    return service.get_vehicles(category_id=category_id)


@router.get(
    "/{vehicle_id}",
    response_model=VehicleResponse,
    summary="Get vehicle by ID",
)
async def get_vehicle(
    vehicle_id: int,
    service: VehicleService = Depends(get_vehicle_service),
) -> VehicleResponse:
    """Get a specific vehicle by ID."""
    return service.get_vehicle(vehicle_id)


@router.put(
    "/{vehicle_id}",
    response_model=VehicleResponse,
    summary="Update a vehicle",
)
async def update_vehicle(
    vehicle_id: int,
    vehicle_data: VehicleCreate,
    service: VehicleService = Depends(get_vehicle_service),
) -> VehicleResponse:
    """Update a vehicle."""
    return service.update_vehicle(vehicle_id, vehicle_data)


@router.delete(
    "/{vehicle_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a vehicle",
)
async def delete_vehicle(
    vehicle_id: int,
    service: VehicleService = Depends(get_vehicle_service),
) -> None:
    """Delete a vehicle."""
    service.delete_vehicle(vehicle_id)


