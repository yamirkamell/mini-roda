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
COPY apps/mfe-customers/package.json ./apps/mfe-customers/
COPY apps/mfe-customers/tsconfig.json ./apps/mfe-customers/
COPY apps/mfe-customers/tsconfig.node.json ./apps/mfe-customers/
COPY apps/mfe-customers/vite.config.ts ./apps/mfe-customers/
COPY apps/mfe-customers/index.html ./apps/mfe-customers/

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
WORKDIR /app/apps/mfe-customers

# Copy app source code (now that we're in the right directory)
COPY apps/mfe-customers/src ./src

RUN pnpm build

# Production stage
FROM nginx:alpine

# Install curl for health checks
RUN apk add --no-cache curl

# Copy built files
COPY --from=builder /app/apps/mfe-customers/dist /usr/share/nginx/html

# Copy nginx configuration
COPY apps/mfe-customers/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 5173

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl --fail --silent http://localhost:5173/ || exit 1

CMD ["nginx", "-g", "daemon off;"]

