#!/bin/bash
# Start Local File Server - Serve phone files via HTTP
# Usage: ./start_file_server.sh [port] [directory]

PORT="${1:-8080}"
SERVE_DIR="${2:-/storage/emulated/0/pixel8a}"

echo "📂 Starting File Server..."
echo "Port: $PORT"
echo "Serving: $SERVE_DIR"
echo ""
echo "Access at: http://localhost:$PORT"
echo "Stop with: Ctrl+C or kill the process"
echo ""

# Check if python available
if command -v python3 >/dev/null 2>&1; then
    echo "Using Python HTTP server..."
    cd "$SERVE_DIR" && python3 -m http.server "$PORT"
elif command -v busybox >/dev/null 2>&1; then
    echo "Using BusyBox httpd..."
    busybox httpd -f -p "$PORT" -h "$SERVE_DIR"
else
    echo "✗ No HTTP server available"
    echo "Install with: pkg install python"
    exit 1
fi
