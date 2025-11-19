"""Vehicle Category service for business logic."""

from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.vehicle_category_repository import VehicleCategoryRepository
from app.schemas.vehicle_category import VehicleCategoryCreate, VehicleCategoryResponse


class VehicleCategoryService:
    """Service for vehicle category business logic."""

    def __init__(self, db: Session) -> None:
        """
        Initialize service with database session.
        
        Args:
            db: SQLAlchemy database session
        """
        self.repository = VehicleCategoryRepository(db)

    def create_category(self, category_data: VehicleCategoryCreate) -> VehicleCategoryResponse:
        """
        Create a new vehicle category with validation.
        
        Args:
            category_data: Vehicle category creation data
            
        Returns:
            Created vehicle category response
            
        Raises:
            HTTPException: If category with name already exists
        """
        existing_category = self.repository.get_by_name(category_data.name)
        if existing_category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Category with name '{category_data.name}' already exists",
            )

        db_category = self.repository.create(category_data)
        return VehicleCategoryResponse.model_validate(db_category)

    def get_category(self, category_id: int) -> VehicleCategoryResponse:
        """
        Get vehicle category by ID.
        
        Args:
            category_id: Vehicle category ID
            
        Returns:
            Vehicle category response
            
        Raises:
            HTTPException: If category not found
        """
        db_category = self.repository.get_by_id(category_id)
        if db_category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {category_id} not found",
            )
        return VehicleCategoryResponse.model_validate(db_category)

    def get_categories(self) -> List[VehicleCategoryResponse]:
        """
        Get all vehicle categories.
        
        Returns:
            List of vehicle category responses
        """
        db_categories = self.repository.get_all()
        return [VehicleCategoryResponse.model_validate(cat) for cat in db_categories]

    def update_category(
        self, category_id: int, category_data: VehicleCategoryCreate
    ) -> VehicleCategoryResponse:
        """
        Update a vehicle category.
        
        Args:
            category_id: Vehicle category ID
            category_data: Updated vehicle category data
            
        Returns:
            Updated vehicle category response
            
        Raises:
            HTTPException: If category not found or name already exists
        """
        existing_category = self.repository.get_by_name(category_data.name)
        if existing_category and existing_category.id != category_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Category with name '{category_data.name}' already exists",
            )

        db_category = self.repository.update(category_id, category_data)
        if db_category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {category_id} not found",
            )
        return VehicleCategoryResponse.model_validate(db_category)

    def delete_category(self, category_id: int) -> None:
        """
        Delete a vehicle category.
        
        Args:
            category_id: Vehicle category ID
            
        Raises:
            HTTPException: If category not found
        """
        success = self.repository.delete(category_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {category_id} not found",
            )


