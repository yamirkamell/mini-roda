"""Vehicle service for business logic."""

from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.vehicle_category_repository import VehicleCategoryRepository
from app.repositories.vehicle_repository import VehicleRepository
from app.schemas.vehicle import VehicleCreate, VehicleResponse


class VehicleService:
    """Service for vehicle business logic."""

    def __init__(self, db: Session) -> None:
        """
        Initialize service with database session.
        
        Args:
            db: SQLAlchemy database session
        """
        self.repository = VehicleRepository(db)
        self.category_repository = VehicleCategoryRepository(db)

    def create_vehicle(self, vehicle_data: VehicleCreate) -> VehicleResponse:
        """
        Create a new vehicle with validation.
        
        Args:
            vehicle_data: Vehicle creation data
            
        Returns:
            Created vehicle response
            
        Raises:
            HTTPException: If category not found
        """
        # Validate category exists
        category = self.category_repository.get_by_id(vehicle_data.category_id)
        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {vehicle_data.category_id} not found",
            )

        db_vehicle = self.repository.create(vehicle_data)
        return VehicleResponse.model_validate(db_vehicle)

    def get_vehicle(self, vehicle_id: int) -> VehicleResponse:
        """
        Get vehicle by ID.
        
        Args:
            vehicle_id: Vehicle ID
            
        Returns:
            Vehicle response
            
        Raises:
            HTTPException: If vehicle not found
        """
        db_vehicle = self.repository.get_by_id(vehicle_id)
        if db_vehicle is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vehicle with id {vehicle_id} not found",
            )
        return VehicleResponse.model_validate(db_vehicle)

    def get_vehicles(self, category_id: int | None = None) -> List[VehicleResponse]:
        """
        Get all vehicles, optionally filtered by category.
        
        Args:
            category_id: Optional category ID to filter by
            
        Returns:
            List of vehicle responses
        """
        db_vehicles = self.repository.get_all(category_id=category_id)
        return [VehicleResponse.model_validate(vehicle) for vehicle in db_vehicles]

    def update_vehicle(self, vehicle_id: int, vehicle_data: VehicleCreate) -> VehicleResponse:
        """
        Update a vehicle.
        
        Args:
            vehicle_id: Vehicle ID
            vehicle_data: Updated vehicle data
            
        Returns:
            Updated vehicle response
            
        Raises:
            HTTPException: If vehicle or category not found
        """
        # Validate category exists
        category = self.category_repository.get_by_id(vehicle_data.category_id)
        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {vehicle_data.category_id} not found",
            )

        db_vehicle = self.repository.update(vehicle_id, vehicle_data)
        if db_vehicle is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vehicle with id {vehicle_id} not found",
            )
        return VehicleResponse.model_validate(db_vehicle)

    def delete_vehicle(self, vehicle_id: int) -> None:
        """
        Delete a vehicle.
        
        Args:
            vehicle_id: Vehicle ID
            
        Raises:
            HTTPException: If vehicle not found
        """
        success = self.repository.delete(vehicle_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vehicle with id {vehicle_id} not found",
            )


