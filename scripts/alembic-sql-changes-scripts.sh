#!/bin/bash
# alembic-sql-scripts.sh
# Interactive SQL script execution for KIOSK database
# Allows selective execution of SQL scripts with error handling

set -euo pipefail

echo "📜 KIOSK Database SQL Scripts Manager"
echo "===================================="
echo ""
echo "📋 This script will:"
echo "   🔍 Find all SQL scripts in backend/DBchangesscripts/"
echo "   📝 Show you each script's content"
echo "   ❓ Ask if you want to execute each script"
echo "   🛡️  Handle errors gracefully (skip conflicts, continue)"
echo "   📊 Provide execution summary"
echo ""

# Configuration
DB_SCRIPTS_DIR="backend/DBchangesscripts"
EXECUTION_LOG="/tmp/sql_execution.log"
SUCCESS_LOG="/tmp/sql_success.log"
ERROR_LOG="/tmp/sql_errors.log"

# Clear logs
> "$EXECUTION_LOG"
> "$SUCCESS_LOG" 
> "$ERROR_LOG"

# Check if KIOSK containers are running
echo "🔍 Checking for KIOSK project containers..."
if ! docker ps --format "{{.Names}}" | grep -q "^kiosk_postgres$"; then
    echo "❌ KIOSK PostgreSQL container 'kiosk_postgres' is not running!"
    echo "Please start KIOSK containers first: docker-compose up -d"
    exit 1
fi
echo "✅ KIOSK PostgreSQL container is running"

# Check database connectivity and verify KIOSK database
echo "🔍 Verifying KIOSK database connection..."
if ! docker exec kiosk_postgres pg_isready -U kiosk_user -d kiosk_db >/dev/null 2>&1; then
    echo "❌ Cannot connect to KIOSK database!"
    exit 1
fi

# Double-check we're connected to the right database
DB_NAME=$(docker exec kiosk_postgres psql -U kiosk_user -d kiosk_db -t -c "SELECT current_database();" 2>/dev/null | xargs)
if [ "$DB_NAME" != "kiosk_db" ]; then
    echo "❌ Connected to wrong database: $DB_NAME (expected: kiosk_db)"
    echo "❗ Safety check failed - aborting to protect other databases"
    exit 1
fi
echo "✅ Connected to KIOSK database: $DB_NAME"

# Find SQL scripts
echo ""
echo "🔍 Discovering SQL Scripts..."
echo "=============================="

if [ ! -d "$DB_SCRIPTS_DIR" ]; then
    echo "❌ Directory $DB_SCRIPTS_DIR not found!"
    echo "Creating directory for future SQL scripts..."
    mkdir -p "$DB_SCRIPTS_DIR"
    echo "✅ Created $DB_SCRIPTS_DIR"
    echo "📝 Add your SQL scripts to this directory and run this script again."
    exit 0
fi

# Find and sort SQL scripts
SCRIPT_FILES=$(find "$DB_SCRIPTS_DIR" -name "*.sql" -type f | sort)

if [ -z "$SCRIPT_FILES" ]; then
    echo "📂 No SQL scripts found in $DB_SCRIPTS_DIR"
    echo "💡 Add .sql files to this directory and run this script again."
    exit 0
fi

# Display found scripts
SCRIPT_COUNT=$(echo "$SCRIPT_FILES" | wc -l)
echo "📜 Found $SCRIPT_COUNT SQL script(s):"
echo ""

SCRIPT_INDEX=0
for script in $SCRIPT_FILES; do
    SCRIPT_INDEX=$((SCRIPT_INDEX + 1))
    script_name=$(basename "$script")
    echo "[$SCRIPT_INDEX] $script_name"
done

echo ""
echo "🔍 Current Database State:"
echo "-------------------------"

# Show current data summary
DATA_SUMMARY="
SELECT 
    'Data Summary:' as info;
SELECT 
    'roles' as table_name, COUNT(*) as records FROM roles
