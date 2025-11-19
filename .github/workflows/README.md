# GitHub Actions Workflows

Este directorio contiene los workflows de CI/CD para el proyecto Mini-Roda.

## Workflows Disponibles

### 1. `ci.yml` - Continuous Integration

**Trigger:** Push y Pull Requests a `main` y `develop`

**Jobs:**
- `lint-and-format`: Lint y verificación de formato para JavaScript/TypeScript
- `python-lint`: Lint para servicios Python (customers-service, loans-service)
- `test`: Ejecuta tests unitarios con base de datos PostgreSQL en contenedor
- `build`: Construye todas las aplicaciones (UI package y microfrontends)
- `docker-build`: Construye imágenes Docker para verificar que los Dockerfiles funcionan

**Características:**
- ✅ Tests automatizados con PostgreSQL en contenedor
- ✅ Verificación de builds
- ✅ Cache de dependencias
- ✅ Multi-stage Docker builds

### 2. `cd.yml` - Continuous Deployment

**Trigger:** Push a `main` (puede activarse manualmente con `workflow_dispatch`)

**Jobs:**
- `lint-and-test`: Lint completo y ejecución de tests
- `build-and-push`: Construye y publica imágenes Docker a GitHub Container Registry
- `deploy`: Despliega a Kubernetes (si está configurado)

**Características:**
- ✅ Build y push de imágenes a ghcr.io
- ✅ Multi-arch builds (amd64, arm64)
- ✅ Cache de Docker layers
- ✅ Despliegue automático a Kubernetes
- ✅ Verificación de despliegue

### 3. `test.yml` - Test Suite

**Trigger:** Push y Pull Requests a `main` y `develop`

**Jobs:**
- `test-js`: Tests de JavaScript/TypeScript
- `test-python`: Tests de servicios Python con matriz de servicios

**Características:**
- ✅ Tests paralelos por servicio
- ✅ Base de datos PostgreSQL en contenedor para tests

### 4. `cloud-deploy.yml` - Cloud Deployment

**Trigger:** Manual (`workflow_dispatch`)

**Características:**
- ✅ Despliegue a entornos staging/production
- ✅ Verificación de conexión a bases de datos cloud
- ✅ Build y push de imágenes
- ✅ Uso de secrets para configuración cloud

## Configuración Requerida

### Secrets de GitHub

Configura los siguientes secrets en tu repositorio (Settings → Secrets and variables → Actions):

#### Para CI/CD Básico:
- No se requieren secrets (usa PostgreSQL en contenedor para tests)

#### Para Deployment a Kubernetes:
1. **KUBECONFIG** (requerido para deploy)
   - Contenido del archivo `~/.kube/config` codificado en base64
   - Para obtenerlo: `cat ~/.kube/config | base64 -w 0` (Linux/Mac)

#### Para Uso de Servicios Cloud:
1. **DATABASE_URL_CUSTOMERS**
   - Connection string para base de datos de clientes en la nube
   - Ejemplo: `postgresql://user:password@ep-xxx-xxx.us-east-1.aws.neon.tech/customers_db?sslmode=require`

2. **DATABASE_URL_LOANS**
   - Connection string para base de datos de préstamos en la nube
   - Ejemplo: `postgresql://user:password@ep-xxx-xxx.us-east-1.aws.neon.tech/loans_db?sslmode=require`

### Permisos del Repositorio

Asegúrate de que el repositorio tenga permisos para:
- ✅ Escribir en GitHub Container Registry (automático con `GITHUB_TOKEN`)
- ✅ Leer y escribir en el repositorio
- ✅ Ejecutar workflows

### Configuración de Kubernetes (Opcional)

El workflow de CD espera (si se configura):
- Un cluster de Kubernetes configurado y accesible
- El namespace `roda` creado
- Traefik Ingress Controller instalado
- Secrets de base de datos configurados en el cluster

## Imágenes Docker

Las imágenes se publican en GitHub Container Registry con el formato:
```
ghcr.io/<OWNER>/mini-roda/<service-name>:<tag>
```

**Tags disponibles:**
- `latest` - Última versión en main
- `main-<sha>` - Versión específica por commit SHA
- `<branch-name>` - Versión por rama

**Servicios:**
- `customers-service`
- `loans-service`
- `mfe-customers`
- `mfe-loans`

## Caching

El workflow utiliza caching para:
- **pnpm**: Cache de dependencias de Node.js basado en `pnpm-lock.yaml`
- **pip**: Cache de dependencias de Python basado en `requirements.txt`
- **Docker**: Cache de layers usando GitHub Actions cache (gha)

## Uso de Servicios Cloud

### Desarrollo Local con Cloud DB

```bash
# 1. Configurar variables de entorno
export DATABASE_URL_CUSTOMERS="postgresql://user:password@cloud-host:5432/customers_db?sslmode=require"
export DATABASE_URL_LOANS="postgresql://user:password@cloud-host:5432/loans_db?sslmode=require"

# 2. Usar docker-compose.cloud.yml
docker compose -f docker-compose.yml -f docker-compose.cloud.yml up -d
```

### CI/CD con Cloud DB

Los workflows de CI/CD pueden usar bases de datos cloud configurando los secrets:
- `DATABASE_URL_CUSTOMERS`
- `DATABASE_URL_LOANS`

Estos se usan automáticamente en los tests y despliegues.

## Despliegue

El despliegue se ejecuta automáticamente cuando:
- ✅ Se hace push a la rama `main`
- ✅ Todos los tests pasan
- ✅ Las imágenes se construyen exitosamente

El workflow:
1. Actualiza las tags de imágenes en los manifiestos de Kubernetes usando Kustomize
2. Aplica los manifiestos al cluster
3. Verifica el estado del despliegue
4. Muestra el estado de pods, services e ingress

## Troubleshooting

### Las imágenes no se construyen
- Verifica que los Dockerfiles estén correctos
- Revisa los logs del job `build-and-push`
- Verifica que el contexto de Docker sea correcto

### El despliegue falla
- Verifica que `KUBECONFIG` esté correctamente configurado
- Asegúrate de que el cluster sea accesible desde GitHub Actions
- Revisa los logs del job `deploy`
- Verifica que los secrets de base de datos estén configurados

### Tests fallan
- Ejecuta los tests localmente primero
- Verifica que todas las dependencias estén en `requirements.txt` o `package.json`
- Verifica que la base de datos en contenedor esté funcionando

### Conexión a base de datos cloud falla
- Verifica que los secrets estén correctamente configurados
- Verifica que la connection string incluya `?sslmode=require`
- Verifica que el servicio cloud esté activo y accesible
- Revisa los logs del servicio para errores de conexión

## Mejoras Futuras

- [ ] Tests de integración end-to-end
- [ ] Tests de carga y performance
- [ ] Notificaciones de despliegue (Slack, email)
- [ ] Rollback automático en caso de fallo
- [ ] Blue-green deployments
- [ ] Canary deployments
- [ ] Métricas de despliegue
