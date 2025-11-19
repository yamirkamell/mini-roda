# Loans Service

FastAPI microservice for managing loans, vehicles, and payment schedules with clean architecture, SQLAlchemy, and PostgreSQL.

## Features

- ✅ Clean Architecture (Repository/Service layers)
- ✅ SQLAlchemy ORM with PostgreSQL
- ✅ Alembic for database migrations
- ✅ Pydantic schemas for validation
- ✅ Swagger/OpenAPI documentation
- ✅ Unit tests with pytest
- ✅ Vehicle Catalog Management (CRUD)
- ✅ Loan Simulation
- ✅ Loan Approval/Rejection
- ✅ Automatic Payment Schedule Generation
- ✅ Payment Registration

## Project Structure

```
apps/loans-service/
├── app/
│   ├── api/              # API endpoints
│   │   └── v1/
│   │       ├── loans.py
│   │       ├── vehicles.py
│   │       └── vehicle_categories.py
│   ├── core/             # Core configuration
│   │   ├── config.py     # Settings
│   │   └── database.py    # Database setup
│   ├── models/           # SQLAlchemy models
│   │   ├── loan.py
│   │   ├── payment_schedule.py
│   │   ├── vehicle.py
│   │   └── vehicle_category.py
│   ├── schemas/          # Pydantic schemas
│   │   ├── loan.py
│   │   ├── payment_schedule.py
│   │   ├── vehicle.py
│   │   └── vehicle_category.py
│   ├── repositories/     # Data access layer
│   │   ├── loan_repository.py
│   │   ├── payment_schedule_repository.py
│   │   ├── vehicle_repository.py
│   │   └── vehicle_category_repository.py
│   ├── services/         # Business logic layer
│   │   ├── loan_service.py
│   │   ├── vehicle_service.py
│   │   └── vehicle_category_service.py
│   └── main.py          # FastAPI app
├── alembic/              # Database migrations
├── tests/                # Unit tests
├── requirements.txt      # Python dependencies
└── Dockerfile            # Docker configuration
```

## Setup

### Prerequisites

- Python 3.11+
- PostgreSQL 12+
- pnpm (for monorepo scripts)

### Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file:
```bash
DATABASE_URL=postgresql://user:password@localhost:5432/loans_db
```

4. Run database migrations:
```bash
alembic upgrade head
```

## Development

### Run the service

```bash
# Using pnpm (from monorepo root)
pnpm dev

# Or directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8002
```

### Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1
```

### API Documentation

Once the service is running, access:
- Swagger UI: http://localhost:8002/docs
- ReDoc: http://localhost:8002/redoc
- OpenAPI JSON: http://localhost:8002/openapi.json

## API Endpoints

### Vehicle Categories

- `POST /api/v1/vehicle-categories` - Create category
- `GET /api/v1/vehicle-categories` - List all categories
- `GET /api/v1/vehicle-categories/{id}` - Get category by ID
- `PUT /api/v1/vehicle-categories/{id}` - Update category
- `DELETE /api/v1/vehicle-categories/{id}` - Delete category

### Vehicles

- `POST /api/v1/vehicles` - Create vehicle
- `GET /api/v1/vehicles` - List all vehicles (optional `?category_id=X`)
- `GET /api/v1/vehicles/{id}` - Get vehicle by ID
- `PUT /api/v1/vehicles/{id}` - Update vehicle
- `DELETE /api/v1/vehicles/{id}` - Delete vehicle

### Loans

- `POST /api/v1/loans/simulate` - Simulate loan (calculate monthly payment)
- `POST /api/v1/loans` - Create loan
- `GET /api/v1/loans` - List all loans (optional `?customer_id=X`)
- `GET /api/v1/loans/{id}` - Get loan by ID
- `POST /api/v1/loans/{id}/approve` - Approve loan (generates payment schedule)
- `POST /api/v1/loans/{id}/reject` - Reject loan
- `POST /api/v1/loans/{id}/payments` - Register payment
- `GET /api/v1/loans/{id}/payment-schedule` - Get payment schedule

## Loan Simulation Example

```json
POST /api/v1/loans/simulate
{
  "amount": "10000.00",
  "interest_rate": "5.5",
  "term_months": 12
}

Response:
{
  "monthly_payment": "859.68",
  "total_amount": "10316.16"
}
```

## Testing

Run tests:
```bash
pytest tests/ -v
```

Run tests with coverage:
```bash
pytest tests/ -v --cov=app --cov-report=term-missing
```

## Linting

```bash
# Check code style
ruff check .

# Format code
ruff format .

# Type checking
mypy .
```

## Docker

Build and run with Docker:
```bash
docker build -t loans-service .
docker run -p 8002:8002 -e DATABASE_URL=postgresql://... loans-service
```

The Dockerfile automatically runs migrations on startup.
