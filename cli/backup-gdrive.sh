#!/bin/bash
# blog-lifecycle Backup Script
# Compress, encrypt, upload to Google Drive (folder: blog-lifecycle-backups/)
# Usage: bash blog-lifecycle-backup.sh

set -euo pipefail

# ─── Config ──────────────────────────────────────────────────────────────────
SRC_DIR="$HOME/Project/blog-lifecycle"
BACKUP_NAME="blog-lifecycle-$(date +%Y%m%d_%H%M%S)"
STAGING_DIR="/tmp/blog-lifecycle-backup-$$"
GDRIVE_REMOTE="Google:blog-lifecycle-backups"
ENCRYPT_PASSPHRASE="${BACKUP_ENCRYPT_PASSPHRASE:-}"

# ─── Validation ──────────────────────────────────────────────────────────────
if [ ! -d "$SRC_DIR" ]; then
    echo "❌ Source directory not found: $SRC_DIR"
    exit 1
fi

if [ -z "$ENCRYPT_PASSPHRASE" ]; then
    # Try loading from hermes .env
    if [ -f "$HOME/.hermes/.env" ]; then
        ENCRYPT_PASSPHRASE=$(grep -E "^BACKUP_ENCRYPT_PASSPHRASE" "$HOME/.hermes/.env" 2>/dev/null | cut -d'=' -f2 | tr -d '"' | tr -d "'" || true)
    fi
fi

if [ -z "$ENCRYPT_PASSPHRASE" ]; then
    # Try loading from passphrase file (same as hermes-backup.sh)
    if [ -f "$HOME/.hermes/.backup-passphrase" ]; then
        ENCRYPT_PASSPHRASE=$(cat "$HOME/.hermes/.backup-passphrase" 2>/dev/null || true)
    fi
fi

if [ -z "$ENCRYPT_PASSPHRASE" ]; then
    echo "⚠️  No encryption passphrase found — uploading unencrypted"
    DO_ENCRYPT=false
else
    DO_ENCRYPT=true
fi

# ─── Staging ─────────────────────────────────────────────────────────────────
mkdir -p "$STAGING_DIR"

echo "📦 Creating archive: blog-lifecycle-backup.tar.gz"
cd "$(dirname "$SRC_DIR")"
tar -czf "$STAGING_DIR/$BACKUP_NAME.tar.gz" \
    --exclude='.git' \
    --exclude='node_modules' \
    --exclude='__pycache__' \
    --exclude='.pytest_cache' \
    --exclude='.venv' \
    --exclude='*.pyc' \
    "$(basename "$SRC_DIR")"

ARCHIVE_SIZE=$(du -h "$STAGING_DIR/$BACKUP_NAME.tar.gz" | cut -f1)
echo "   Archive size: $ARCHIVE_SIZE"

# ─── Encrypt ─────────────────────────────────────────────────────────────────
FINAL_FILE="$STAGING_DIR/$BACKUP_NAME.tar.gz"
if [ "$DO_ENCRYPT" = true ]; then
    echo "🔐 Encrypting archive..."
    gpg --batch --yes --symmetric \
        --cipher-algo AES256 \
        --passphrase "$ENCRYPT_PASSPHRASE" \
        --output "$FINAL_FILE.gpg" \
        "$FINAL_FILE"
    FINAL_FILE="$FINAL_FILE.gpg"
    FINAL_SIZE=$(du -h "$FINAL_FILE" | cut -f1)
    echo "   Encrypted size: $FINAL_SIZE"
fi

# ─── Upload to Google Drive ─────────────────────────────────────────────────
echo "☁️  Uploading to $GDRIVE_REMOTE..."
rclone copy "$FINAL_FILE" "$GDRIVE_REMOTE/" \
    --no-traverse \
    --stats-one-line \
    --log-level INFO

# ─── Verify ──────────────────────────────────────────────────────────────────
echo "🔍 Verifying upload..."
UPLOADED=$(rclone ls "$GDRIVE_REMOTE/" 2>/dev/null | grep "$(basename "$FINAL_FILE")" | wc -l)
if [ "$UPLOADED" -gt 0 ]; then
    echo "✅ Upload verified"
else
    echo "❌ Upload verification failed!"
    exit 1
fi

# ─── Cleanup old backups (keep last 10) ─────────────────────────────────────
echo "🧹 Cleaning old backups (keep last 10)..."
BACKUP_COUNT=$(rclone ls "$GDRIVE_REMOTE/" 2>/dev/null | grep -c "\.tar\.gz" || true)
if [ "$BACKUP_COUNT" -gt 10 ]; then
    DELETE_COUNT=$((BACKUP_COUNT - 10))
    rclone delete "$GDRIVE_REMOTE/" \
        --min-age "30d" \
        --include "*.tar.gz.gpg" \
        --include "*.tar.gz" \
        --max-delete "$DELETE_COUNT" \
        --log-level INFO 2>/dev/null
    echo "   Deleted $DELETE_COUNT old backup(s)"
else
    echo "   No cleanup needed ($BACKUP_COUNT backups)"
fi

# ─── Local cleanup ───────────────────────────────────────────────────────────
rm -rf "$STAGING_DIR"

echo ""
echo "════════════════════════════════════════════════"
echo "✅ Blog Lifecycle Backup Complete"
echo "════════════════════════════════════════════════"
echo "📅 $(date '+%Y-%m-%d %H:%M:%S')"
echo "📦 $(basename "$FINAL_FILE")"
echo "☁️  $GDRIVE_REMOTE/"
echo "════════════════════════════════════════════════"
