"""Vehicle Category repository for database operations."""

from typing import List

from sqlalchemy.orm import Session

from app.models.vehicle_category import VehicleCategory
from app.schemas.vehicle_category import VehicleCategoryCreate


class VehicleCategoryRepository:
    """Repository for vehicle category data access operations."""

    def __init__(self, db: Session) -> None:
        """
        Initialize repository with database session.
        
        Args:
            db: SQLAlchemy database session
        """
        self.db = db

    def create(self, category_data: VehicleCategoryCreate) -> VehicleCategory:
        """
        Create a new vehicle category.
        
        Args:
            category_data: Vehicle category creation data
            
        Returns:
            Created vehicle category instance
        """
        db_category = VehicleCategory(name=category_data.name)
        self.db.add(db_category)
        self.db.commit()
        self.db.refresh(db_category)
        return db_category

    def get_by_id(self, category_id: int) -> VehicleCategory | None:
        """
        Get vehicle category by ID.
        
        Args:
            category_id: Vehicle category ID
            
        Returns:
            Vehicle category instance or None if not found
        """
        return self.db.query(VehicleCategory).filter(VehicleCategory.id == category_id).first()

    def get_all(self) -> List[VehicleCategory]:
        """
        Get all vehicle categories.
        
        Returns:
            List of vehicle category instances
        """
        return self.db.query(VehicleCategory).all()

    def get_by_name(self, name: str) -> VehicleCategory | None:
        """
        Get vehicle category by name.
        
        Args:
            name: Vehicle category name
            
        Returns:
            Vehicle category instance or None if not found
        """
        return self.db.query(VehicleCategory).filter(VehicleCategory.name == name).first()

    def update(self, category_id: int, category_data: VehicleCategoryCreate) -> VehicleCategory | None:
        """
        Update a vehicle category.
        
        Args:
            category_id: Vehicle category ID
            category_data: Updated vehicle category data
            
        Returns:
            Updated vehicle category instance or None if not found
        """
        db_category = self.get_by_id(category_id)
        if db_category is None:
            return None
        db_category.name = category_data.name
        self.db.commit()
        self.db.refresh(db_category)
        return db_category

    def delete(self, category_id: int) -> bool:
        """
        Delete a vehicle category.
        
        Args:
            category_id: Vehicle category ID
            
        Returns:
            True if deleted, False if not found
        """
        db_category = self.get_by_id(category_id)
        if db_category is None:
            return False
        self.db.delete(db_category)
        self.db.commit()
        return True


