#!/bin/bash
# ContentPilot — Start Web Dashboard

echo "=========================================="
echo "  ContentPilot — Web Dashboard"
echo "=========================================="
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required"
    exit 1
fi

# Check if Flask is installed
python3 -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing Flask..."
    pip3 install flask
fi

# Start the web server
echo "Starting ContentPilot..."
echo ""
echo "Open in your browser: http://localhost:8080"
echo ""
echo "Press Ctrl+C to stop"
echo ""

cd "$(dirname "$0")"
python3 web/app.py
