# Gateway (Traefik)

Traefik reverse proxy configuration for routing requests to backend services.

## Configuration

### Files

- `traefik-simple.yml` - Main Traefik static configuration (used in dev)
- `traefik.yml` - Full Traefik configuration with ACME (for production)
- `dynamic.yml` - Dynamic routing rules and middleware
- `docker-compose.dev.yml` - Docker Compose setup for development

## Routes

- `/customers` → `customers-service:8001` (rewrites to `/api/v1/customers`)
- `/loans` → `loans-service:8002` (rewrites to `/api/v1/loans`)

## Development

### Start with Docker Compose

```bash
# From gateway directory
cd apps/gateway
docker-compose -f docker-compose.dev.yml up

# Or using pnpm (from project root)
pnpm dev
```

### Access Points

- **Traefik Dashboard**: http://localhost:8080
- **Customers Service**: http://localhost/customers
- **Loans Service**: http://localhost/loans
- **Customers API Docs**: http://localhost/customers/docs
- **Loans API Docs**: http://localhost/loans/docs

### Services Included

- Traefik (port 80, 443, 8080)
- Customers Service (internal port 8001)
- Loans Service (internal port 8002)
- PostgreSQL (port 5432) with multiple databases

## Features

- ✅ Automatic service discovery via Docker labels
- ✅ Path rewriting middleware (maps `/customers` → `/api/v1/customers`)
- ✅ Health checks for services
- ✅ Custom headers
- ✅ HTTP and HTTPS support
- ✅ Self-signed certificates for development (HTTPS)

## Routing Details

When a request comes to `/customers/api/v1/customers`, Traefik:
1. Matches the `/customers` prefix
2. Applies the `customers-stripprefix` middleware
3. Rewrites the path from `/customers/...` to `/api/v1/customers/...`
4. Forwards to `customers-service:8001`

Same logic applies for `/loans` → `/api/v1/loans`.

## Production

For production, update `traefik.yml` to use proper certificate resolvers (Let's Encrypt, etc.) and configure proper domain names.
