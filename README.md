# 🚀 ContentPilot

**Blog automation tool with full pipeline — from research to publish.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)

---

## ✨ Features

- **🔍 Smart Research** — AI-powered topic research with competitor analysis
- **✍️ AI Writing** — Generate content with any AI provider (BYOM)
- **📊 E-E-A-T Scoring** — Google-compliant content quality scoring
- **🎙️ Voice Guide** — AI analyzes your blog's writing style
- **📝 Cross-Platform** — Publish to Blogger & WordPress
- **🔍 Indexing Monitor** — Check & submit URLs to Google
- **⚡ Full Automation** — Research → Write → Optimize → Publish
- **🔒 BYOM** — Bring Your Own Model, your data stays yours

## 📦 Installation

### Requirements

- Python 3.10+
- PostgreSQL
- Redis (for Celery)

### Quick Start

```bash
# Clone repository
git clone https://github.com/bagasunix/contentpilot.git
cd contentpilot

# Install dependencies
pip install -r requirements.txt

# Setup database
psql -U postgres -d contentpilot -f schema.sql

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Run server
python central-server/app.py

# Run desktop app (optional)
python web/desktop.py
```

## 🔧 Configuration

### Environment Variables

```env
# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=contentpilot
DB_USER=contentpilot
DB_PASSWORD=your_password

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your_secret_key
ENCRYPTION_KEY=your_encryption_key

# AI Provider (optional)
AI_PROVIDER=openai
AI_API_KEY=your_api_key
AI_MODEL=gpt-4o-mini
```

### AI Provider Setup

ContentPilot supports any OpenAI-compatible API:

| Provider | Base URL | Notes |
|----------|----------|-------|
| OpenAI | https://api.openai.com/v1 | GPT-4, GPT-3.5 |
| DeepSeek | https://api.deepseek.com/v1 | Affordable |
| Ollama | http://localhost:11434/v1 | Local, free |
| OpenRouter | https://openrouter.ai/api/v1 | Multi-model |
| Custom | Your endpoint | Any OpenAI-compatible |

## 🚀 Usage

### Desktop App

```bash
python web/desktop.py
```

Opens native window with full dashboard.

### Web Interface

```bash
python central-server/app.py
# Open http://localhost:5000
```

### API Usage

```bash
# Run pipeline
curl -X POST http://localhost:5000/api/pipeline/run \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "blog_id": 1, "topic": "Python tutorials"}'

# Check E-E-A-T score
curl -X POST http://localhost:5000/api/eeat/score \
  -H "Content-Type: application/json" \
  -d '{"content": "Your article content here..."}'
```

## 📁 Project Structure

```
contentpilot/
├── central-server/           # Backend API
│   ├── app.py               # Flask application
│   ├── database.py          # PostgreSQL connection
│   ├── ai_provider.py       # AI integration
│   ├── adapters/
│   │   ├── wordpress.py     # WordPress adapter
│   │   └── blogger.py       # Blogger adapter
│   └── services/
│       ├── pipeline.py      # Full automation pipeline
│       ├── voice_guide.py   # Writing style analysis
│       ├── eeat_scorer.py   # E-E-A-T scoring
│       └── indexing.py      # Google indexing
├── client/                  # Frontend
│   ├── web/
│   │   ├── app.py          # Flask routes
│   │   ├── desktop.py      # PyWebView wrapper
│   │   └── templates/      # HTML templates
│   └── src/contentpilot/   # Domain logic
├── schema.sql              # Database schema
├── migrations/             # Database migrations
└── docs/                   # Documentation
```

## 🛠️ Tech Stack

- **Backend:** Python, Flask, Celery, PostgreSQL
- **Frontend:** HTML, Tailwind CSS, JavaScript
- **Desktop:** PyWebView + PyQt5
- **AI:** Any OpenAI-compatible API (BYOM)

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/pipeline/run` | POST | Run full pipeline |
| `/api/pipeline/status/<id>` | GET | Get pipeline status |
| `/api/eeat/score` | POST | Score article E-E-A-T |
| `/api/voice-guide/generate` | POST | Generate voice guide |
| `/api/indexing/check` | POST | Check URL indexing |
| `/api/indexing/submit` | POST | Submit URL for indexing |
| `/api/wordpress/publish` | POST | Publish to WordPress |

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Flask](https://flask.palletsprojects.com/) - Web framework
- [Tailwind CSS](https://tailwindcss.com/) - CSS framework
- [PyWebView](https://pywebview.flowrl.com/) - Desktop wrapper
- [PostgreSQL](https://www.postgresql.org/) - Database

---

**Built with ❤️ by [bagasunix](https://github.com/bagasunix)**
