# Customers Service

FastAPI microservice for managing customers with clean architecture, SQLAlchemy, and PostgreSQL.

## Features

- ✅ Clean Architecture (Repository/Service layers)
- ✅ SQLAlchemy ORM with PostgreSQL
- ✅ Alembic for database migrations
- ✅ Pydantic schemas for validation
- ✅ Swagger/OpenAPI documentation
- ✅ Unit tests with pytest
- ✅ Type hints and strict linting

## Project Structure

```
apps/customers-service/
├── app/
│   ├── api/              # API endpoints
│   │   └── v1/
│   │       └── customers.py
│   ├── core/             # Core configuration
│   │   ├── config.py     # Settings
│   │   └── database.py   # Database setup
│   ├── models/           # SQLAlchemy models
│   │   └── customer.py
│   ├── schemas/          # Pydantic schemas
│   │   └── customer.py
│   ├── repositories/     # Data access layer
│   │   └── customer_repository.py
│   ├── services/         # Business logic layer
│   │   └── customer_service.py
│   └── main.py           # FastAPI app
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

3. Create `.env` file from `.env.example`:
```bash
cp .env.example .env
```

4. Update `.env` with your PostgreSQL connection string:
```
DATABASE_URL=postgresql://user:password@localhost:5432/customers_db
```

5. Run database migrations:
```bash
alembic upgrade head
```

## Development

### Run the service

```bash
# Using pnpm (from monorepo root)
pnpm dev

# Or directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
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
- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc
- OpenAPI JSON: http://localhost:8001/openapi.json

## API Endpoints

### POST /api/v1/customers
Create a new customer.

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "phone": "+1234567890"
}
```

### GET /api/v1/customers
Get all customers (with pagination).

**Query Parameters:**
- `skip` (int, default: 0): Number of records to skip
- `limit` (int, default: 100): Maximum number of records

### GET /api/v1/customers/{id}
Get a specific customer by ID.

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
docker build -t customers-service .
docker run -p 8001:8001 -e DATABASE_URL=postgresql://... customers-service
```

The Dockerfile automatically runs migrations on startup.
