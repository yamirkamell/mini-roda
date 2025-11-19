"""Repository layer for data access."""

from app.repositories.loan_repository import LoanRepository
from app.repositories.payment_schedule_repository import PaymentScheduleRepository
from app.repositories.vehicle_category_repository import VehicleCategoryRepository
from app.repositories.vehicle_repository import VehicleRepository

__all__ = [
    "VehicleCategoryRepository",
    "VehicleRepository",
    "LoanRepository",
    "PaymentScheduleRepository",
]


