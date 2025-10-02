# KIOSK Application Setup Guide

This project uses a modular monorepo architecture: each service and frontend application lives in its own folder within a single repository.

This comprehensive guide covers everything you need to deploy, configure, and manage the KIOSK application using Docker.

## 🚀 Quick Start

## 🖥️ Local Frontend Development (No Docker)

Each frontend application can be developed and tested independently using pnpm:

Kiosk (http://localhost:3000):
```bash
cd frontend/apps/kiosk
pnpm install
pnpm dev
```
Admin (http://localhost:3001):
```bash
cd frontend/apps/admin
pnpm install
pnpm dev
```
Super-Admin (http://localhost:3002):
```bash
cd frontend/apps/super-admin
pnpm install
pnpm dev
```
### Prerequisites
- Docker and Docker Compose installed
- No services running on ports: 8001, 5433, 6380, 3001, 5050

### One-Command Deployment
```bash
# Run from: KIOSK project root directory
./scripts/start-docker.sh
```

This script will:
- ✅ Check Docker is running  
- ✅ Create necessary directories
- ✅ Stop any existing containers
- ✅ Build and start all services
- ✅ Wait for services to be healthy
- ✅ Test backend and database connectivity

## 🧹 Complete Cleanup & Fresh Installation

### Full System Cleanup
```bash
# Run from: KIOSK project root directory
# Clean up everything - containers, images, data
./scripts/cleanup-docker.sh

# Remove all Docker artifacts
docker system prune -a -f --volumes

# Remove data directories (WARNING: All data will be lost!)
sudo rm -rf data/uploads/* data/logs/* data/postgres/*
```

### Additional Cleanup Commands
```bash
# Run from: KIOSK project root directory
# Remove only KIOSK containers and images
docker-compose down -v --remove-orphans --rmi all

# Clean Docker system cache
docker builder prune -f

# Remove unused networks
docker network prune -f
```

### Database Data Cleanup Options

#### Option 1: Clean Business Data Only (Preserve Users)
```bash
# Run from: KIOSK project root directory (containers must be running)
# Keeps users, roles, sessions - removes business data
./scripts/cleanup-data-from-db.sh
```

This script will:
- ✅ Preserve all users (superadmin, admin, staff)
- ✅ Preserve all roles and permissions
- ✅ Preserve active user sessions
- 🗑️ Delete all orders, payments, customers
- 🗑️ Delete all inventory items and devices
- 🗑️ Delete all categories
- ✅ Reset business data sequences to start from 1

#### Option 2: Complete Database Cleanup (Nuclear Option)
```bash
# Run from: KIOSK project root directory (containers must be running)
# ⚠️ WARNING: This deletes ALL data while preserving roles
./scripts/cleanup-complete-data-from-db.sh
```

This script will:
- ✅ Delete all users (including superadmin)
- ✅ Delete all orders, payments, customers
- ✅ Delete all sessions and inventory
- ✅ Delete all devices and categories
- ✅ Reset all ID sequences to start from 1
- ✅ Preserve roles for system functionality
- ⚠️ Require explicit confirmation ("DELETE ALL")

## 🔧 Deployment Options

### Basic Backend Only (Recommended)
```bash
# Run from: KIOSK project root directory
./scripts/start-docker.sh
```

### With kiosk frontend only
```bash
# Run from: KIOSK project root directory
./scripts/start-docker.sh --kiosk
```

### With admin frontend only
```bash
# Run from: KIOSK project root directory
./scripts/start-docker.sh --admin
```

### With superadmin frontend only
```bash
# Run from: KIOSK project root directory
./scripts/start-docker.sh --superadmin
```

### With all frontends
```bash
# Run from: KIOSK project root directory
./scripts/start-docker.sh --frontend
```

### With Database Management Tools
```bash
# Run from: KIOSK project root directory
./scripts/start-docker.sh --tools
```

### With all frontends and tools
```bash
# Run from: KIOSK project root directory
./scripts/start-docker.sh --frontend --tools
```

### Clean Start (Removes All Data)
```bash
# Run from: KIOSK project root directory
./scripts/start-docker.sh --clean
```

## 🗄️ Database Migration with Alembic

### Interactive Migration Script (Recommended)
```bash
# Run from: KIOSK project root directory
# Make sure containers are running first
./scripts/start-docker.sh

# Run interactive migration script
./scripts/alembic_init_and_migrate.sh
```

This script will:
- ✅ Check for schema changes in `models.py`
- ✅ Look for SQL scripts in `backend/DBchangesscripts/`
- ✅ Show you exactly what will happen
- ✅ Ask for confirmation before proceeding
- ✅ Apply schema migrations (if needed)
- ✅ Execute SQL scripts (if found)

### Managing Database Changes

#### Schema Changes
1. Modify `backend/app/database/models.py`
2. Run `./scripts/alembic_init_and_migrate.sh`
3. Review and confirm changes

#### API Structure
- All API endpoints are in `backend/app/api/`
- No versioning folders - direct files: `auth.py`, `users.py`
- Simple import structure for rapid development

#### Data Changes (Like Adding Roles)
1. Create SQL file in `backend/DBchangesscripts/`
2. Run `./scripts/alembic_init_and_migrate.sh`
3. Script will find and execute your SQL files

#### Current Default Roles
The system includes these roles (populated via `default_roles.sql`):
- `superadmin` - Full system access
- `admin` - Administrative access
- `customer` - Customer/end-user access
- `pos-terminal` - POS terminal device
- `kkt` - KKT device
- `externalDisplay` - External display device
- `externalKitchen` - Kitchen display system
- `externalPostBox` - Post/delivery system
- `externalPaymentGate` - Payment gateway
- `externalEmailService` - Email service integration
- `externalSMSService` - SMS service integration

### Manual Migration Commands (Advanced)
```bash
# Run from: KIOSK project root directory (containers must be running)
# Generate new migration
docker exec kiosk_backend alembic revision --autogenerate -m "Migration description"

# Apply migrations
docker exec kiosk_backend alembic upgrade head

# Check migration status
docker exec kiosk_backend alembic current

# Downgrade to previous migration
docker exec kiosk_backend alembic downgrade -1

# Execute SQL script manually
docker exec -i kiosk_postgres psql -U kiosk_user -d kiosk_db < backend/DBchangesscripts/your_script.sql
```

## 🌐 Service Endpoints & Health Checks

### Available Endpoints

| Service | External URL | Purpose | Status |
|---------|--------------|---------|--------|
| API Docs (Swagger) | http://localhost:8000/docs#/ | Interactive API documentation | ✅ Working |
| Health Check | http://localhost:8000/health | Service health status | ✅ Working |
| Server Info | http://localhost:8000/ | Basic server information | ✅ Working |
| Setup Status | http://localhost:8000/api/v1/setup/status | Check if SuperAdmin setup needed | ✅ Working |
| Setup SuperAdmin | http://localhost:8000/api/v1/setup/superadmin | First-time SuperAdmin creation (race-safe) | ✅ Working |
| Frontend | http://localhost:3001 | React application (if enabled) | ❌ Not Found (OK if not enabled) |
| pgAdmin | http://localhost:5050 | Database management (if enabled) | ❌ Not responding (needs --tools flag) |

**Note**: The `/api/v1` prefix is configured in main.py, while the folder structure is simplified (no v1 folders).

### Health Check Commands
```bash
# Run from: Any terminal (containers must be running)
# Backend health (working port)
curl http://localhost:8000/health
# Expected: {"status": "healthy", "version": "0.1.0"}

# Backend info
curl http://localhost:8000/
# Expected: {"message": "KIOSK Application Backend API", "version": "0.1.0"}

# Run from: KIOSK project root directory
# Database health
docker-compose exec postgres pg_isready -U kiosk_user -d kiosk_db

# Redis health
docker-compose exec redis redis-cli ping
# Expected: PONG

# Check all services status
docker-compose ps

# Check backend container logs
docker-compose logs backend | tail -10
```

## 👥 User Management & Authentication

### Initial Setup - Creating SuperAdmin

First, check if setup is required:
```bash
# Run from: Any terminal (containers must be running)
curl http://localhost:8000/api/v1/setup/status
```

Create SuperAdmin (first-time setup only):
```bash
# Run from: Any terminal (containers must be running)
# Note: This endpoint has race condition protection for safe concurrent access
curl -X POST http://localhost:8000/api/v1/setup/superadmin \
  -H "Content-Type: application/json" \
  -d '{"username": "superadmin", "password": "SuperPassword123", "email": "super@admin.com"}'
```

### SuperAdmin Login
```bash
# Run from: Any terminal (containers must be running)
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "superadmin", "password": "SuperPassword123"}'
```

**Save the `access_token` from the response for creating other users!**

### Creating Admin Users

Using the SuperAdmin token:
```bash
# Run from: Any terminal (containers must be running)
# Using JSON body (role_id field is ignored - admin role assigned automatically)
curl -X POST http://localhost:8000/api/v1/users/create-admin \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_SUPERADMIN_TOKEN_HERE" \
  -d '{"username": "admin_user", "password": "AdminPass123", "email": "admin@test.com"}'
```

### User Roles Setup (SQL Script)

If you need to manually populate the roles table, connect to the database and run:

```bash
# Run from: KIOSK project root directory (containers must be running)
# Connect to database
docker-compose exec postgres psql -U kiosk_user -d kiosk_db
```

Then execute this SQL:
```sql
-- Insert default roles
INSERT INTO roles (role_id, name, permissions, created_at) VALUES 
(1, 'superadmin', '{"all_permissions": true, "can_create_admins": true, "can_manage_system": true}', NOW()),
(2, 'admin', '{"can_create_users": true, "can_manage_inventory": true, "can_view_reports": true, "can_manage_devices": true}', NOW()),
(3, 'customer', '{"can_use_kiosk": true, "can_view_own_transactions": true}', NOW())
ON CONFLICT (role_id) DO NOTHING;
```

### User Authentication Workflow
```bash
# Run from: Any terminal (containers must be running)
# 1. Get current user info
curl -X GET http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"

# 2. Logout
curl -X POST http://localhost:8000/api/v1/auth/logout \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"

# 3. List all users (SuperAdmin only)
curl -X GET http://localhost:8000/api/v1/users/ \
  -H "Authorization: Bearer YOUR_SUPERADMIN_TOKEN_HERE"
```

## 🔍 Service Ports & Database Access

### Port Configuration
| Service | Internal Port | External Port | Working URLs | Purpose |
|---------|---------------|---------------|--------------|---------|
| Backend | 8000 | 8001 | http://localhost:8000 | FastAPI application |
| PostgreSQL | 5432 | 5433 | localhost:5433 | Database |
| Redis | 6379 | 6380 | localhost:6380 | Cache/Sessions |
| Frontend | 3000 | 3001 | http://localhost:3001 | React application |
| pgAdmin | 80 | 5050 | http://localhost:5050 | Database management |

**Note**: Backend responds on port 8000 (not 8001) due to current container configuration.

### Database Access Methods

#### Via Docker
```bash
# Run from: KIOSK project root directory (containers must be running)
docker exec -it kiosk_postgres psql -U kiosk_user -d kiosk_db
```

#### Via External Client
- **Host:** localhost
- **Port:** 5433
- **Database:** kiosk_db
- **Username:** kiosk_user
- **Password:** kiosk_secure_password_2025

#### Via pgAdmin (Web Interface)
```bash
# Run from: KIOSK project root directory
# Start with pgAdmin
docker-compose --profile tools up -d

# Access at: http://localhost:5050
# Email: admin@kiosk.local
# Password: admin123
```

## 🚨 Troubleshooting

### Common Issues & Solutions

#### Backend Not Starting
```bash
# Run from: KIOSK project root directory
# Check logs
docker-compose logs backend

# Common fixes:
docker-compose restart backend  # Restart backend
./scripts/start-docker.sh --clean      # Clean start
```

#### Database Connection Issues
```bash
# Run from: KIOSK project root directory
# Check database status
docker-compose exec postgres pg_isready -U kiosk_user -d kiosk_db

# Reset database
docker-compose down -v
./scripts/start-docker.sh
```

#### Port Conflicts
```bash
# Run from: Any terminal
# Check what's using ports
lsof -i :8001  # Backend
lsof -i :5433  # PostgreSQL
lsof -i :6380  # Redis

# Kill processes if needed
sudo kill -9 PID
```

#### Permission Issues (macOS/Linux)
```bash
# Run from: KIOSK project root directory
# Fix permissions
sudo rm -rf frontend/node_modules 2>/dev/null || true
sudo rm -f frontend/package-lock.json 2>/dev/null || true
./scripts/cleanup-docker.sh
```

### Service Monitoring

#### View Logs
```bash
# Run from: KIOSK project root directory
# All services
docker-compose logs -f

# Specific services
docker-compose logs -f backend
docker-compose logs -f postgres
docker-compose logs -f redis
```

#### Restart Services
```bash
# Run from: KIOSK project root directory
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart backend
docker-compose restart postgres
```

## ✅ Verification Checklist

After deployment, verify these indicators:

1. **All containers healthy:** `docker-compose ps` shows "Up (healthy)"
2. **Health endpoint:** `curl http://localhost:8000/health` returns 200
3. **Database accessible:** Can connect and query tables
4. **Authentication works:** SuperAdmin creation and login successful
5. **API documentation:** http://localhost:8000/docs#/ loads correctly
6. **User creation:** SuperAdmin can create admin users
7. **Migrations applied:** Database schema is up-to-date

### Automated Testing
```bash
# Run from: KIOSK project root directory, then navigate to backend
cd backend
python test_auth_apis.py
```

## 🎯 Expected Final State

Successfully deployed KIOSK application should have:

- ✅ PostgreSQL running on port 5433 with KIOSK database
- ✅ Redis running on port 6380 for caching/sessions
- ✅ FastAPI backend accessible on port 8000 with all endpoints
- ✅ Database tables auto-created with proper schema
- ✅ Default roles (superadmin, admin, customer) in database
- ✅ SuperAdmin user created and authenticated
- ✅ JWT authentication system working
- ✅ All API endpoints responding correctly
- ✅ Optional frontend on port 3001 (if enabled)
- ✅ Optional pgAdmin on port 5050 (if enabled)

## 📋 Maintenance Commands

### Regular Maintenance
```bash
# Run from: KIOSK project root directory
# Update and restart services
./scripts/start-docker.sh --clean

# View system resource usage
docker stats

# Backup database
docker-compose exec postgres pg_dump -U kiosk_user kiosk_db > backup.sql

# Restore database
docker-compose exec -T postgres psql -U kiosk_user -d kiosk_db < backup.sql
```

### Production Considerations
```bash
# Run from: KIOSK project root directory
# Monitor logs continuously
docker-compose logs -f --tail=100

# Check disk usage
docker system df

# Clean up old logs
docker system prune -f --filter "until=24h"
```

This setup provides a complete, isolated, and production-ready KIOSK authentication system using Docker!