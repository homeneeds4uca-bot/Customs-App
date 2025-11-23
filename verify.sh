#!/bin/bash

# CustomsCompass Verification Script
# Checks if all services are running correctly

set -e

echo "🔍 CustomsCompass Service Verification"
echo "======================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

SUCCESS_COUNT=0
FAIL_COUNT=0

check_service() {
    local name=$1
    local url=$2
    local expected=$3

    printf "%-30s" "$name"

    response=$(curl -s -o /dev/null -w "%{http_code}" "$url" 2>/dev/null || echo "000")

    if [ "$response" == "$expected" ]; then
        echo -e "${GREEN}✓ OK${NC} (HTTP $response)"
        ((SUCCESS_COUNT++))
    else
        echo -e "${RED}✗ FAIL${NC} (HTTP $response, expected $expected)"
        ((FAIL_COUNT++))
    fi
}

check_port() {
    local name=$1
    local host=$2
    local port=$3

    printf "%-30s" "$name"

    if nc -z "$host" "$port" 2>/dev/null; then
        echo -e "${GREEN}✓ Listening${NC}"
        ((SUCCESS_COUNT++))
    else
        echo -e "${RED}✗ Not reachable${NC}"
        ((FAIL_COUNT++))
    fi
}

# Check Docker services
echo "📦 Docker Services"
echo "-------------------"

check_port "PostgreSQL" "localhost" "5432"
check_port "Redis" "localhost" "6379"
check_port "MinIO API" "localhost" "9000"
check_port "MinIO Console" "localhost" "9001"
check_port "Mailhog SMTP" "localhost" "1025"
check_port "Mailhog Web UI" "localhost" "8025"

echo ""

# Check Web services
echo "🌐 Web Services"
echo "-------------------"

check_service "Backend API Root" "http://localhost:8000/" "200"
check_service "Backend Health Check" "http://localhost:8000/health" "200"
check_service "Backend API Docs" "http://localhost:8000/api/docs" "200"
check_service "Frontend Landing Page" "http://localhost:3000/" "200"
check_service "MinIO Console" "http://localhost:9001/" "200"
check_service "Mailhog UI" "http://localhost:8025/" "200"

echo ""

# Test backend API
echo "🔌 Backend API Tests"
echo "-------------------"

printf "%-30s" "API Root Endpoint"
api_response=$(curl -s http://localhost:8000/ 2>/dev/null || echo "{}")
if echo "$api_response" | grep -q "CustomsCompass"; then
    echo -e "${GREEN}✓ OK${NC}"
    ((SUCCESS_COUNT++))
else
    echo -e "${RED}✗ FAIL${NC}"
    ((FAIL_COUNT++))
fi

printf "%-30s" "API Health Endpoint"
health_response=$(curl -s http://localhost:8000/health 2>/dev/null || echo "{}")
if echo "$health_response" | grep -q "healthy"; then
    echo -e "${GREEN}✓ OK${NC}"
    ((SUCCESS_COUNT++))
else
    echo -e "${RED}✗ FAIL${NC}"
    ((FAIL_COUNT++))
fi

echo ""

# Database check
echo "🗄️  Database"
echo "-------------------"

printf "%-30s" "PostgreSQL Connection"
if docker exec customs_postgres psql -U customs -d customs_compass -c "\dt" >/dev/null 2>&1; then
    echo -e "${GREEN}✓ Connected${NC}"
    ((SUCCESS_COUNT++))

    # Count tables
    TABLE_COUNT=$(docker exec customs_postgres psql -U customs -d customs_compass -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public';" 2>/dev/null | tr -d ' ')
    printf "%-30s" "Database Tables"
    if [ "$TABLE_COUNT" -gt 0 ]; then
        echo -e "${GREEN}✓ $TABLE_COUNT tables${NC}"
        ((SUCCESS_COUNT++))
    else
        echo -e "${YELLOW}⚠ No tables (run migrations)${NC}"
        ((FAIL_COUNT++))
    fi
else
    echo -e "${RED}✗ Cannot connect${NC}"
    ((FAIL_COUNT++))
fi

echo ""

# Redis check
echo "🔴 Redis"
echo "-------------------"

printf "%-30s" "Redis Connection"
if docker exec customs_redis redis-cli ping >/dev/null 2>&1; then
    echo -e "${GREEN}✓ Connected${NC}"
    ((SUCCESS_COUNT++))
else
    echo -e "${RED}✗ Cannot connect${NC}"
    ((FAIL_COUNT++))
fi

echo ""

# Summary
echo "======================================"
echo "📊 Summary"
echo "======================================"
echo ""

TOTAL=$((SUCCESS_COUNT + FAIL_COUNT))
SUCCESS_PERCENT=$((SUCCESS_COUNT * 100 / TOTAL))

echo "Total checks: $TOTAL"
echo -e "Passed: ${GREEN}$SUCCESS_COUNT${NC}"
echo -e "Failed: ${RED}$FAIL_COUNT${NC}"
echo "Success rate: $SUCCESS_PERCENT%"

echo ""

if [ $FAIL_COUNT -eq 0 ]; then
    echo -e "${GREEN}🎉 All services are running correctly!${NC}"
    exit 0
elif [ $FAIL_COUNT -lt 3 ]; then
    echo -e "${YELLOW}⚠️  Some services have issues. Check the failures above.${NC}"
    exit 1
else
    echo -e "${RED}❌ Multiple services are not running. Please check:${NC}"
    echo ""
    echo "1. Are Docker services running?"
    echo "   docker compose ps"
    echo ""
    echo "2. Is the backend running?"
    echo "   cd backend && source venv/bin/activate && uvicorn main:app --reload"
    echo ""
    echo "3. Is the frontend running?"
    echo "   cd frontend && npm run dev"
    echo ""
    exit 1
fi
