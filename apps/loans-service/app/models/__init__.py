"""Database models."""

from app.models.loan import Loan
from app.models.payment_schedule import PaymentSchedule
from app.models.vehicle import Vehicle
from app.models.vehicle_category import VehicleCategory

__all__ = ["VehicleCategory", "Vehicle", "Loan", "PaymentSchedule"]


