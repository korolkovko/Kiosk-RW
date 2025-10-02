#!/bin/bash
# alembic-schema-only.sh
# Create database schema ONLY from models.py using Alembic
# This script focuses solely on schema creation without data population

set -euo pipefail

echo "🏗️  KIOSK Database Schema Creation (Models.py Only)"
echo "================================================="
echo ""
echo "📋 This script will:"
echo "   ✅ Generate database schema from backend/app/database/models.py"
echo "   ✅ Create all tables, indexes, and constraints"
echo "   ✅ Set up foreign key relationships"
echo "   ❌ NOT populate any data (use alembic-sql-scripts.sh for that)"
echo ""

# Check if KIOSK containers are running
echo "🔍 Checking for KIOSK project containers..."
if ! docker ps --format "{{.Names}}" | grep -q "^kiosk_postgres$"; then
    echo "❌ KIOSK PostgreSQL container 'kiosk_postgres' is not running!"
    echo "Please start KIOSK containers first: docker-compose up -d"
    exit 1
fi

if ! docker ps --format "{{.Names}}" | grep -q "^kiosk_backend$"; then
    echo "❌ KIOSK Backend container 'kiosk_backend' is not running!"
    echo "Please start KIOSK containers first: docker-compose up -d" 
    exit 1
fi
echo "✅ KIOSK containers are running"

# Check database connectivity
echo "🔍 Verifying KIOSK database connection..."
if ! docker exec kiosk_postgres pg_isready -U kiosk_user -d kiosk_db >/dev/null 2>&1; then
    echo "❌ Cannot connect to KIOSK database!"
    exit 1
fi
echo "✅ Database connection verified"

# Check current migration status
echo "🔍 Checking current Alembic migration status..."
CURRENT_HEAD=$(docker exec kiosk_backend alembic current 2>&1 || echo "No migrations found")
echo "Current state: $CURRENT_HEAD"

# Check if there are any existing migrations
MIGRATION_COUNT=$(docker exec kiosk_backend find /app/alembic/versions -name "*.py" -type f | wc -l 2>/dev/null || echo "0")
echo "📁 Existing migration files: $MIGRATION_COUNT"

