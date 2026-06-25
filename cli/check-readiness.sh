#!/bin/bash
# Blog Lifecycle — Readiness Check
# Verifikasi semua dependensi & config untuk FASE 0-2

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

pass() { echo -e "${GREEN}✅ $1${NC}"; }
warn() { echo -e "${YELLOW}⚠️  $1${NC}"; }
fail() { echo -e "${RED}❌ $1${NC}"; FAILURES=$((FAILURES+1)); }

FAILURES=0

# Repo root + workspace, resolved from this script's location (HOME-independent).
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WS="${BLOG_WORKSPACE:-$REPO/workspace}"

echo "═══ Blog Lifecycle — Readiness Check ═══"
echo ""

# 1. Workspace
echo "── Workspace ($WS) ──"
[ -d "$WS" ] && pass "workspace/ exists" || fail "workspace/ missing"
[ -f "$WS/config.yaml" ] && pass "config.yaml exists" || fail "config.yaml missing"
[ -f "$WS/idea-bank.md" ] && pass "idea-bank.md exists" || fail "idea-bank.md missing"
[ -f "$WS/voice.md" ] && pass "voice.md exists" || warn "voice.md missing"
[ -d "$WS/drafts" ] && pass "drafts/ exists" || fail "drafts/ missing"
[ -d "$WS/published" ] && pass "published/ exists" || fail "published/ missing"
echo ""

# 2. Python
echo "── Python ──"
command -v python3 >/dev/null && pass "python3 available ($(python3 --version 2>&1 | cut -d' ' -f2))" || fail "python3 not found"
python3 -c "import yaml" 2>/dev/null && pass "PyYAML installed" || fail "PyYAML missing (pip install pyyaml)"
echo ""

# 3. Pipeline runner
echo "── Pipeline Runner ──"
PIPELINE="$REPO/scripts/pipeline.py"
[ -f "$PIPELINE" ] && pass "pipeline.py exists" || fail "pipeline.py missing"
if [ -f "$PIPELINE" ]; then
    python3 "$PIPELINE" status >/dev/null 2>&1 && pass "pipeline.py runs OK" || fail "pipeline.py has errors"
fi
echo ""

# 4. LLM endpoint
echo "── LLM (9router) ──"
if curl -s --connect-timeout 3 http://127.0.0.1:20128/v1/models >/dev/null 2>&1; then
    pass "9router reachable at :20128"
else
    warn "9router not reachable (pipeline still works with Hermes native)"
fi
echo ""

# 5. Templates
echo "── Templates ──"
TMPL_DIR="$REPO/templates"
[ -f "$TMPL_DIR/article-tutorial.md" ] && pass "tutorial template" || warn "tutorial template missing"
[ -f "$TMPL_DIR/article-listicle.md" ] && pass "listicle template" || warn "listicle template missing"
[ -f "$TMPL_DIR/article-news.md" ] && pass "news template" || warn "news template missing"
echo ""

# 6. OAuth (FASE 3 — optional now)
echo "── OAuth Blogger (FASE 3, optional) ──"
if [ -f "$WS/credentials.json" ]; then
    pass "credentials.json exists"
else
    warn "credentials.json belum ada (dibutuhkan untuk publish, bukan untuk draft)"
fi
if [ -f "$WS/token.json" ]; then
    pass "token.json exists"
else
    warn "token.json belum ada (dibutuhkan untuk publish)"
fi
echo ""

# Summary
echo "═══════════════════════════════════"
if [ $FAILURES -eq 0 ]; then
    echo -e "${GREEN}All checks passed. Pipeline ready for FASE 0-2.${NC}"
else
    echo -e "${RED}${FAILURES} check(s) failed. Fix before running pipeline.${NC}"
fi
