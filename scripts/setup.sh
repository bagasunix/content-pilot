#!/usr/bin/env bash
# Blog Lifecycle — Setup & Dependency Check
set -e

echo "🔍 Checking dependencies..."

check_cmd() {
    if command -v "$1" &>/dev/null; then
        echo "  ✅ $1 $(command -v $1)"
    else
        echo "  ❌ $1 — NOT FOUND"
        MISSING+=("$1")
    fi
}

MISSING=()

check_cmd python3
check_cmd rclone
check_cmd jq
check_cmd curl

echo ""
echo "🔍 Checking Python packages..."
PYTHON=~/venv/bin/python3

if [ -f "$PYTHON" ]; then
    echo "  ✅ Python venv: $PYTHON"
    declare -A PYIMPORTS=(
        [google-auth]="google.auth"
        [google-auth-oauthlib]="google_auth_oauthlib"
        [google-api-python-client]="googleapiclient"
        [httpx]="httpx"
        [markdown]="markdown"
    )
    for pkg in google-auth google-auth-oauthlib google-api-python-client httpx markdown; do
        if $PYTHON -c "import ${PYIMPORTS[$pkg]}" 2>/dev/null; then
            echo "  ✅ $pkg"
        else
            echo "  ❌ $pkg — pip install $pkg"
            MISSING+=("pip:$pkg")
        fi
    done
else
    echo "  ❌ Python venv not found at $PYTHON"
    MISSING+=("venv")
fi

echo ""
echo "🔍 Checking config..."

ENV_FILE="$(dirname "$0")/../config/.env"
if [ -f "$ENV_FILE" ]; then
    echo "  ✅ .env exists"
    # Check required vars
    for var in BLOGGER_BLOG_ID TELEGRAM_BOT_TOKEN BLOG_URL; do
        if grep -q "^${var}=.\+" "$ENV_FILE"; then
            echo "  ✅ $var set"
        else
            echo "  ⚠️  $var — empty or missing"
        fi
    done
else
    echo "  ❌ .env not found — copy .env.example → .env and fill values"
    MISSING+=("config/.env")
fi

echo ""
if [ ${#MISSING[@]} -eq 0 ]; then
    echo "🎉 All good! Ready to run blog lifecycle."
else
    echo "⚠️  Missing ${#MISSING[@]} items. Fix above issues before running automation."
fi
