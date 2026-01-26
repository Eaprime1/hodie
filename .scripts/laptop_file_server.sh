#!/bin/bash
# Laptop File Server - Serve Q folder for local access
# Usage: ./laptop_file_server.sh [port]

PORT="${1:-8080}"
SERVE_DIR="/home/user/Q"

echo "📂 Starting Laptop File Server..."
echo "Port: $PORT"
echo "Serving from: $SERVE_DIR"
echo ""
echo "Access at:"
echo "  http://localhost:$PORT/                 (browse all)"
echo "  http://localhost:$PORT/hodie/           (hodie repo)"
echo "  http://localhost:$PORT/today/           (today folder)"
echo ""
echo "Stop with: Ctrl+C"
echo ""

# Check if python available
if ! command -v python3 >/dev/null 2>&1; then
    echo "✗ Python not found. Installing..."
    apt-get install -y python3
fi

echo "🚀 Starting server..."
cd "$SERVE_DIR" && python3 -m http.server "$PORT"
