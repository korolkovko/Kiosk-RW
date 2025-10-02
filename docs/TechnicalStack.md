# Technical Stack - KIOSK

## Core Platform

- **Python 3.11+** — backend
- **React 18 + TypeScript 5.0+** — frontend SPA with strict typing
- **Linux** (any distribution) — we'll try Ubuntu
- **Docker + docker-compose** — the only dependency for installation

## Backend Stack

### Web Framework & Server
- **FastAPI 0.104+** — typed API framework
- **Uvicorn** — ASGI server
- **Pydantic (v2)** — data validation and schemas

### Database & Storage
- **PostgreSQL 15+** — main DB (via Docker)
- **asyncpg** — async driver for PostgreSQL
- **SQLAlchemy 2.0** — async ORM
- **Alembic** — DB migrations
- **Redis** — cache, sessions, queues (via Docker)

### Task Processing
- **FastAPI BackgroundTasks** — simple tasks
- **APScheduler** — periodic tasks (backups, archiving)
- **Celery + Redis** — complex tasks (integrations, bulk processing)

### Authentication & Security
- **python-jose** — JWT tokens
- **passlib + bcrypt** — password hashing
- **python-multipart** — file uploads

## Frontend Stack

### Core Libraries
- **React 18** — UI library
- **TypeScript 5.0+** — static typing
- **Vite** — fast build and dev server with TS support
- **TailwindCSS** — utility-first styles

### Type Safety & Code Quality
- **TypeScript** — strict typing for reliability
- **Storybook** — for debugging

### State & Data (typed)
- **Zustand** — typed global state
- **React Query/TanStack Query** — typed server state
- **React Hook Form** — typed form handling
- **Zod** — runtime validation and TypeScript schemas

### Real-time & Interactions
- **WebSocket (native)** — real-time updates from backend
- **Framer Motion** — smooth animations for kiosk

## DevOps & Infrastructure

### Deployment
- **Docker** — the only dependency for target system
- **docker-compose** — orchestration of all services
- **Built-in web server** — FastAPI serves static files directly

### Database Services (via Docker)
```yaml
services:
  postgres:
    image: postgres:15-alpine
  redis:
    image: redis:7-alpine
  kiosk-app:
    depends_on: [postgres, redis]
```

### Automation
- **Bash scripts** — install.sh, start.sh, stop.sh, update.sh, backup.sh
- **Auto-migrations** — on application startup
- **Auto-backups** — via APScheduler + pg_dump

### Monitoring & Logging (built-in)
- **loguru** — file logs with rotation
- **FastAPI built-in metrics** — simple metrics via /health
- **PostgreSQL statistics** — DB performance monitoring

## Testing Stack

### Backend Testing
- **pytest** — main testing framework
- **pytest-asyncio** — async code tests
- **httpx** — HTTP client for API tests
- **fakeredis** — Redis mocks for tests
- **factory-boy** — test data generation

### Frontend Testing
- **Vitest** — fast unit tests with TypeScript support
- **Testing Library** — typed React component testing
- **MSW** — typed API mocks
- **@testing-library/jest-dom** — additional matchers
- **Playwright** — E2E tests with TypeScript (optional)

## Development Tools

### Python Code Quality
- Nothing used yet

### TypeScript Code Quality
- Nothing used yet

### Documentation
- **Swagger UI** — API auto-documentation (built into FastAPI)
- **Storybook** — React component documentation and development
- **Markdown** — project documentation
- **Mermaid** — diagrams in markdown
- Or just Codex or Claude - we'll see

## Deployment & Configuration (maximally simplified)

### One-Command Installation

### User Project Structure
```
kiosk-app/
├── docker-compose.yml    # Main configuration
├── .env                  # Settings (auto-generated)
├── data/                 # All data here
│   ├── postgres/         # PostgreSQL database
│   ├── redis/           # Redis data
│   ├── logs/            # Application logs
│   ├── backups/         # Auto-backups
│   └── uploads/         # Uploaded files (menu, images)
├── scripts/
│   ├── start.sh         # Start all services
│   ├── stop.sh          # Stop
│   ├── update.sh        # Update to new version
│   ├── backup.sh        # Manual DB backup
│   ├── restore.sh       # Restore from backup
│   └── logs.sh          # View logs
└── README.md            # User instructions
```

### Auto-configuration
- **First launch** — DB creation, admin user, sample menu
- **Auto-migrations** — DB schema updates on upgrades
- **Passwords** — auto-generation of secure DB passwords
- **Certificates** — self-signed SSL certificates

### User Commands
```bash
# Installation
curl -sSL install.kiosk.com | bash

# Management
cd kiosk-app
./scripts/start.sh              # Start kiosk
./scripts/stop.sh               # Stop
./scripts/update.sh             # Update to new version
./scripts/backup.sh             # Make backup
./scripts/restore.sh backup.sql # Restore from backup
./scripts/logs.sh               # View logs

# Open in browser
xdg-open http://localhost       # Kiosk
xdg-open http://localhost/admin # Admin panel
```

## Package Management

