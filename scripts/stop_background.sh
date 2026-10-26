#!/usr/bin/env bash
# ==============================================================================
# Stop background RaiSakshya Gunicorn process
# ==============================================================================

if [ -f "gunicorn.pid" ]; then
    PID=$(cat gunicorn.pid)
    echo "Stopping Gunicorn process (PID: $PID)..."
    kill "$PID" 2>/dev/null || pkill -f "gunicorn.*app:app"
    rm -f gunicorn.pid
    echo "Server stopped successfully."
else
    echo "No gunicorn.pid file found. Killing any running gunicorn processes..."
    pkill -f "gunicorn.*app:app" 2>/dev/null || echo "No active processes found."
    echo "Done."
fi
