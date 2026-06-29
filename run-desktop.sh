#!/bin/bash
# ContentPilot Desktop — Quick Launch Script
#
# Usage:
#   ./run-desktop.sh              # Start with defaults
#   ./run-desktop.sh --debug      # Flask debug mode
#   ./run-desktop.sh --port 5001  # Custom port

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}ContentPilot Desktop${NC}"
echo "===================="

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}ERROR: python3 not found${NC}"
    exit 1
fi

# Check dependencies
echo -e "${YELLOW}Checking dependencies...${NC}"
python3 -c "import webview" 2>/dev/null || {
    echo -e "${YELLOW}Installing pywebview...${NC}"
    pip install pywebview[qt]
}

python3 -c "import flask" 2>/dev/null || {
    echo -e "${YELLOW}Installing flask...${NC}"
    pip install flask flask-limiter flask-wtf
}

# Check if server is already running on port
PORT="${1:-8080}"
if [[ "$1" == "--port" ]]; then
    PORT="$2"
fi

if lsof -i :"$PORT" &> /dev/null; then
    echo -e "${YELLOW}WARNING: Port $PORT already in use${NC}"
    echo "Use --port to specify different port"
    # If server already running, connect to it
    echo -e "${GREEN}Connecting to existing server...${NC}"
    python3 web/desktop.py --server-url "http://127.0.0.1:$PORT" "${@}"
else
    echo -e "${GREEN}Starting ContentPilot Desktop...${NC}"
    python3 web/desktop.py "${@}"
fi
