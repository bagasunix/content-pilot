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
# Cek status
contentpilot status

# Mulai riset
contentpilot research "cara install docker"

# Lihat draft
ls workspace/drafts/

# Full pipeline
contentpilot full "cara install docker"
```

## Publish ke Blogger

```bash
# 1. Setup OAuth
contentpilot setup

# 2. Push draft
contentpilot push-draft <idea_id>

# 3. Attach images
contentpilot attach-images <idea_id>
```

## Standalone

```bash
cd standalone
pip install -r requirements.txt
contentpilot setup
contentpilot activate --key SB-XXXX-XXXX-XXXX
contentpilot status
```

## Web UI

```bash
cd standalone
pip install flask
./start.sh
# Buka http://localhost:8080
```
