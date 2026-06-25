#!/bin/bash
# Retarget hardcoded project path saat pindah mesin (mis. WSL → VPS).
#
# Skill & task-prompt nyimpen path absolut /home/bagas/Project/blog-lifecycle
# (perlu absolut karena profil Hermes me-remap $HOME). Di VPS dgn path beda,
# jalanin sekali ini buat rewrite semua ref.
#
# Usage:  bash scripts/retarget.sh /abs/path/baru/blog-lifecycle
# Contoh: bash scripts/retarget.sh /opt/blog-lifecycle
set -euo pipefail

NEW="${1:-}"
[ -z "$NEW" ] && { echo "Usage: bash scripts/retarget.sh /abs/path/baru/blog-lifecycle"; exit 1; }
case "$NEW" in /*) ;; *) echo "Path harus absolut (mulai dgn /)"; exit 1;; esac

OLD="/home/bagas/Project/blog-lifecycle"
REPO="$(cd "$(dirname "$0")/.." && pwd)"

echo "Retarget: $OLD  →  $NEW"

# 1) File project (skills + scripts)
mapfile -t FILES < <(grep -rl "$OLD" "$REPO/skills" "$REPO/scripts" 2>/dev/null || true)
for f in "${FILES[@]:-}"; do
  [ -n "$f" ] && sed -i "s#$OLD#$NEW#g" "$f" && echo "  ✓ $f"
done

# 2) Profil Hermes (env + bashrc) — kalau ada di mesin ini
for f in "$HOME/.hermes/profiles/blog/.env" "$HOME/.hermes/profiles/blog/home/.bashrc"; do
  [ -f "$f" ] && grep -q "$OLD" "$f" && sed -i "s#$OLD#$NEW#g" "$f" && echo "  ✓ $f"
done

echo ""
if grep -rl "$OLD" "$REPO/skills" "$REPO/scripts" 2>/dev/null; then
  echo "⚠️  Masih ada sisa ref di atas — cek manual."
else
  echo "✅ Beres. Tidak ada sisa '$OLD' di skills/scripts."
fi
echo "Ingat: cron job & webhook subscription dibuat ULANG di VPS (lihat DEPLOY.md),"
echo "jadi prompt-nya otomatis pakai path baru."
