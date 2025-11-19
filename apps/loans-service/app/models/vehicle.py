"""Vehicle database model."""

from decimal import Decimal

from sqlalchemy import ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Vehicle(Base):
    """Vehicle model for database."""

    __tablename__ = "vehicles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vehicle_categories.id"), nullable=False, index=True
    )
    brand: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    model: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)

    # Relationship
    category: Mapped["VehicleCategory"] = relationship("VehicleCategory", back_populates="vehicles")

    def __repr__(self) -> str:
        """String representation of Vehicle."""
        return f"<Vehicle(id={self.id}, brand='{self.brand}', model='{self.model}', price={self.price})>"


