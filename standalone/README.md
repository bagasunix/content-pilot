# ✨ ContentPilot — Standalone

> **Blog automation yang bikin kamu produktif 10x lipat.**
> 
> Tanpa Hermes dependency. Bisa jalan di Windows/Linux.

---

## 🚀 Quick Start

### Option 1: Web UI (Recommended)

```bash
# Install
git clone https://github.com/bagasunix/contentpilot.git
cd contentpilot/standalone
pip install -r requirements.txt flask

# Start
./start.sh

# Open browser
http://localhost:8080
```

### Option 2: CLI

```bash
# Install
pip install -r requirements.txt

# Setup
python3 scripts/setup.py

# Activate
python3 scripts/activate.py --key SB-XXXX-XXXX-XXXX

# Run
python3 -m blog.pipeline status
```

---

## 📱 Web UI Features

| Page | Description |
|------|-------------|
| **Dashboard** | Overview of your blog pipeline |
| **Articles** | View and manage all articles |
| **Settings** | Configure domain, AI provider, etc. |
| **Activation** | Enter your license key |

---

## 🤖 AI Providers

| Provider | Model | Cost |
|----------|-------|------|
| OpenAI | GPT-4 | Paid |
| DeepSeek | DeepSeek Chat | Paid |
| Ollama | Llama2/Mistral | Free (local) |

---

## 📝 License

MIT License
