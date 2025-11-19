# Kubernetes Manifests

Manifiestos de Kubernetes para desplegar todos los servicios en un cluster.

## Estructura

- `namespace.yaml` - Namespace `roda`
- `configmap.yaml` - Configuración compartida
- `secrets.yaml` - Secretos (base de datos, API keys)
- `customers-service.yaml` - Deployment y Service para customers-service
- `loans-service.yaml` - Deployment y Service para loans-service
- `mfe-customers.yaml` - Deployment y Service para mfe-customers
- `mfe-loans.yaml` - Deployment y Service para mfe-loans
- `traefik-ingressroute.yaml` - IngressRoute de Traefik
- `traefik-middleware.yaml` - Middlewares de Traefik
- `kustomization.yaml` - Configuración de Kustomize

## Requisitos

- Kubernetes cluster (k3d, Minikube, o cualquier cluster)
- Traefik Ingress Controller instalado
- kubectl configurado

## Configuración

### 1. Configurar Secrets

Copia el archivo de ejemplo y edita con tus credenciales reales:

```bash
cp infra/k8s/secrets.example.yaml infra/k8s/secrets.yaml
```

Edita `secrets.yaml` con tus credenciales reales de Neon/Supabase:

**Para Neon:**
```yaml
DATABASE_URL_CUSTOMERS: "postgresql://user:password@ep-xxx-xxx.us-east-1.aws.neon.tech/customers_db?sslmode=require"
DATABASE_URL_LOANS: "postgresql://user:password@ep-xxx-xxx.us-east-1.aws.neon.tech/loans_db?sslmode=require"
```

**Para Supabase:**
```yaml
DATABASE_URL_CUSTOMERS: "postgresql://postgres:password@db.xxx.supabase.co:5432/postgres"
DATABASE_URL_LOANS: "postgresql://postgres:password@db.xxx.supabase.co:5432/postgres"
```

**Nota:** El archivo `secrets.yaml` está en `.gitignore` para evitar commits accidentales.

### 2. Aplicar Manifiestos

```bash
# Aplicar todos los recursos
kubectl apply -k infra/k8s

# O aplicar individualmente
kubectl apply -f infra/k8s/namespace.yaml
kubectl apply -f infra/k8s/configmap.yaml
kubectl apply -f infra/k8s/secrets.yaml
kubectl apply -f infra/k8s/customers-service.yaml
kubectl apply -f infra/k8s/loans-service.yaml
kubectl apply -f infra/k8s/mfe-customers.yaml
kubectl apply -f infra/k8s/mfe-loans.yaml
kubectl apply -f infra/k8s/traefik-middleware.yaml
kubectl apply -f infra/k8s/traefik-ingressroute.yaml
```

## Instalación de Traefik en k3d/Minikube

### k3d

Traefik viene preinstalado en k3d.

### Minikube

```bash
# Instalar Traefik usando Helm
helm repo add traefik https://traefik.github.io/charts
helm repo update
helm install traefik traefik/traefik -n traefik --create-namespace
```

## Skaffold

### Instalación

```bash
# macOS
brew install skaffold

# Linux
curl -Lo skaffold https://storage.googleapis.com/skaffold/releases/latest/skaffold-linux-amd64
sudo install skaffold /usr/local/bin/
```

### Uso

```bash
# Desarrollo con hot-reload
skaffold dev

# Build y deploy
skaffold run

# Deploy sin build
skaffold deploy

# Limpiar recursos
skaffold delete
```

## Verificación

```bash
# Ver pods
kubectl get pods -n roda

# Ver services
kubectl get svc -n roda

# Ver ingress
kubectl get ingressroute -n roda

# Ver logs
kubectl logs -f deployment/customers-service -n roda
kubectl logs -f deployment/loans-service -n roda
```

## Acceso

Una vez desplegado, los servicios estarán disponibles a través del Ingress:

- Customers Service: http://localhost/customers
- Loans Service: http://localhost/loans
- Customers MFE: http://localhost/customers
- Loans MFE: http://localhost/loans

## Troubleshooting

### Pods no inician

```bash
# Ver eventos
kubectl describe pod <pod-name> -n roda

# Ver logs
kubectl logs <pod-name> -n roda
```

### Problemas de conexión a base de datos

Verifica que los secrets estén correctamente configurados:

```bash
kubectl get secret database-secrets -n roda -o yaml
```

### Traefik no enruta

Verifica que Traefik esté instalado:

```bash
kubectl get pods -n traefik
kubectl get ingressroute -n roda
```

