# Shell Application (Host)

Aplicación host que integra los microfrontends usando Module Federation.

## Arquitectura

El Shell Application es el punto de entrada principal de la aplicación. Carga y renderiza los componentes de los microfrontends según la ruta.

```
Usuario → Shell (Puerto 3000)
    ↓
Module Federation
    ├── Carga mfe-customers (si ruta es /customers)
    └── Carga mfe-loans (si ruta es /loans)
```

## Características

- ✅ Routing centralizado con React Router
- ✅ Layout común (header, navegación, footer)
- ✅ Carga dinámica de microfrontends vía Module Federation
- ✅ Suspense para loading states
- ✅ Navegación entre secciones

## Desarrollo

```bash
# Desde la raíz del monorepo
pnpm --filter @mini-roda/shell dev

# O desde apps/shell
cd apps/shell
pnpm dev
```

La aplicación estará disponible en http://localhost:3000

**Importante**: Los microfrontends deben estar corriendo:
- `mfe-customers` en http://localhost:5173
- `mfe-loans` en http://localhost:5174

## Estructura

```
apps/shell/
├── src/
│   ├── App.tsx          # Componente principal con routing
│   ├── App.css          # Estilos del shell
│   ├── main.tsx         # Entry point
│   └── index.css        # Estilos globales
├── vite.config.ts       # Configuración Vite + Module Federation
├── Dockerfile           # Dockerfile para producción
└── nginx.conf           # Configuración Nginx para producción
```

## Rutas

- `/` → Redirige a `/customers`
- `/customers` → Carga `CustomerList` de `mfe-customers`
- `/customers/:id` → Carga `CustomerDetail` de `mfe-customers`
- `/loans` → Carga `LoanList` de `mfe-loans`
- `/loans/:id` → Carga `LoanDetail` de `mfe-loans`

## Module Federation

El shell consume los siguientes remotes:

- `mfe_customers/CustomerList`
- `mfe_customers/CustomerDetail`
- `mfe_loans/LoanList`
- `mfe_loans/LoanDetail`

## Build

```bash
pnpm build
```

El build genera:
- `dist/index.html` - HTML principal
- `dist/assets/*` - Assets estáticos
- `dist/remoteEntry.js` - Entry point de Module Federation (si se expone)

## Producción

En producción, el shell se sirve desde Nginx en el puerto 3000. Traefik enruta todas las peticiones (excepto APIs y docs) al shell.

Los microfrontends se sirven desde sus propios contenedores y el shell los carga dinámicamente vía Module Federation.

## Variables de Entorno

No requiere variables de entorno específicas. Las URLs de los microfrontends se configuran en `vite.config.ts`.

