# ✨ ContentPilot

> **From idea to published blog post — in minutes, not hours.**

ContentPilot is an AI-powered blog automation pipeline that handles the entire content creation process: research, writing, quality checking, and publishing.

**You bring your own AI** (OpenAI, DeepSeek, or Ollama). **We handle the pipeline.**

---

## Why ContentPilot?

Writing a blog post manually takes 4-8 hours. With ContentPilot:

| Step | Manual | ContentPilot |
|------|--------|-------------|
| Research keywords | 1-2 hours | 2 minutes |
| Write 1000+ word article | 2-4 hours | 5 minutes |
| SEO optimization | 30 min | Automatic |
| Quality check | 1 hour | Instant |
| Publish to Blogger | 10 min | One command |
| **Total** | **4-8 hours** | **~10 minutes** |

---

## Quick Start

```bash
# 1. Install
git clone https://github.com/bagasunix/content-pilot.git
cd content-pilot
pip install -r requirements.txt

# 2. Setup
python3 cli/setup_wizard.py

# 3. Run
python3 -m contentpilot.pipeline status
python3 -m contentpilot.pipeline full "how to install docker"
```

---

## How It Works

```
📝 Idea ──→ 🔍 Research ──→ ✍️ Write ──→ 🔍 Quality Gate ──→ 🚀 Publish
```

**Quality Gate catches:**
- ❌ AI-tell phrases ("Di era digital saat ini...")
- ❌ Dead links (404/410)
- ❌ Hoax domains
- ❌ Missing SEO fields
- ❌ Articles under 600 words

---

## Project Structure

```
content-pilot/
├── src/contentpilot/       # Core pipeline library
│   ├── domain/             # Entities, gates, stages
│   ├── application/        # Use cases, ports
│   ├── infrastructure/     # Adapters (Blogger, files)
│   └── interface/          # CLI entry point
├── cli/                    # CLI commands
├── templates/              # Article templates
├── workspace/              # Runtime data (drafts, config)
├── config/                 # Config templates
├── docs/                   # Documentation
├── pyproject.toml
└── requirements.txt
```

---

## Bring Your Own AI

```yaml
# OpenAI
ai:
  provider: openai
  model: gpt-4

# DeepSeek (cheaper)
ai:
  provider: deepseek
  model: deepseek-chat

# Ollama (free, local)
ai:
  provider: ollama
  model: llama2
```

---

## Commands

```bash
python3 -m contentpilot.pipeline status          # See all articles
python3 -m contentpilot.pipeline next            # Pick next topic
python3 -m contentpilot.pipeline research "topic" # Research
python3 -m contentpilot.pipeline draft <id>       # Write
python3 -m contentpilot.pipeline gate <id>        # Quality check
python3 -m contentpilot.pipeline approve <id>     # Human approval
python3 -m contentpilot.pipeline push-draft <id>  # Publish
```

---

## Perfect For

- **🧑‍💻 Solo Bloggers** — Stop staring at blank pages
- **📝 Content Creators** — Publish 10x more content
- **🏢 Agencies** — Standardize content workflow
- **📈 SEO Professionals** — All-in-one pipeline

---

## License

MIT License — free for personal and commercial use.

---

<div align="center">

**ContentPilot** — From idea to published post in minutes.

[![GitHub stars](https://img.shields.io/github/stars/bagasunix/content-pilot?style=social)](https://github.com/bagasunix/content-pilot)
[![GitHub forks](https://img.shields.io/github/forks/bagasunix/content-pilot?style=social)](https://github.com/bagasunix/content-pilot)

</div>
