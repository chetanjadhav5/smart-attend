#!/usr/bin/env bash
# ==============================================================================
# Start RaiSakshya in the background (survives SSH disconnect)
# ==============================================================================

# Activate virtual environment if present
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Ensure SSL cert exists
if [ ! -f "cert.pem" ] || [ ! -f "key.pem" ]; then
    python3 scripts/generate_ssl.py
fi

echo "Starting RaiSakshya Gunicorn daemon in the background..."

# Run Gunicorn as a background daemon
gunicorn \
    --daemon \
    --certfile cert.pem \
    --keyfile key.pem \
    --bind 0.0.0.0:5000 \
    --workers 3 \
    --threads 2 \
    --timeout 120 \
    --pid gunicorn.pid \
    --access-logfile access.log \
    --error-logfile error.log \
    app:app

echo "=========================================================================="
echo " RaiSakshya is now running in the BACKGROUND!"
echo " Safe to close SSH session."
echo " Access URL: https://3.110.208.141:5000"
echo " Process PID: $(cat gunicorn.pid 2>/dev/null)"
echo " Check logs anytime with: tail -f error.log"
echo " Stop server anytime with: bash scripts/stop_background.sh"
echo "=========================================================================="
