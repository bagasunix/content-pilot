# Quick Start Card

> Setup ContentPilot dalam 5 menit.

## Step 1: Install

```bash
git clone <repo-url> content-pilot
cd content-pilot
pip install pyyaml
```

## Step 2: Config

Edit `workspace/config.yaml`:

```yaml
domain: bloganda.com
blog_id: "YOUR_BLOG_ID"
```

## Step 3: Test

```bash
contentpilot status
```

## Step 4: Mulai

```bash
# Lihat topik
contentpilot next

# Mulai riset
contentpilot research "topik anda"
```

## Commands Penting

| Command | Fungsi |
|---------|--------|
| `status` | Lihat status pipeline |
| `next` | Topik berikutnya |
| `research "topik"` | Mulai riset |
| `draft <id>` | Buat draft |
| `gate <id>` | Quality check |
| `approve <id>` | Approve artikel |
| `push <id>` | Publish ke Blogger |

## Butuh Bantuan?

```bash
# Lihat semua commands
contentpilot --help

# Baca docs
cat docs/SETUP_GUIDE.md
```
