"""Pydantic schemas for request/response validation."""

from app.schemas.loan import (
    Loan,
    LoanApprove,
    LoanCreate,
    LoanReject,
    LoanResponse,
    LoanSimulate,
    LoanSimulateResponse,
)
from app.schemas.payment_schedule import PaymentSchedule, PaymentScheduleCreate, PaymentScheduleResponse
from app.schemas.vehicle import Vehicle, VehicleCreate, VehicleResponse
from app.schemas.vehicle_category import (
    VehicleCategory,
    VehicleCategoryCreate,
    VehicleCategoryResponse,
)

__all__ = [
    "VehicleCategory",
    "VehicleCategoryCreate",
    "VehicleCategoryResponse",
    "Vehicle",
    "VehicleCreate",
    "VehicleResponse",
    "Loan",
    "LoanCreate",
    "LoanResponse",
    "LoanSimulate",
    "LoanSimulateResponse",
    "LoanApprove",
    "LoanReject",
    "PaymentSchedule",
    "PaymentScheduleCreate",
    "PaymentScheduleResponse",
]