UNION ALL SELECT 'users', COUNT(*) FROM users
UNION ALL SELECT 'sessions', COUNT(*) FROM sessions
UNION ALL SELECT 'known_customers', COUNT(*) FROM known_customers
UNION ALL SELECT 'orders', COUNT(*) FROM orders
UNION ALL SELECT 'items_live', COUNT(*) FROM items_live
UNION ALL SELECT 'devices', COUNT(*) FROM devices
UNION ALL SELECT 'branches', COUNT(*) FROM branches
UNION ALL SELECT 'food_categories', COUNT(*) FROM food_categories
UNION ALL SELECT 'day_categories', COUNT(*) FROM day_categories
UNION ALL SELECT 'units_of_measure', COUNT(*) FROM units_of_measure
UNION ALL SELECT 'payment_methods', COUNT(*) FROM payment_methods
ORDER BY records DESC, table_name;
"

echo "$DATA_SUMMARY" | docker exec -i kiosk_postgres psql -U kiosk_user -d kiosk_db -t | while read -r line; do
    if [ -n "$line" ]; then
        echo "   📊 $(echo $line | xargs)"
    fi
done

echo ""
echo "⚠️  Ready to Process SQL Scripts"
echo "================================"
echo "You'll be asked about each script individually."
echo "Type 'START PROCESSING' to begin, anything else to cancel:"
echo ""
echo -n "Enter confirmation: "
read -r confirmation

if [ "$confirmation" != "START PROCESSING" ]; then
    echo "❌ SQL script processing cancelled."
    exit 0
fi

# Process each script interactively
echo ""
echo "📜 Processing SQL Scripts Interactively..."
echo "=========================================="

TOTAL_PROCESSED=0
TOTAL_EXECUTED=0
TOTAL_SKIPPED=0
TOTAL_ERRORS=0

for script in $SCRIPT_FILES; do
    TOTAL_PROCESSED=$((TOTAL_PROCESSED + 1))
    script_name=$(basename "$script")
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📄 Script [$TOTAL_PROCESSED/$SCRIPT_COUNT]: $script_name"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # Show script content
    echo "📝 Script Content Preview:"
    echo "  File: $script"
    echo "  Size: $(wc -l < "$script") lines"
    echo ""
    echo "  Content (first 10 lines):"
    head -10 "$script" | sed 's/^/     /'
    
    if [ "$(wc -l < "$script")" -gt 10 ]; then
        echo "     ... ($(( $(wc -l < "$script") - 10 )) more lines)"
    fi
    
    echo ""
    echo "❓ What would you like to do with this script?"
    echo "   [E] Execute this script"
    echo "   [S] Skip this script" 
    echo "   [V] View full script content"
    echo "   [Q] Quit processing (exit)"
    echo ""
    echo -n "Choose [E/S/V/Q]: "
    read -r choice
    
    case "$(echo $choice | tr '[:lower:]' '[:upper:]')" in
        "E")
            echo ""
            echo "⚡ Executing: $script_name"
            echo "$(date): Executing $script_name" >> "$EXECUTION_LOG"
            
            # Execute with error handling
            if docker exec -i kiosk_postgres psql -U kiosk_user -d kiosk_db -v ON_ERROR_STOP=0 < "$script" 2>/dev/null; then
                echo "✅ $script_name executed successfully"
                echo "$(date): SUCCESS - $script_name" >> "$SUCCESS_LOG"
                TOTAL_EXECUTED=$((TOTAL_EXECUTED + 1))
            else
                echo "⚠️  $script_name had errors/conflicts - logged but continued"
                echo "$(date): ERROR - $script_name" >> "$ERROR_LOG"
                TOTAL_ERRORS=$((TOTAL_ERRORS + 1))
            fi
            ;;
        "S")
            echo "⏭️  Skipped: $script_name"
            echo "$(date): SKIPPED - $script_name" >> "$EXECUTION_LOG"
            TOTAL_SKIPPED=$((TOTAL_SKIPPED + 1))
            ;;
        "V")
            echo ""
            echo "📖 Full Content of $script_name:"
            echo "────────────────────────────────"
            cat "$script" | sed 's/^/  /'
            echo "────────────────────────────────"
            echo ""
            echo "❓ Now what would you like to do?"
            echo "   [E] Execute this script"
            echo "   [S] Skip this script"
            echo ""
            echo -n "Choose [E/S]: "
            read -r subchoice
            
            case "$(echo $subchoice | tr '[:lower:]' '[:upper:]')" in
                "E")
                    echo "⚡ Executing: $script_name"
                    if docker exec -i kiosk_postgres psql -U kiosk_user -d kiosk_db -v ON_ERROR_STOP=0 < "$script" 2>/dev/null; then
                        echo "✅ $script_name executed successfully"
                        echo "$(date): SUCCESS - $script_name" >> "$SUCCESS_LOG"
                        TOTAL_EXECUTED=$((TOTAL_EXECUTED + 1))
                    else
                        echo "⚠️  $script_name had errors/conflicts"
                        echo "$(date): ERROR - $script_name" >> "$ERROR_LOG"
                        TOTAL_ERRORS=$((TOTAL_ERRORS + 1))
                    fi
                    ;;
                *)
                    echo "⏭️  Skipped: $script_name"
                    TOTAL_SKIPPED=$((TOTAL_SKIPPED + 1))
                    ;;
            esac
            ;;
        "Q")
            echo "🛑 Processing stopped by user"
            break
            ;;
        *)
            echo "⏭️  Invalid choice - skipping: $script_name"
            TOTAL_SKIPPED=$((TOTAL_SKIPPED + 1))
            ;;
    esac
