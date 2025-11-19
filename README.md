# Mini-Roda Monorepo

Monorepo construido con Turborepo y pnpm que agrupa los microfrontends, servicios FastAPI y la infraestructura necesaria para operar el flujo de originación y seguimiento de préstamos.

## Estructura general

```
/apps
  customers-service     -> FastAPI + SQLAlchemy + Alembic
  loans-service         -> FastAPI + SQLAlchemy + Alembic
  gateway               -> Traefik + Docker Compose
  mfe-customers         -> React + Vite + Module Federation
  mfe-loans             -> React + Vite + Module Federation
  shell                 -> React host que federra los MFEs

/packages
  ui                    -> Librería de componentes compartidos
  config                -> Configuración compartida (tsconfig, etc.)

/infra
  docker                -> Artefactos de construcción
  k8s                   -> Manifiestos Kubernetes
```

## Requisitos

- Node.js >= 18
- pnpm >= 8
- Python >= 3.11
- Docker >= 20.10 + Docker Compose >= 2.0

Instalación base:

```bash
pnpm install
```


### Patrones de diseño aplicados

- **Module Federation + Shell**: composición dinámica de microfrontends sin desplegar bundles monolíticos.
- **Clean Architecture / Capas** en FastAPI: routers → servicios → repositorios → modelos.
- **Repository Pattern**: encapsula SQLAlchemy y aísla a los servicios de detalles de persistencia.
- **Factory Script (start.sh)**: ejecuta migraciones y health-checks antes de levantar los servidores Python.
- **State Management** con **Zustand**: stores locales por MFE, con singletons compartidos vía Federation.
- **Edge Routing** con Traefik + labels (pattern “configuration-as-code”).

### Guía de despliegue

#### Desarrollo local (Docker recomendado)

```bash
pnpm docker:up          # levanta todo (traefik, db, servicios, MFEs, shell)
pnpm docker:down        # detiene
pnpm docker:logs        # inspecciona logs
```

Puertos:
- Shell + Traefik host: `http://localhost`
- Traefik dashboard: `http://localhost:8080`
- Swagger clientes: `http://localhost/customers/docs`
- Swagger préstamos: `http://localhost/loans/docs`

#### Desarrollo sin Docker

```bash
pnpm install
pnpm dev                # levanta shell y MFEs

cd apps/customers-service
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --port 8001
```

Repetir para `apps/loans-service` (puerto 8002) y configurar Traefik/hosts manualmente.

#### CI/CD

- Workflow GitHub Actions (no incluido en repo) esperado:
  1. Ejecutar `pnpm install`, `pnpm lint`, `pnpm test`.
  2. Construir imágenes Docker (`docker compose build`).
  3. Publicar en GitHub Container Registry.
  4. Desplegar vía SSH (Droplet) o `railway up` / `render deploy`.

Variables mínimas en el pipeline:

| Servicio | Variable                        | Descripción                                       |
|----------|---------------------------------|---------------------------------------------------|
| Todos    | `ENV`                           | `development`, `staging`, `production`            |
| Backends | `DATABASE_URL`                  | `postgresql+psycopg://user:pass@host/dbname`      |
| MFEs     | `VITE_API_BASE_URL`             | Base para llamadas (`http://localhost` en dev)    |
| Traefik  | `TRAEFIK_DASHBOARD_USER/PASS`   | Basic auth opcional para panel                    |

### 5. Manual de uso, pruebas

1. **Iniciar el sistema** (`pnpm docker:up`).
2. **Shell**: `http://localhost` → navegación entre Clientes y Préstamos. Los botones crean/gestionan entidades vía modales.
3. **Swagger**:
   - Clientes: `http://localhost/customers/docs`
   - Préstamos: `http://localhost/loans/docs`
   - Recomendación: probar `POST /api/v1/customers` y luego `POST /api/v1/loans`.
4. **Pruebas automáticas**:
   ```bash
   cd apps/customers-service && pytest -v
   cd ../loans-service && pytest -v
   ```

## Scripts útiles

| Comando             | Descripción                              |
|---------------------|------------------------------------------|
| `pnpm dev`          | Levanta shell + MFEs en modo Vite        |
| `pnpm build`        | Construye todos los paquetes             |
| `pnpm lint`         | Ejecuta ESLint en MFEs + shell           |
| `pnpm format`       | Formatea con Prettier                    |
| `pnpm clean`        | Limpia artefactos de build               |

## Docker Compose

`docker-compose.yml` define: PostgreSQL, Traefik, ambos servicios FastAPI, MFEs y shell. Cada backend corre migraciones al iniciar y expone `/health` para Traefik.

## Testing rápido

```bash
cd apps/customers-service && pytest -v
cd apps/loans-service && pytest -v
pnpm lint && pnpm format --check
```

## Linting

```bash
pnpm lint        # ESLint
pnpm format      # Prettier
```

---

