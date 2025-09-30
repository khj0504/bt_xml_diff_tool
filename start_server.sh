#!/bin/bash

# BehaviorTree XML Diff Tool - HTTP Server Starter
# Usage: ./start_server.sh [port]

PORT=${1:-8080}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🚀 Starting BehaviorTree Analysis Server..."
echo "📁 Serving from: $SCRIPT_DIR"
echo "🌐 Server will be available at: http://localhost:$PORT"
echo "📄 HTML result files will be served from this directory"
echo ""

# Kill any existing servers on this port
pkill -f "python3 -m http.server $PORT" 2>/dev/null || true

# Start HTTP server in the script directory
cd "$SCRIPT_DIR" || exit 1
python3 -m http.server "$PORT"