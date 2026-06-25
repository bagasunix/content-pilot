# 📚 ContentPilot — Installation Guide

> Panduan lengkap install ContentPilot di Windows/Linux/Mac.

---

## 📋 Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **OS** | Windows 10 / Linux / Mac | Windows 11 / Ubuntu 22.04 / Mac latest |
| **Python** | 3.10+ | 3.11+ |
| **RAM** | 4 GB | 8 GB |
| **Disk** | 500 MB | 1 GB |
| **Internet** | Required | Stable connection |

---

## 🚀 Installation

### Step 1: Clone Repository

```bash
git clone https://github.com/bagasunix/contentpilot.git
cd contentpilot/standalone
```

### Step 2: Install Dependencies

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install requirements
pip install -r requirements.txt flask
```

### Step 3: Run Setup Wizard

```bash
python3 scripts/setup.py
```

Follow the wizard:
1. Enter your blog domain
2. Enter Blogger Blog ID
3. Choose AI provider (OpenAI/DeepSeek/Ollama)
4. Enter your AI API key

### Step 4: Activate License

```bash
python3 scripts/activate.py --key SB-XXXX-XXXX-XXXX
```

### Step 5: Start Web UI

```bash
./start.sh
# or
python3 web/app.py
```

Open browser: `http://localhost:8080`

---

## 🖥️ Platform-Specific Instructions

### Windows

```powershell
# Open PowerShell as Administrator
cd C:\path\to\contentpilot\standalone

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt flask

# Run setup
python scripts\setup.py

# Start server
python web\app.py
```

### Linux (Ubuntu/Debian)

```bash
# Install Python if not installed
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Navigate to project
cd ~/contentpilot/standalone

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt flask

# Run setup
python3 scripts/setup.py

# Start server
./start.sh
```

### Mac

```bash
# Install Homebrew if not installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python

# Navigate to project
cd ~/contentpilot/standalone

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt flask

# Run setup
python3 scripts/setup.py

# Start server
./start.sh
```

---

## 🔧 Configuration

### config/config.yaml

```yaml
domain: "yourblog.com"
blog_id: "1234567890"

ai:
  provider: openai  # openai | deepseek | ollama
  model: gpt-4
  api_key: "sk-your-api-key"

pipeline:
  wip_limit: 3
  publish_mode: draft
```

### Environment Variables

```bash
# Optional: Set API key via environment
export OPENAI_API_KEY="sk-your-key"
export DEEPSEEK_API_KEY="your-key"
```

---

## 🧪 Verify Installation

```bash
# Check status
python3 -m blog.pipeline status

# Test AI connection
python3 -c "from blog.pipeline import create_provider; p = create_provider(); print('AI OK')"
```

---

## ❓ Troubleshooting

### "Python not found"
```bash
# Check Python version
python3 --version

# If not installed:
# Windows: Download from python.org
# Linux: sudo apt install python3
# Mac: brew install python
```

### "Module not found"
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows

# Reinstall dependencies
pip install -r requirements.txt flask
```

### "License key invalid"
```bash
# Check key format (should be SB-XXXX-XXXX-XXXX)
python3 scripts/activate.py --check

# Get new key at: https://smartblogger.dev/free
```

### "AI API error"
```bash
# Check API key is valid
# OpenAI: https://platform.openai.com/api-keys
# DeepSeek: https://platform.deepseek.com/api_keys

# Test connection
python3 -c "
import requests
r = requests.get('https://api.openai.com/v1/models', headers={'Authorization': 'Bearer sk-your-key'})
print(r.status_code)
"
```

---

## 📞 Support

- **Documentation**: https://docs.smartblogger.dev
- **GitHub Issues**: https://github.com/bagasunix/contentpilot/issues
- **Email**: support@smartblogger.dev

---

## 📝 License

MIT License
