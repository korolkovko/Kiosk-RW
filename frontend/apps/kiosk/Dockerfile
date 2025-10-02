# syntax=docker/dockerfile:1
FROM node:18-alpine AS build
WORKDIR /app

# Keep npm updated for better workspace handling
RUN npm i -g npm@latest

# Copy only manifest files first to leverage Docker layer caching
COPY package*.json ./
COPY shared/package.json ./shared/
COPY apps/kiosk/package.json ./apps/kiosk/
COPY apps/admin/package.json ./apps/admin/
COPY apps/super-admin/package.json ./apps/super-admin/

# Install workspace deps (tolerant to peer deps during containerized builds)
RUN npm install --force || npm install --legacy-peer-deps || true

# Copy full workspace
COPY . .

# Build only the kiosk app
RUN npm run build:kiosk

# ---- Runtime ----
FROM nginx:alpine

# SPA nginx config with history fallback
COPY apps/kiosk/nginx.conf /etc/nginx/nginx.conf

# Static assets
COPY --from=build /app/apps/kiosk/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
