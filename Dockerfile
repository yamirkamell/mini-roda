#############################################
# Mini-Roda Monolito para Railway
#############################################

############################
# Etapa 1: Build Frontend
############################
FROM node:20-bullseye AS frontend-builder

WORKDIR /repo

# Copiamos archivos de configuración del workspace
COPY package.json pnpm-workspace.yaml turbo.json tsconfig.json ./
COPY apps ./apps
COPY packages ./packages

RUN corepack enable

# Instalamos dependencias (el repo no incluye pnpm-lock.yaml)
RUN pnpm install --no-frozen-lockfile

# Variable para apuntar las apps frontend al mismo dominio
ARG VITE_API_BASE_URL=/
ENV VITE_API_BASE_URL=${VITE_API_BASE_URL}

# Construimos librerías compartidas primero
RUN pnpm --filter @mini-roda/ui build

# Construimos shell y microfrontends
RUN pnpm --filter shell build \
  && pnpm --filter mfe-customers build \
  && pnpm --filter mfe-loans build

# Guardamos los artefactos compilados en un directorio común
RUN mkdir -p /build/frontend \
  && cp -r apps/shell/dist /build/frontend/shell \
  && cp -r apps/mfe-customers/dist /build/frontend/mfe-customers \
  && cp -r apps/mfe-loans/dist /build/frontend/mfe-loans

############################
# Etapa 2: Runtime (Python)
############################
FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=3000 \
    CUSTOMERS_PORT=8001 \
    LOANS_PORT=8002 \
    CUSTOMERS_DATABASE_URL="postgresql+psycopg://user:password@localhost:5432/customers_db" \
    LOANS_DATABASE_URL="postgresql+psycopg://user:password@localhost:5432/loans_db"

WORKDIR /app

# Dependencias del sistema necesarias para psycopg2, nginx y supervisord
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    nginx \
    supervisor \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Instalamos dependencias de ambos servicios backend
COPY apps/customers-service/requirements.txt /tmp/requirements-customers.txt
COPY apps/loans-service/requirements.txt /tmp/requirements-loans.txt

RUN pip install --no-cache-dir -r /tmp/requirements-customers.txt \
    && pip install --no-cache-dir -r /tmp/requirements-loans.txt \
    && pip install --no-cache-dir uvicorn gunicorn

# Copiamos el código backend
COPY apps/customers-service ./apps/customers-service
COPY apps/loans-service ./apps/loans-service

# Copiamos los artefactos frontend construidos
COPY --from=frontend-builder /build/frontend ./frontend

# Configuración de nginx y supervisor
RUN rm -f /etc/nginx/sites-enabled/default
COPY infra/nginx/monolith.conf /etc/nginx/sites-enabled/monolith.conf
COPY infra/supervisor/monolith.conf /etc/supervisor/conf.d/monolith.conf

# Exponemos solo el puerto público que Railway necesita
EXPOSE 3000

# Supervisord arranca nginx + uvicorns en el mismo contenedor
CMD ["supervisord", "-n"]

