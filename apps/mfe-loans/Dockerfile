# Build stage
FROM node:20-alpine AS builder

WORKDIR /app

# Install pnpm
RUN npm install -g pnpm

# Copy root workspace files
COPY pnpm-workspace.yaml ./
COPY package.json ./
COPY pnpm-lock.yaml* ./

# Copy packages (needed for workspace dependencies)
COPY packages/ ./packages/

# Copy app package files
COPY apps/mfe-loans/package.json ./apps/mfe-loans/
COPY apps/mfe-loans/tsconfig.json ./apps/mfe-loans/
COPY apps/mfe-loans/tsconfig.node.json ./apps/mfe-loans/
COPY apps/mfe-loans/vite.config.ts ./apps/mfe-loans/
COPY apps/mfe-loans/index.html ./apps/mfe-loans/

# Install dependencies
WORKDIR /app
RUN if [ -f pnpm-lock.yaml ]; then \
      pnpm install --frozen-lockfile; \
    else \
      pnpm install; \
    fi

# Build shared packages first (required for MFE build)
WORKDIR /app/packages/ui
RUN pnpm build

# Accept build args for environment variables
ARG VITE_API_BASE_URL=http://localhost
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

# Build application
WORKDIR /app/apps/mfe-loans

# Copy app source code (now that we're in the right directory)
COPY apps/mfe-loans/src ./src

RUN pnpm build

# Production stage
FROM nginx:alpine

# Install curl for health checks
RUN apk add --no-cache curl

# Copy built files
COPY --from=builder /app/apps/mfe-loans/dist /usr/share/nginx/html

# Copy nginx configuration
COPY apps/mfe-loans/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 5174

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl --fail --silent http://localhost:5174/ || exit 1

CMD ["nginx", "-g", "daemon off;"]