### Development
- **Poetry** — Python dependency management + virtual environment
- **npm/yarn** — TypeScript/JavaScript dependency management
- **pre-commit** — automatic checks on commits
- **TypeScript compiler (tsc)** — type checking

### Production
- **Docker images** — all dependencies inside containers
- No installations on target machine except Docker

## Performance & Security (automatic)

### Performance
- **PostgreSQL optimizations** — connection pooling, indexes
- **Redis caching** — sessions, frequent queries
- **Static files** — optimized serving via FastAPI
- **Database partitioning** — automatic splitting of large tables

### Security
- **JWT tokens** — auto-generation of secret on installation
- **Bcrypt passwords** — secure hashing
- **HTTPS support** — self-signed certificates
- **Input validation** — Pydantic automatically validates all inputs
- **SQL injection protection** — SQLAlchemy ORM
- **CORS settings** — proper configuration for security

## Data Management (5-year storage)

### Database Architecture
- **PostgreSQL partitioning** — automatic monthly partitioning
- **Incremental backups** — daily incremental backups
- **Point-in-time recovery** — restore to any date
- **Archive management** — automatic archiving of old data

### Retention Policies
```yaml
# Configurable retention policies
retention_policies:
  active_orders: 90_days      # Active orders in main DB
  completed_orders: 5_years   # Completed orders (archives)
  payment_logs: 5_years       # Payment logs
  application_logs: 1_year    # Technical logs
  user_sessions: 7_days       # User sessions
```

## Monitoring (built into application)

### Simple Monitoring Commands
```bash
./scripts/status.sh   # Status of all services
./scripts/logs.sh tail # Latest logs
./scripts/metrics.sh  # Order and performance metrics
./scripts/health.sh   # System health check
```

### Web Monitoring Interface
- **http://localhost/admin/status** — system and service status
- **http://localhost/admin/logs** — real-time log viewing
- **http://localhost/admin/metrics** — order and performance graphs
- **http://localhost/admin/database** — DB and archive status

### Automatic Alerts
- **Payment errors** — notifications to admin panel + logs
- **Integration problems** — automatic retry + alerts
- **Storage shortage** — warnings and auto-cleanup
- **DB problems** — connection and lock monitoring

## External Integrations

### Payment & Fiscal
- **httpx** — async HTTP client for external APIs
- **aiofiles** — async file operations
- **xmltodict** — parsing XML responses from legacy systems

### Real-time Features
- **WebSockets (FastAPI)** — push notifications to clients
- **Server-Sent Events** — WebSocket alternative for simple cases

## Hardware Specific Optimizations

### iPad Frontend
- **PWA (Service Worker)** — offline operation during network failures
- **Touch gestures** — optimization for touch control
- **Responsive design** — adaptation to various screen sizes
- **Performance optimization** — lazy loading, code splitting

### Mini PC Backend
- **Resource limits** — Docker memory/CPU limits for stability
- **systemd services** — auto-start after reboot
- **Log rotation** — automatic cleanup of old logs
- **Database optimization** — PostgreSQL settings for limited resources

## Development Workflow

### Local Development
```bash
# Full development stack
git clone repo
cd kiosk-app
cp .env.example .env.local

# Backend
poetry install
poetry run uvicorn main:app --reload

# Frontend (TypeScript)
npm install
npm run type-check  # Type checking
npm run dev         # Dev server with hot reload

# Or full stack via Docker
docker-compose -f docker-compose.dev.yml up
```

### Production Deployment
```bash
# User just downloads and runs
curl -sSL install.kiosk.com | bash

# Or manual installation
wget kiosk-app.tar.gz
tar -xzf kiosk-app.tar.gz
cd kiosk-app
./scripts/start.sh
```

## Backup & Recovery Strategy

### Automated Backups
- **Daily PostgreSQL dumps** — full DB backups
- **Weekly full backups** — entire system including configurations
- **Monthly archive backups** — long-term storage
- **Real-time WAL backups** — for point-in-time recovery

### Recovery Procedures
```bash
# Restore from backup
./scripts/restore.sh data/backups/2024-01-15.sql

# Restore to specific date
./scripts/restore-point-in-time.sh "2024-01-15 14:30:00"

# Emergency restore
./scripts/emergency-restore.sh
```

## Scalability & Future Growth

### Current Architecture Supports
- **Single kiosk** — primary use case
- **Multiple kiosks** — one backend for multiple locations
- **Chain deployment** — multiple independent installations

### Easy Upgrade Paths
- **Load balancer** — nginx for multiple instances
- **Database clustering** — PostgreSQL master-slave
- **Microservices** — splitting into separate services
- **Cloud deployment** — migration to cloud

## Resource Estimates

### Minimum System Requirements
- **CPU**: 2 cores, 2 GHz
- **RAM**: 8 GB
- **Storage**: 256 GB
- **Network**: 10 Mbps

### Recommended System
- **CPU**: 4 cores, 2.5 GHz
- **RAM**: 16 GB
- **Storage**: 512 GB
- **Network**: 50 Mbps + backup channel