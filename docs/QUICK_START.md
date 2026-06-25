# Quick Start Card

> Setup Blog Lifecycle Pro dalam 5 menit.

## Step 1: Install

```bash
git clone <repo-url> blog-lifecycle-pro
cd blog-lifecycle-pro
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
python3 scripts/pipeline.py status
```

## Step 4: Mulai

```bash
# Lihat topik
python3 scripts/pipeline.py next

# Mulai riset
python3 scripts/pipeline.py research "topik anda"
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
python3 scripts/pipeline.py --help

# Baca docs
cat docs/SETUP_GUIDE.md
```
