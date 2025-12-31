#!/bin/bash
# Start Unified File Server - Serve from parent directory for access to all locations
# Usage: ./start_unified_server.sh [port]

PORT="${1:-8080}"

# Serve from /storage/emulated/0/pixel8a to access everything
SERVE_DIR="/storage/emulated/0/pixel8a"

echo "📂 Starting Unified File Server..."
echo "Port: $PORT"
echo "Serving from: $SERVE_DIR"
echo ""
echo "Access at:"
echo "  http://localhost:$PORT/                 (browse all)"
echo "  http://localhost:$PORT/Q/               (Q workspace)"
echo "  http://localhost:$PORT/Q/hodie/         (hodie repo)"
echo "  http://localhost:$PORT/Q/today/         (today repo)"
echo ""
echo "Stop with: Ctrl+C"
echo ""

# Check if python available
if ! command -v python3 >/dev/null 2>&1; then
    echo "✗ Python not found. Install with: pkg install python"
    exit 1
fi

echo "Using Python HTTP server..."
cd "$SERVE_DIR" && python3 -m http.server "$PORT"
