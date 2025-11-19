"""Vehicle Category database model."""

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class VehicleCategory(Base):
    """Vehicle Category model for database."""

    __tablename__ = "vehicle_categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)

    # Relationship
    vehicles: Mapped[list["Vehicle"]] = relationship("Vehicle", back_populates="category")

    def __repr__(self) -> str:
        """String representation of VehicleCategory."""
        return f"<VehicleCategory(id={self.id}, name='{self.name}')>"


