#!/bin/bash
# start-docker.sh
# Script to start the KIOSK application with Docker

set -e

echo "🚀 Starting KIOSK Application with Docker"
echo "=========================================="

# Parse command line arguments
ENABLE_FRONTEND=false
ENABLE_KIOSK=false
ENABLE_ADMIN=false
ENABLE_SUPERADMIN=false
ENABLE_TOOLS=false
CLEAN_START=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --frontend)
      ENABLE_FRONTEND=true
      ENABLE_KIOSK=true
      ENABLE_ADMIN=true
      ENABLE_SUPERADMIN=true
      shift
      ;;
    --kiosk)
      ENABLE_KIOSK=true
      shift
      ;;
    --admin)
      ENABLE_ADMIN=true
      shift
      ;;
    --superadmin)
      ENABLE_SUPERADMIN=true
      shift
      ;;
    --tools)
      ENABLE_TOOLS=true
      shift
      ;;
    --clean)
      CLEAN_START=true
      shift
      ;;
    --help)
      echo "Usage: $0 [OPTIONS]"
      echo "Options:"
      echo "  --kiosk       Enable kiosk frontend"
      echo "  --admin       Enable admin frontend"
      echo "  --superadmin  Enable superadmin frontend"
      echo "  --frontend    Enable all frontend services (kiosk, admin, superadmin)"
      echo "  --tools       Enable pgAdmin tools"
      echo "  --clean       Clean start (remove all data)"
      echo "  --help        Show this help message"
      exit 0
      ;;
    *)
      echo "Unknown option $1"
      echo "Use --help for usage information"
      exit 1
      ;;
  esac
done

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null && ! command -v docker &> /dev/null; then
    echo "❌ docker-compose is not installed. Please install Docker Compose and try again."
    exit 1
fi

# Use docker compose (new) or docker-compose (legacy)
DOCKER_COMPOSE_CMD="docker-compose"
if docker compose version > /dev/null 2>&1; then
    DOCKER_COMPOSE_CMD="docker compose"
fi

# Clean start if requested
if [ "$CLEAN_START" = true ]; then
    echo "🧹 Performing clean start..."
    $DOCKER_COMPOSE_CMD down -v --remove-orphans || true
    docker system prune -f || true
    sudo rm -rf data/uploads/* data/logs/* data/postgres/* 2>/dev/null || true
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p data/uploads
mkdir -p data/logs
mkdir -p data/postgres

# Fix permissions for frontend node_modules if they exist
if [ -d "frontend/node_modules" ]; then
    echo "🔧 Fixing frontend permissions..."
    sudo rm -rf frontend/node_modules 2>/dev/null || true
    sudo rm -f frontend/package-lock.json 2>/dev/null || true
fi

# Stop any existing containers
echo "🛑 Stopping any existing containers..."
$DOCKER_COMPOSE_CMD down --remove-orphans || true

# Build compose command with profiles
COMPOSE_PROFILES=""
if [ "$ENABLE_KIOSK" = true ]; then
    COMPOSE_PROFILES="$COMPOSE_PROFILES --profile kiosk"
fi
if [ "$ENABLE_ADMIN" = true ]; then
    COMPOSE_PROFILES="$COMPOSE_PROFILES --profile admin"
fi
if [ "$ENABLE_SUPERADMIN" = true ]; then
    COMPOSE_PROFILES="$COMPOSE_PROFILES --profile superadmin"
fi
if [ "$ENABLE_TOOLS" = true ]; then
    COMPOSE_PROFILES="$COMPOSE_PROFILES --profile tools"
fi

# Build and start services
echo "🔨 Building and starting services..."
echo "   Profiles: $([ -n "$COMPOSE_PROFILES" ] && echo "$COMPOSE_PROFILES" || echo "backend-only")"
$DOCKER_COMPOSE_CMD $COMPOSE_PROFILES up --build -d

# Wait for services to be healthy
echo "⏳ Waiting for services to be ready..."
sleep 20

# Check service status
echo "🔍 Checking service status..."
$DOCKER_COMPOSE_CMD ps

# Test if backend is responding (with retries)
echo "🧪 Testing backend health..."
RETRIES=5
for i in $(seq 1 $RETRIES); do
    if curl -f http://localhost:8001/health > /dev/null 2>&1; then
        echo "✅ Backend is healthy and responding"
        break
    else
        if [ $i -eq $RETRIES ]; then
            echo "❌ Backend is not responding after $RETRIES attempts."
            echo "   Check logs with: $DOCKER_COMPOSE_CMD logs backend"
            exit 1
        fi
        echo "   Attempt $i/$RETRIES failed, retrying in 5 seconds..."
        sleep 5
    fi
done

# Test database connection
echo "🗄️  Testing database connection..."
if $DOCKER_COMPOSE_CMD exec -T postgres pg_isready -U kiosk_user -d kiosk_db > /dev/null 2>&1; then
    echo "✅ Database is ready"
else
    echo "❌ Database is not ready. Check logs with: $DOCKER_COMPOSE_CMD logs postgres"
fi

# Test Redis connection
echo "📦 Testing Redis connection..."
if $DOCKER_COMPOSE_CMD exec -T redis redis-cli ping > /dev/null 2>&1; then
    echo "✅ Redis is ready"
else
    echo "❌ Redis is not ready. Check logs with: $DOCKER_COMPOSE_CMD logs redis"
fi

echo ""
echo "🎉 KIOSK Application is running successfully!"
echo ""
echo "📍 Access Points:"
echo "   • Backend API: http://localhost:8001"
echo "   • API Documentation: http://localhost:8001/docs"
if [ "$ENABLE_KIOSK" = true ]; then
    echo "   • Kiosk Frontend: http://localhost:8080"
fi
if [ "$ENABLE_ADMIN" = true ]; then
    echo "   • Admin Frontend: http://localhost:8081"
fi
if [ "$ENABLE_SUPERADMIN" = true ]; then
    echo "   • Superadmin Frontend: http://localhost:8082"
fi
if [ "$ENABLE_TOOLS" = true ]; then
    echo "   • pgAdmin: http://localhost:5050 (admin@kiosk.local / admin123)"
fi
echo ""
echo "🔧 Database Connection:"
echo "   • Host: localhost"
echo "   • Port: 5433"
echo "   • Database: kiosk_db"
echo "   • Username: kiosk_user"
echo "   • Password: kiosk_secure_password_2024"
echo ""
echo "📋 Useful Commands:"
echo "   • View logs: $DOCKER_COMPOSE_CMD logs -f"
echo "   • Stop services: $DOCKER_COMPOSE_CMD down"
echo "   • Restart services: $DOCKER_COMPOSE_CMD restart"
echo "   • Clean restart: ./start-docker.sh --clean"
echo "   • With kiosk frontend only: ./start-docker.sh --kiosk"
echo "   • With admin frontend only: ./start-docker.sh --admin"
echo "   • With superadmin frontend only: ./start-docker.sh --superadmin"
echo "   • With all frontends: ./start-docker.sh --frontend"
echo "   • With tools: ./start-docker.sh --tools"
echo ""
echo "🚀 To run the KIOSK application:"
echo "   python main.py"
echo ""
echo "💡 Next steps:"
echo "   1. Run KIOSK app: python main.py"
echo "   2. Open API docs: http://localhost:8001/docs"
echo "   3. Create SuperAdmin via KIOSK application"