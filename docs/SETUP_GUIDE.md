# Setup Guide - ContentPilot

> Panduan lengkap setup ContentPilot untuk customer.

## Requirements

- Python 3.10+
- Akun Blogger (Google account)
- Domain blog sendiri (opsional)

## Installation

### 1. Clone Repository

```bash
git clone <repo-url> content-pilot
cd content-pilot
```

### 2. Install Dependencies

```bash
pip install pyyaml
```

### 3. Setup Configuration

Edit `workspace/config.yaml`:

```yaml
domain: bloganda.com          # Domain blog Anda
blog_id: "123456789"          # ID blog dari Blogger
language: id                  # Bahasa konten
publish_mode: draft           # draft atau live
autonomy: gated               # gated = butuh approval manual
wip_limit: 3                  # Max artikel aktif
```

### 4. Setup Notifications (Optional)

```bash
# Telegram (Recommended)
# 1. Buat bot via @BotFather
# 2. Dapatkan chat ID
# 3. Edit workspace/config.yaml

notifications:
  telegram:
    enabled: true
    bot_token: "YOUR_BOT_TOKEN"
    chat_id: "YOUR_CHAT_ID"
```

Lihat `docs/TELEGRAM_SETUP.md` untuk panduan lengkap.

### 5. Setup OAuth (untuk Publish)

1. Buat Google Cloud Project, enable **Blogger API v3**
2. Buat **OAuth 2.0 Client ID** (type *Web application*) dengan redirect
   `http://127.0.0.1:8080/oauth2/callback`
3. Sediakan `GOOGLE_CLIENT_ID`/`GOOGLE_CLIENT_SECRET` (env) atau
   `workspace/credentials.json`
4. Di aplikasi: **Settings → Google / Blogger → Connect Google**

Detail lengkap: `docs/setup-credentials.md`.

### 5. Verifikasi Setup

```bash
# Cek status
contentpilot status

# Cek koneksi
contentpilot check
```

## Quick Start

### Mulai Artikel Baru

```bash
# 1. Lihat topik yang tersedia
contentpilot next

# 2. Mulai riset
contentpilot research "cara install docker"

# 3. Lihat status
contentpilot status
```

### Pipeline Workflow

```
1. Research    → contentpilot research "topik"
2. Write       → contentpilot draft <idea_id>
3. Review      → contentpilot review <idea_id>
4. Gate        → contentpilot gate <idea_id>
5. Approve     → contentpilot approve <idea_id>
6. Publish     → contentpilot push <idea_id>
```

## Configuration Reference

### workspace/config.yaml

| Field | Description | Default |
|-------|-------------|---------|
| `domain` | Blog domain | - |
| `blog_id` | Blogger blog ID | - |
| `language` | Bahasa konten | `id` |
| `publish_mode` | `draft` atau `live` | `draft` |
| `autonomy` | `gated` atau `auto` | `gated` |
| `wip_limit` | Max artikel aktif | `3` |

### workspace/voice.md

Panduan menulis konten. Edit untuk menyesuaikan gaya tulisan Anda.

### workspace/idea-bank.md

Antrian topik. Format:

```markdown
### [H] Judul Artikel
- idea_id: slug-artikel
- keyword target: kata kunci
- kategori: Technology
- status: idea
```

Prioritas: H (High) > M (Medium) > L (Low)

## Commands Reference

### Pipeline Commands

```bash
# Status
contentpilot status

# Topik berikutnya
contentpilot next

# Research
contentpilot research "topik"

# Draft
contentpilot draft <idea_id>

# Review
contentpilot review <idea_id>

# Quality Gate
contentpilot gate <idea_id>

# Approve (manual)
contentpilot approve <idea_id>

# Publish
contentpilot push <idea_id>

# Attach images
contentpilot images <idea_id>
```

### Utility Commands

```bash
# Cek status
contentpilot status

# Reconcile state
contentpilot reconcile

# Run tests
python3 -m unittest discover -s tests -t . -v
```

## Quality Gates

System otomatis cek kualitas artikel:

| Gate | Tipe | Description |
|------|------|-------------|
| Word count | FAIL | Minimal 600 kata |
| SEO fields | FAIL | Title, meta, slug, keywords wajib |
| AI-tells | FAIL | Tidak ada frasa AI generik |
| Hoax links | FAIL | Tidak ada link hoax |
| Dead links | FAIL | Tidak ada link mati |
| Images | FAIL | Minimal 1 gambar |
| Markers | FAIL | Tidak ada TODO/FIXME |
| Voice | WARN | Tidak pakai "Anda" |

### AI-Tell Phrases (Hard Fail)

- "di era digital"
- "sangat penting"
- "tidak dapat dipungkiri"
- "menjadi salah satu"
- "hadir sebagai solusi"
- dll (lihat `blog/domain/gates.py`)

## Troubleshooting

### Pipeline Error

```bash
# Cek log
cat workspace/journal.jsonl | tail -10

# Reconcile
contentpilot reconcile
```

### OAuth Expired

```bash
# Re-setup
python3 scripts/setup_oauth.py
```

### Gate Fail

```bash
# Lihat detail
contentpilot gate <idea_id> --verbose

# Fix manual
# Edit draft di workspace/drafts/<idea_id>/draft.md
```

### WIP Limit

```bash
# Cek status
contentpilot status

# Selesaikan atau drop artikel
contentpilot drop <idea_id>
```

## Support

- Dokumentasi: `docs/`
- Issues: <repo-url>/issues
- Email: support@bloglifecyclepro.com

## License

MIT
