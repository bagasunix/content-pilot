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

## What You Get

**🧠 Smart Research**
- AI finds the best keywords and topics
- Competitor analysis built-in
- Content angle suggestions

**✍️ Quality Writing**
- AI-generated articles that don't sound like AI
- 19 AI-tell phrases automatically detected and removed
- Voice guide keeps your tone consistent

**📊 SEO Scoring**
- Real-time SEO score (0-100)
- Readability grading
- Internal linking suggestions

**🚀 One-Click Publish**
- Auto-post to Blogger
- Draft or live mode
- Featured image upload

---

## Quick Start

```bash
# 1. Install
git clone https://github.com/bagasunix/content-pilot.git
cd content-pilot
pip install -r requirements.txt

# 2. Setup (interactive wizard)
python3 scripts/setup_wizard.py

# 3. Run
python3 scripts/pipeline.py status
python3 scripts/pipeline.py full "how to install docker on ubuntu"
```

That's it. Your article is ready in `workspace/drafts/`.

---

## How It Works

```
┌─────────────────────────────────────────────────┐
│              ContentPilot Pipeline               │
├─────────────────────────────────────────────────┤
│                                                   │
│  📝 Idea ──→ 🔍 Research ──→ ✍️ Write           │
│                                         │         │
│  📊 Score ◄── 🔍 Quality Gate ◄────────┘         │
│      │                                            │
│      ▼                                            │
│  🚀 Publish ──→ Blogger (draft/live)              │
│                                                   │
└─────────────────────────────────────────────────┘
```

**Quality Gate catches:**
- ❌ "Di era digital saat ini..." (AI-tells)
- ❌ "Sangat penting untuk..." (AI-tells)
- ❌ Dead links (404/410)
- ❌ Hoax domains
- ❌ Missing SEO fields
- ❌ Articles under 600 words

---

## Bring Your Own AI

ContentPilot works with any AI provider:

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

**No vendor lock-in. No API limits. Your data stays local with Ollama.**

---

## Commands

```bash
python3 scripts/pipeline.py status          # See all articles
python3 scripts/pipeline.py next            # Pick next topic
python3 scripts/pipeline.py research "topic" # Research phase
python3 scripts/pipeline.py draft <id>       # Write article
python3 scripts/pipeline.py gate <id>        # Quality check
python3 scripts/pipeline.py approve <id>     # Human approval
python3 scripts/pipeline.py push-draft <id>  # Publish to Blogger
```

---

## Perfect For

**🧑‍💻 Solo Bloggers** — Stop staring at blank pages. Let AI do the heavy lifting while you focus on your ideas.

**📝 Content Creators** — Publish 10x more content without sacrificing quality. Built-in quality gates ensure every post meets your standards.

**🏢 Agencies** — Standardize content workflow across clients. Same quality, same process, every time.

**📈 SEO Professionals** — Keyword research + writing + optimization in one pipeline. No more juggling 5 different tools.

---

## Quality That Competes

| Feature | ContentPilot | Manual | Jasper | Copy.ai |
|---------|:------------:|:------:|:------:|:-------:|
| AI Research | ✅ | ❌ | ⚠️ | ⚠️ |
| AI Writing | ✅ | ❌ | ✅ | ✅ |
| Quality Gates | ✅ | ❌ | ❌ | ❌ |
| Voice Guide | ✅ | ⚠️ | ⚠️ | ❌ |
| SEO Scoring | ✅ | ❌ | ⚠️ | ⚠️ |
| Publish to Blogger | ✅ | ❌ | ❌ | ❌ |
| Open Source | ✅ | — | ❌ | ❌ |
| Free Tier | ✅ | — | ❌ | ❌ |
| Local AI (Ollama) | ✅ | — | ❌ | ❌ |

---

## Installation

```bash
git clone https://github.com/bagasunix/content-pilot.git
cd content-pilot
pip install -r requirements.txt
```

**Requirements:** Python 3.10+, pip

**Optional:** Ollama (for free local AI), Google Cloud credentials (for Blogger publishing)

---

## License

MIT License — free for personal and commercial use.

---

<div align="center">

**ContentPilot** — From idea to published post in minutes.

[![GitHub stars](https://img.shields.io/github/stars/bagasunix/content-pilot?style=social)](https://github.com/bagasunix/content-pilot)
[![GitHub forks](https://img.shields.io/github/forks/bagasunix/content-pilot?style=social)](https://github.com/bagasunix/content-pilot)

</div>
