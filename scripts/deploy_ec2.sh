#!/usr/bin/env bash
# ==============================================================================
# RaiSakshya EC2 Deployment Script
# Target EC2 Public IP: 3.110.208.141
# ==============================================================================

set -e

echo "=== 1. Updating System Packages ==="
sudo apt-get update -y && sudo apt-get install -y python3 python3-pip python3-venv git libgl1 libglib2.0-0

echo "=== 2. Setting Up Python Virtual Environment ==="
python3 -m venv venv
source venv/bin/activate

echo "=== 3. Installing Dependencies ==="
pip install --upgrade pip
pip install -r requirements.txt

echo "=== 4. Validating .env Configuration ==="
if [ ! -f .env ]; then
    echo "Creating .env from defaults..."
    cat << 'EOT' >> .env
EC2_PUBLIC_IP=3.110.208.141
HOST=0.0.0.0
PORT=5000
ALLOWED_ORIGINS=http://${EC2_PUBLIC_IP},http://${EC2_PUBLIC_IP}:5000,https://${EC2_PUBLIC_IP},https://${EC2_PUBLIC_IP}:5000,http://localhost:5000,http://127.0.0.1:5000,http://localhost:3000
ALLOW_ALL_CORS=true
ENABLE_HTTPS=true
SSL_CERT=cert.pem
SSL_KEY=key.pem
EOT
fi

# Load EC2_PUBLIC_IP from .env if present
if [ -f .env ]; then
    export $(grep -E '^EC2_PUBLIC_IP=' .env | xargs) 2>/dev/null || true
fi
SERVER_IP="${EC2_PUBLIC_IP:-3.110.208.141}"

echo "=== 5. Generating / Verifying SSL Certificate (Webcam & Secure Context Support) ==="
python3 scripts/generate_ssl.py

echo "=== 6. Starting RaiSakshya with Gunicorn Production Server (HTTPS) ==="
echo "=========================================================================="
echo " Secure HTTPS Access (Webcam Unlocked): https://${SERVER_IP}:5000"
echo " Note: In your browser, click 'Advanced' -> 'Proceed to ${SERVER_IP}'"
echo "       to accept the certificate and allow camera access."
echo "=========================================================================="
gunicorn --certfile cert.pem --keyfile key.pem --bind 0.0.0.0:5000 --workers 3 --threads 2 --timeout 120 app:app
