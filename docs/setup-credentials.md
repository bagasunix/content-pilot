# Setup Credentials

Panduan setup credentials untuk ContentPilot.

---

## 1. Blogger OAuth (Wajib untuk publish)

### Buat Google Cloud Project
1. https://console.cloud.google.com → **New Project** (mis. "ContentPilot")
2. Enable **Blogger API v3**
3. **Credentials** → **Create Credentials** → **OAuth 2.0 Client ID**
4. Type: **Desktop App**
5. Download `credentials.json` → taruh di `workspace/credentials.json`

### Generate Token
```bash
contentpilot setup
```

Browser akan buka → login → authorize → token.json auto-saved.

### Token Refresh
Token auto-refresh oleh publisher.py. Kalau expired:
```bash
python3 -c "
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from pathlib import Path
c = Credentials.from_authorized_user_file('workspace/token.json')
c.refresh(Request())
Path('workspace/token.json').write_text(c.to_json())
print('Token refreshed')
"
```

## 2. AI Provider

### Ollama (Local, Free)
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull model
ollama pull llama2

# Config
# workspace/config.yaml:
# ai:
#   provider: ollama
#   model: llama2
```

### OpenAI (Paid)
```bash
# Get API key from https://platform.openai.com/api-keys

# Config
# workspace/config.yaml:
# ai:
#   provider: openai
#   model: gpt-4
#   api_key: sk-...
```

### DeepSeek (Paid, cheaper)
```bash
# Get API key from https://platform.deepseek.com

# Config
# workspace/config.yaml:
# ai:
#   provider: deepseek
#   model: deepseek-chat
#   api_key: sk-...
```

## 3. Google Search Console (Optional)

Untuk SEO monitoring:
1. https://search.google.com/search-console → Add property
2. Verify via DNS TXT record
3. Save verification tag di `workspace/config.yaml`:
```yaml
gsc:
  verification_tag: "your-tag-here"
```

## Checklist

- [ ] `workspace/credentials.json` ada (Blogger OAuth)
- [ ] `workspace/token.json` ada (auto-generated)
- [ ] AI provider configured di `workspace/config.yaml`
- [ ] `workspace/config.yaml` punya domain + blog_id
