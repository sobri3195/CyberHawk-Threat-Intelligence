#!/bin/bash

# TNI AU Threat Intelligence System - API Startup Script
# Starts both Python Flask API and Node.js Express API

echo "🚀 Starting TNI AU Threat Intelligence System APIs"
echo "=================================================="

# Kill any existing processes on ports 5001 and 5000
echo "🔧 Cleaning up existing processes..."
lsof -ti:5001 | xargs kill -9 2>/dev/null || true
lsof -ti:5000 | xargs kill -9 2>/dev/null || true

# Activate Python virtual environment and start Flask API
echo "🐍 Starting Python Flask API on port 5001..."
cd "$(dirname "$0")"
source .venv/bin/activate

# Start Flask API in background
python3 api.py > flask_api.log 2>&1 &
FLASK_PID=$!
echo "   ✓ Flask API started (PID: $FLASK_PID)"

# Wait a bit for Flask to start
sleep 2

# Start Node.js Express API
echo "🟢 Starting Node.js Express API on port 5000..."
npm run server > node_api.log 2>&1 &
NODE_PID=$!
echo "   ✓ Node.js API started (PID: $NODE_PID)"

echo ""
echo "✅ All APIs started successfully!"
echo ""
echo "📡 API Endpoints:"
echo "   Python Flask API: http://localhost:5001/api/health"
echo "   Node.js Express API: http://localhost:5000/api/health"
echo ""
echo "📋 Logs:"
echo "   Flask: flask_api.log"
echo "   Node.js: node_api.log"
echo ""
echo "🛑 To stop: kill $FLASK_PID $NODE_PID"
echo ""

# Save PIDs for later cleanup
echo $FLASK_PID > .flask_api.pid
echo $NODE_PID > .node_api.pid

# Wait for both processes
wait $FLASK_PID $NODE_PID
