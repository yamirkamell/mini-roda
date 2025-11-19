# Build stage - Install dependencies
FROM python:3.11-slim AS builder

WORKDIR /app

# Install system dependencies for building
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY apps/loans-service/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --user -r requirements.txt

# Production stage
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y \
    postgresql-client \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY apps/loans-service/ .

# Expose port
EXPOSE 8002

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost:8002/health || exit 1

# Script to wait for PostgreSQL and run migrations
RUN echo '#!/bin/sh\n\
set -e\n\
echo "Waiting for PostgreSQL..."\n\
until pg_isready -h postgres -p 5432 -U user; do\n\
  echo "PostgreSQL is unavailable - sleeping"\n\
  sleep 1\n\
done\n\
echo "PostgreSQL is up - executing migrations"\n\
if ! alembic upgrade head; then\n\
  echo "ERROR: Database migrations failed!"\n\
  echo "Please check the database connection and migration files."\n\
  exit 1\n\
fi\n\
echo "Migrations completed successfully"\n\
echo "Verifying database schema..."\n\
if ! python -c "from app.core.database import engine; from sqlalchemy import inspect; inspector = inspect(engine); tables = inspector.get_table_names(); assert '\''loans'\'' in tables, '\''loans table not found'\''"; then\n\
  echo "ERROR: Database schema verification failed!"\n\
  exit 1\n\
fi\n\
echo "Database schema verified"\n\
echo "Starting application"\n\
exec uvicorn app.main:app --host 0.0.0.0 --port 8002\n\
' > /app/start.sh && chmod +x /app/start.sh

# Run database migrations and start application
CMD ["/app/start.sh"]
