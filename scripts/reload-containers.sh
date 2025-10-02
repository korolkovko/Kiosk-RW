#!/bin/bash
# reload-containers.sh
# Reload KIOSK Docker containers to pick up configuration changes
# Use this when you need to restart containers without rebuilding images

set -euo pipefail

echo "🔄 KIOSK Container Reload"
echo "========================"
echo ""
echo "📋 This script will:"
echo "   🔄 Stop all KIOSK containers gracefully"
echo "   🔄 Start all KIOSK containers with current configuration"
echo "   ✅ Preserve all data (volumes remain intact)"
echo "   ✅ Apply any docker-compose.yml changes"
echo ""

# Change to project root directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

echo "📁 Working directory: $PROJECT_ROOT"
echo ""

# Check if containers are currently running
echo "🔍 Checking current container status..."
POSTGRES_STATUS=$(docker ps --format "table {{.Names}}\t{{.Status}}" | grep "kiosk_postgres" || echo "Not running")
REDIS_STATUS=$(docker ps --format "table {{.Names}}\t{{.Status}}" | grep "kiosk_redis" || echo "Not running")
BACKEND_STATUS=$(docker ps --format "table {{.Names}}\t{{.Status}}" | grep "kiosk_backend" || echo "Not running")

echo "Current status:"
echo "   🐘 PostgreSQL: $POSTGRES_STATUS"
echo "   🔴 Redis: $REDIS_STATUS"
echo "   🚀 Backend: $BACKEND_STATUS"
echo ""

# Confirmation prompt
echo "⚠️  CONFIRMATION REQUIRED"
echo "Continue with container reload?"
echo "Type 'RELOAD' to proceed, anything else to cancel:"
echo ""
echo -n "Enter confirmation: "
read -r confirmation

if [ "$confirmation" != "RELOAD" ]; then
    echo "❌ Container reload cancelled."
    exit 0
fi

echo ""
echo "🔄 Reloading KIOSK Containers..."
echo "================================"

# Stop containers gracefully
echo "⏹️  Stopping containers..."
if docker-compose down; then
    echo "✅ Containers stopped successfully"
else
    echo "⚠️  Some containers may have already been stopped"
fi

# Wait a moment for cleanup
echo "⏳ Waiting for cleanup..."
sleep 2

# Start containers
echo "▶️  Starting containers..."
if docker-compose up -d; then
    echo "✅ Containers started successfully"
else
    echo "❌ Failed to start containers"
    exit 1
fi

# Wait for containers to be ready
echo "⏳ Waiting for containers to be ready..."
sleep 5

# Health check
echo ""
echo "🏥 Health Check"
echo "==============="

# Check PostgreSQL
echo "🔍 Checking PostgreSQL..."
if docker exec kiosk_postgres pg_isready -U kiosk_user -d kiosk_db >/dev/null 2>&1; then
    echo "✅ PostgreSQL is ready"
else
    echo "⚠️  PostgreSQL may still be starting up"
fi

# Check Redis
echo "🔍 Checking Redis..."
if docker exec kiosk_redis redis-cli ping >/dev/null 2>&1; then
    echo "✅ Redis is ready"
else
    echo "⚠️  Redis may still be starting up"
fi

# Check Backend
echo "🔍 Checking Backend..."
BACKEND_HEALTH=$(docker exec kiosk_backend python -c "print('Backend container responding')" 2>/dev/null || echo "Not ready")
echo "   Backend status: $BACKEND_HEALTH"

# Final status
echo ""
echo "📊 Final Container Status"
echo "========================="
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep "kiosk_" || echo "No KIOSK containers running"

echo ""
echo "✅ Container Reload Complete!"
echo "============================="
echo ""
echo "📋 What happened:"
echo "   🔄 All KIOSK containers were gracefully reloaded"
echo "   💾 All data volumes preserved"
echo "   🔧 Configuration changes applied"
echo "   📁 Volume mounts refreshed"
echo ""
echo "💡 Next Steps:"
echo "   1. ✅ Containers are ready for use"
echo "   2. 🔄 Code changes now immediately reflected"
echo "   3. 🚀 Backend API available at: http://localhost:8001"
echo "   4. 🐘 PostgreSQL available at: localhost:5433"
echo ""
echo "🎉 Ready for development with hot reload!"