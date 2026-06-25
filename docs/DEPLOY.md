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
python3 scripts/pipeline.py status

# Mulai riset
python3 scripts/pipeline.py research "cara install docker"

# Lihat draft
ls workspace/drafts/

# Full pipeline
python3 scripts/pipeline.py full "cara install docker"
```

## Publish ke Blogger

```bash
# 1. Setup OAuth
python3 scripts/setup_credentials.py

# 2. Push draft
python3 scripts/pipeline.py push-draft <idea_id>

# 3. Attach images
python3 scripts/pipeline.py attach-images <idea_id>
```

## Standalone (tanpa Hermes)

```bash
cd standalone
pip install -r requirements.txt
python3 scripts/setup.py
python3 scripts/activate.py --key SB-XXXX-XXXX-XXXX
python3 -m blog.pipeline status
```

## Web UI

```bash
cd standalone
pip install flask
./start.sh
# Buka http://localhost:8080
```
