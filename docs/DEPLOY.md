# Deploy ContentPilot

Panduan install dan jalankan ContentPilot.

---

## Prasyarat
- Python 3.10+
- pip
- (Optional) Ollama / OpenAI API key untuk AI writing

## Install

```bash
git clone https://github.com/bagasunix/contentpilot.git
cd contentpilot
pip install -r requirements.txt
```

## Setup

```bash
python3 scripts/setup_wizard.py
```

Wizard akan minta:
- Domain blog
- Blog ID (dari Blogger)
- AI provider (Ollama/OpenAI/DeepSeek)
- API key

## Jalankan

```bash
# Start server + client
./start.sh

# Atau manual:
cd standalone && ./start.sh
```

## Standalone Mode

```bash
cd standalone
pip install -r requirements.txt
./start.sh
# Buka http://localhost:8080
```

## Google Connection

Google OAuth sekarang ditangani server-side. Tidak perlu setup Cloud Project sendiri.

1. Buka Settings → Google / Blogger
2. Klik **Connect Google**
3. Login & approve consent di browser
4. Token disimpan otomatis di server

> Lihat [setup-credentials.md](setup-credentials.md) untuk detail lengkap.

## Publish ke Blogger

```bash
# 1. Connect Google (via Settings → Connect Google)
# 2. Push draft
contentpilot push-draft <idea_id>

# 3. Attach images
contentpilot attach-images <idea_id>
```

## Web UI

```bash
cd standalone
pip install flask
./start.sh
# Buka http://localhost:8080
```

## Config

Config path priority:
1. `config/config.yaml` (per INSTALLATION.md)
2. `workspace/config.yaml` (fallback)