done

# Final summary
echo ""
echo "📊 SQL Script Processing Summary"
echo "==============================="
echo "📜 Total scripts found: $SCRIPT_COUNT"
echo "🔄 Scripts processed: $TOTAL_PROCESSED"
echo "✅ Scripts executed: $TOTAL_EXECUTED"
echo "⏭️  Scripts skipped: $TOTAL_SKIPPED"
echo "⚠️  Scripts with errors: $TOTAL_ERRORS"

if [ $TOTAL_EXECUTED -gt 0 ]; then
    echo ""
    echo "✅ Successfully Executed:"
    if [ -f "$SUCCESS_LOG" ] && [ -s "$SUCCESS_LOG" ]; then
        cat "$SUCCESS_LOG" | sed 's/^/   /'
    fi
fi

if [ $TOTAL_ERRORS -gt 0 ]; then
    echo ""
    echo "⚠️  Scripts with Errors/Conflicts:"
    if [ -f "$ERROR_LOG" ] && [ -s "$ERROR_LOG" ]; then
        cat "$ERROR_LOG" | sed 's/^/   /'
    fi
    echo ""
    echo "💡 Note: Errors are usually due to:"
    echo "   - Data already exists (ON CONFLICT clauses)"
    echo "   - Missing dependencies (run schema creation first)"
    echo "   - Syntax issues in SQL"
fi

# Show final database state
echo ""
echo "🔍 Final Database State:"
echo "------------------------"
echo "$DATA_SUMMARY" | docker exec -i kiosk_postgres psql -U kiosk_user -d kiosk_db -t | while read -r line; do
    if [ -n "$line" ]; then
        echo "   📊 $(echo $line | xargs)"
    fi
done

echo ""
echo "🎉 SQL Script Processing Complete!"
echo ""
echo "💡 Next Steps:"
echo "   1. Review the execution summary above"
echo "   2. Check your database for expected data"
echo "   3. Create users via API if needed"
echo "   4. Test your application functionality"

# Cleanup
rm -f "$EXECUTION_LOG" "$SUCCESS_LOG" "$ERROR_LOG"