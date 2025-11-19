"""Vehicle repository for database operations."""

from typing import List

from sqlalchemy.orm import Session

from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate


class VehicleRepository:
    """Repository for vehicle data access operations."""

    def __init__(self, db: Session) -> None:
        """
        Initialize repository with database session.
        
        Args:
            db: SQLAlchemy database session
        """
        self.db = db

    def create(self, vehicle_data: VehicleCreate) -> Vehicle:
        """
        Create a new vehicle.
        
        Args:
            vehicle_data: Vehicle creation data
            
        Returns:
            Created vehicle instance
        """
        db_vehicle = Vehicle(
            category_id=vehicle_data.category_id,
            brand=vehicle_data.brand,
            model=vehicle_data.model,
            price=vehicle_data.price,
        )
        self.db.add(db_vehicle)
        self.db.commit()
        self.db.refresh(db_vehicle)
        return db_vehicle

    def get_by_id(self, vehicle_id: int) -> Vehicle | None:
        """
        Get vehicle by ID.
        
        Args:
            vehicle_id: Vehicle ID
            
        Returns:
            Vehicle instance or None if not found
        """
        return self.db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()

    def get_all(self, category_id: int | None = None) -> List[Vehicle]:
        """
        Get all vehicles, optionally filtered by category.
        
        Args:
            category_id: Optional category ID to filter by
            
        Returns:
            List of vehicle instances
        """
        query = self.db.query(Vehicle)
        if category_id is not None:
            query = query.filter(Vehicle.category_id == category_id)
        return query.all()

    def update(self, vehicle_id: int, vehicle_data: VehicleCreate) -> Vehicle | None:
        """
        Update a vehicle.
        
        Args:
            vehicle_id: Vehicle ID
            vehicle_data: Updated vehicle data
            
        Returns:
            Updated vehicle instance or None if not found
        """
        db_vehicle = self.get_by_id(vehicle_id)
        if db_vehicle is None:
            return None
        db_vehicle.category_id = vehicle_data.category_id
        db_vehicle.brand = vehicle_data.brand
        db_vehicle.model = vehicle_data.model
        db_vehicle.price = vehicle_data.price
        self.db.commit()
        self.db.refresh(db_vehicle)
        return db_vehicle

    def delete(self, vehicle_id: int) -> bool:
        """
        Delete a vehicle.
        
        Args:
            vehicle_id: Vehicle ID
            
        Returns:
            True if deleted, False if not found
        """
        db_vehicle = self.get_by_id(vehicle_id)
        if db_vehicle is None:
            return False
        self.db.delete(db_vehicle)
        self.db.commit()
        return True


