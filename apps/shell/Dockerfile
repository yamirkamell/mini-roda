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
COPY apps/shell/package.json ./apps/shell/
COPY apps/shell/tsconfig.json ./apps/shell/
COPY apps/shell/tsconfig.node.json ./apps/shell/
COPY apps/shell/vite.config.ts ./apps/shell/
COPY apps/shell/index.html ./apps/shell/

# Install dependencies
WORKDIR /app
RUN if [ -f pnpm-lock.yaml ]; then \
      pnpm install --frozen-lockfile; \
    else \
      pnpm install; \
    fi

# Build shared packages first (required for shell build)
WORKDIR /app/packages/ui
RUN pnpm build

# Build application
WORKDIR /app/apps/shell

# Copy app source code
COPY apps/shell/src ./src

RUN pnpm build

# Production stage
FROM nginx:alpine

# Install curl for health checks
RUN apk add --no-cache curl

# Copy built files
COPY --from=builder /app/apps/shell/dist /usr/share/nginx/html

# Copy nginx configuration
COPY apps/shell/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl --fail --silent http://localhost:3000/ || exit 1

CMD ["nginx", "-g", "daemon off;"]

