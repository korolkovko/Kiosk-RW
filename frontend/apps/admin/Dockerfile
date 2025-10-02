# syntax=docker/dockerfile:1
FROM node:18-alpine AS build
WORKDIR /app

RUN npm i -g npm@latest

COPY package*.json ./
COPY shared/package.json ./shared/
COPY apps/kiosk/package.json ./apps/kiosk/
COPY apps/admin/package.json ./apps/admin/
COPY apps/super-admin/package.json ./apps/super-admin/

RUN npm install --force || npm install --legacy-peer-deps || true

COPY . .

# Build only the admin app
RUN npm run build:admin

FROM nginx:alpine
COPY apps/admin/nginx.conf /etc/nginx/nginx.conf
COPY --from=build /app/apps/admin/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