# Fix Alembic state issues
if echo "$CURRENT_HEAD" | grep -q "Can't locate revision\|No migrations found\|database is not up to date"; then
    echo "🔧 Fixing Alembic state issues..."
    
    # Clean up alembic version table
    docker exec kiosk_postgres psql -U kiosk_user -d kiosk_db -c "DROP TABLE IF EXISTS alembic_version;" 2>/dev/null || true
    
    # If we have existing migrations, apply them first
    if [ "$MIGRATION_COUNT" -gt 0 ]; then
        echo "📋 Found existing migrations - applying them first..."
        if docker exec kiosk_backend alembic upgrade head 2>/dev/null; then
            echo "✅ Existing migrations applied"
        else
            echo "⚠️  Could not apply existing migrations - will create fresh migration"
            # Clear migration history to start fresh
            docker exec kiosk_backend rm -f /app/alembic/versions/*.py 2>/dev/null || true
        fi
    fi
    
    # Set alembic to clean state
    docker exec kiosk_backend alembic stamp head 2>/dev/null || true
    echo "✅ Alembic state cleaned"
fi

# Show current database state
echo ""
echo "📊 Current Database State:"
echo "-------------------------"
TABLES=$(docker exec kiosk_postgres psql -U kiosk_user -d kiosk_db -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';" | xargs)
echo "Tables in database: $TABLES"

if [ "$TABLES" -gt 0 ]; then
    echo "📋 Existing tables:"
    docker exec kiosk_postgres psql -U kiosk_user -d kiosk_db -c "SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY tablename;" -t | while read -r table; do
        if [ -n "$table" ]; then
            echo "   - $(echo $table | xargs)"
        fi
    done
fi

echo ""
echo "⚠️  CONFIRMATION REQUIRED"
echo "This will create/update database schema based on models.py"
echo "Type 'CREATE SCHEMA' to proceed, anything else to cancel:"
echo ""
echo -n "Enter confirmation: "
read -r confirmation

if [ "$confirmation" != "CREATE SCHEMA" ]; then
    echo "❌ Schema creation cancelled."
    exit 0
fi

echo ""
echo "🏗️  Creating Database Schema from models.py..."
echo "============================================="

# Generate and apply migration
echo "📝 Generating Alembic migration from models.py..."
MIGRATION_MSG="Schema from models.py - $(date '+%Y%m%d_%H%M%S')"

# Try to generate migration with timeout to prevent hanging
echo "⏱️  Generating migration (with 30s timeout)..."
MIGRATION_OUTPUT=$(timeout 30 docker exec kiosk_backend alembic revision --autogenerate -m "$MIGRATION_MSG" 2>&1 || echo "TIMEOUT_OR_ERROR")
MIGRATION_RESULT=$?

if [ $MIGRATION_RESULT -eq 0 ] && ! echo "$MIGRATION_OUTPUT" | grep -q "TIMEOUT_OR_ERROR"; then
    echo "✅ Migration generated successfully"
    echo "📄 Migration details: $MIGRATION_OUTPUT"
    
    echo "⬆️  Applying migration to database..."
    if timeout 60 docker exec kiosk_backend alembic upgrade head; then
        echo "✅ Schema creation completed successfully!"
    else
        echo "❌ Failed to apply migration"
        exit 1
    fi
elif echo "$MIGRATION_OUTPUT" | grep -q "No changes in schema detected"; then
    echo "ℹ️  No schema changes detected - database is already up to date"
    echo "✅ Schema is current with models.py"
elif echo "$MIGRATION_OUTPUT" | grep -q "TIMEOUT_OR_ERROR"; then
    echo "⏱️  Migration generation timed out - trying cleanup approach..."
    echo ""
    echo "🔧 Clearing migration state and starting fresh..."
    
    # Clear everything and try once more
    docker exec kiosk_postgres psql -U kiosk_user -d kiosk_db -c "DROP TABLE IF EXISTS alembic_version;" 2>/dev/null || true
    docker exec kiosk_backend rm -f /app/alembic/versions/*.py 2>/dev/null || true
    
    echo "🔄 Using alternative approach - direct schema creation..."
    
    # Alternative approach: Use SQLAlchemy to create schema directly
    echo "📝 Creating schema directly from models.py..."
    if docker exec kiosk_backend python -c "
from app.database.models import Base
from app.database.connection import engine
print('Creating all tables from models.py...')
Base.metadata.create_all(bind=engine)
print('✅ Tables created successfully')
"; then
        echo "✅ Schema created directly from SQLAlchemy models"
        
        # Now create an empty migration to track this state
        echo "📝 Creating Alembic migration to track current state..."
        if timeout 30 docker exec kiosk_backend alembic revision -m "Initial schema created directly - $MIGRATION_MSG" >/dev/null 2>&1; then
            echo "✅ Tracking migration created"
            if docker exec kiosk_backend alembic stamp head >/dev/null 2>&1; then
                echo "✅ Alembic state synchronized"
            fi
        else
            echo "⚠️  Could not create tracking migration, but schema is created"
        fi
    else
        echo "❌ Direct schema creation also failed"
        echo "📄 There might be an issue with models.py syntax or database connection"
        exit 1
    fi
else
    echo "❌ Failed to generate migration"
    echo "📄 Error details: $MIGRATION_OUTPUT"
    exit 1
fi

# Verify schema creation
echo ""
echo "🔍 Verifying Schema Creation..."
echo "==============================="

NEW_TABLES=$(docker exec kiosk_postgres psql -U kiosk_user -d kiosk_db -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';" | xargs)
echo "📊 Total tables created: $NEW_TABLES"

if [ "$NEW_TABLES" -gt 0 ]; then
    echo "📋 Created tables:"
    docker exec kiosk_postgres psql -U kiosk_user -d kiosk_db -c "SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY tablename;" -t | while read -r table; do
        if [ -n "$table" ]; then
            echo "   ✅ $(echo $table | xargs)"
        fi
    done
    
    echo ""
    echo "🔗 Foreign key constraints:"
    CONSTRAINTS=$(docker exec kiosk_postgres psql -U kiosk_user -d kiosk_db -t -c "SELECT COUNT(*) FROM information_schema.table_constraints WHERE constraint_type = 'FOREIGN KEY' AND table_schema = 'public';" | xargs)
    echo "   📊 Total foreign keys: $CONSTRAINTS"
    
    echo ""
    echo "📊 Indexes created:"
    INDEXES=$(docker exec kiosk_postgres psql -U kiosk_user -d kiosk_db -t -c "SELECT COUNT(*) FROM pg_indexes WHERE schemaname = 'public';" | xargs)
    echo "   📊 Total indexes: $INDEXES"
fi

echo ""
echo "✅ Database Schema Creation Complete!"
echo "===================================="
echo ""
echo "📋 What was created:"
echo "   🏗️  All tables from models.py"
echo "   🔗 All foreign key relationships"
echo "   📊 All database indexes"
echo "   🎯 All constraints and rules"
echo ""
echo "📋 What was NOT created:"
echo "   ❌ No data was populated"
echo "   ❌ No default roles or categories"
echo "   ❌ No users or system data"
echo ""
echo "💡 Next Steps:"
echo "   1. ✅ Schema is ready for data"
echo "   2. 🔄 Run: ./alembic-sql-scripts.sh to populate default data"
echo "   3. 👤 Create SuperAdmin via API: /api/v1/setup/superadmin"
echo "   4. 🚀 Start using your application!"
echo ""
echo "🎉 Schema creation finished - ready for data population!"