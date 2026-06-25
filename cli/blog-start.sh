#!/usr/bin/env bash
# blog-start.sh — Start all blog-lifecycle gateway processes
# Usage: bash scripts/blog-start.sh
# Requires: ~/.hermes/hermes-agent/venv/bin/hermes

set -euo pipefail

HERMES_BIN="$HOME/.hermes/hermes-agent/venv/bin/hermes"
LOG_DIR="/tmp/hermes-gateways"
PROFILES=(blog_orchestrator researcher writer editor imagery publisher blog_analyst)

mkdir -p "$LOG_DIR"

if [ ! -x "$HERMES_BIN" ]; then
    echo "ERROR: hermes binary not found at $HERMES_BIN"
    exit 1
fi

echo "=== blog-start.sh ==="
STARTED=0

for profile in "${PROFILES[@]}"; do
    RUNNING=$(pgrep -f "hermes.*--profile $profile gateway" 2>/dev/null || true)
    if [ -n "$RUNNING" ]; then
        echo "  $profile — already running (PID: $RUNNING)"
        continue
    fi

    LOG="$LOG_DIR/${profile}.log"
    nohup "$HERMES_BIN" --profile "$profile" gateway run > "$LOG" 2>&1 &
    NEW_PID=$!
    echo "  $profile — started (PID: $NEW_PID, log: $LOG)"
    STARTED=$((STARTED + 1))
    sleep 0.5
done

echo ""
echo "Started: $STARTED new profiles"
echo "Logs: $LOG_DIR/"

# Quick health check
sleep 3
echo ""
echo "=== Health check ==="
for profile in "${PROFILES[@]}"; do
    PID=$(pgrep -f "hermes.*--profile $profile gateway" 2>/dev/null || echo "DEAD")
    echo "  $profile: $PID"
done

echo ""
echo "Done."
