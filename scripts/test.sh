#!/bin/bash
# Test script for AniList GPT MCP Server
# Run this to verify all components are working

set -e

BASE_URL="${BASE_URL:-http://localhost:8000}"

echo "🧪 Testing AniList GPT MCP Server"
echo "================================"
echo "Base URL: $BASE_URL"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

test_endpoint() {
    local name=$1
    local endpoint=$2
    local expected_status=${3:-200}
    
    echo -n "Testing $name... "
    
    status=$(curl -s -o /dev/null -w "%{http_code}" "${BASE_URL}${endpoint}" || echo "000")
    
    if [ "$status" = "$expected_status" ]; then
        echo -e "${GREEN}✓${NC} (HTTP $status)"
        return 0
    else
        echo -e "${RED}✗${NC} (Expected $expected_status, got $status)"
        return 1
    fi
}

test_mcp() {
    echo -n "Testing MCP Protocol... "
    
    response=$(curl -s -X POST "${BASE_URL}/mcp" \
        -H "Content-Type: application/json" \
        -d '{
            "jsonrpc": "2.0",
            "method": "initialize",
            "params": {
                "clientInfo": {"name": "test", "version": "1.0"}
            },
            "id": 1
        }')
    
    if echo "$response" | grep -q "protocolVersion"; then
        echo -e "${GREEN}✓${NC}"
        return 0
    else
        echo -e "${RED}✗${NC}"
        echo "Response: $response"
        return 1
    fi
}

test_search_anime() {
    echo -n "Testing search_anime tool... "
    
    response=$(curl -s -X POST "${BASE_URL}/mcp" \
        -H "Content-Type: application/json" \
        -d '{
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "search_anime",
                "arguments": {
                    "query": "Attack on Titan",
                    "per_page": 5
                }
            },
            "id": 2
        }')
    
    if echo "$response" | grep -q "results"; then
        echo -e "${GREEN}✓${NC}"
        return 0
    else
        echo -e "${RED}✗${NC}"
        echo "Response: $response"
        return 1
    fi
}

test_trending() {
    echo -n "Testing get_trending_anime tool... "
    
    response=$(curl -s -X POST "${BASE_URL}/mcp" \
        -H "Content-Type: application/json" \
        -d '{
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "get_trending_anime",
                "arguments": {
                    "per_page": 5
                }
            },
            "id": 3
        }')
    
    if echo "$response" | grep -q "results"; then
        echo -e "${GREEN}✓${NC}"
        return 0
    else
        echo -e "${RED}✗${NC}"
        return 1
    fi
}

# Run tests
echo ""
echo "📊 Health Checks"
echo "----------------"
test_endpoint "Root endpoint" "/"
test_endpoint "Health check" "/health"
test_endpoint "DB health" "/health/db"
test_endpoint "Redis health" "/health/redis"

echo ""
echo "🔧 MCP Protocol Tests"
echo "---------------------"
test_mcp
test_search_anime
test_trending

echo ""
echo "✅ All tests completed!"
echo ""
echo "📝 Next Steps:"
echo "   1. Check any failed tests above"
echo "   2. Verify all tools are responding"
echo "   3. Test OAuth flow manually"
echo "   4. Check logs: fly logs --app anilist-gpt"
