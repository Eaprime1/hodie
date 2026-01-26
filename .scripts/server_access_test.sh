#!/bin/bash
# Test File Server Access
# Usage: ./server_access_test.sh [port]

PORT="${1:-8080}"
BASE_URL="http://localhost:$PORT"

echo "🧪 Testing file server access..."
echo "Server: $BASE_URL"
echo ""

# Test if server is running
if ! curl -s "$BASE_URL" >/dev/null 2>&1; then
    echo "✗ Server not responding"
    echo "Start with: ./start_file_server.sh $PORT"
    exit 1
fi

echo "✓ Server is running"
echo ""

# Test accessing different locations
echo "Testing locations:"

for location in phone Q hodie today gdrive; do
    echo -n "  $location/ ... "
    if curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/$location/" | grep -q "200"; then
        echo "✓"
    else
        echo "✗ (not available)"
    fi
done

echo ""
echo "To access files:"
echo "  curl http://localhost:$PORT/hodie/.eric/ENJOY_THE_JOURNEY.md"
echo "  wget http://localhost:$PORT/Q/some_file.txt"
echo ""
