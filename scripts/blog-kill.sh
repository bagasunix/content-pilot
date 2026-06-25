#!/usr/bin/env bash
# blog-kill.sh — Stop all blog-lifecycle gateway processes
# Usage: bash scripts/blog-kill.sh

set -euo pipefail

PROFILES=(blog_orchestrator researcher writer editor imagery publisher blog_analyst)
KILLED=0

echo "=== blog-kill.sh ==="
for profile in "${PROFILES[@]}"; do
    PIDS=$(pgrep -f "hermes.*--profile $profile gateway" 2>/dev/null || true)
    if [ -n "$PIDS" ]; then
        echo "Stopping $profile (PIDs: $PIDS)..."
        echo "$PIDS" | xargs kill 2>/dev/null || true
        KILLED=$((KILLED + 1))
    else
        echo "  $profile — not running"
    fi
done

sleep 1
REMAINING=$(pgrep -f "hermes.*gateway run" 2>/dev/null | wc -l || echo 0)
echo ""
echo "Stopped: $KILLED profiles"
echo "Remaining hermes gateway processes: $REMAINING"
echo "Done."
