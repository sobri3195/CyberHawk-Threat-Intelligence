#!/bin/bash

echo "🚀 Starting TNI AU Threat Intelligence System..."
echo ""

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
    echo ""
fi

# Start backend server
echo "🔧 Starting backend server..."
npm run server > server.log 2>&1 &
SERVER_PID=$!
echo "✅ Backend server started (PID: $SERVER_PID)"
sleep 2

# Start frontend dev server
echo "🎨 Starting frontend dev server..."
echo ""
echo "============================================"
echo "  TNI AU - Threat Intelligence System"
echo "============================================"
echo ""
echo "  Frontend: http://localhost:3000"
echo "  Backend:  http://localhost:5000"
echo ""
echo "  Press Ctrl+C to stop all servers"
echo "============================================"
echo ""

npm run dev
