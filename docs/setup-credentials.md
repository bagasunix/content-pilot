# Setup Credentials

Panduan setup credentials untuk ContentPilot.

---

## 1. Blogger OAuth (Wajib untuk publish)

### Buat Google Cloud Project
1. https://console.cloud.google.com → **New Project** (mis. "ContentPilot")
2. Enable **Blogger API v3**
3. **Credentials** → **Create Credentials** → **OAuth 2.0 Client ID**
4. Type: **Web application**
5. **Authorized redirect URIs** → tambahkan:
   - `http://127.0.0.1:8080/oauth2/callback`
   - `http://localhost:8080/oauth2/callback`
6. Sediakan kredensialnya dengan salah satu cara:
   - Set env `GOOGLE_CLIENT_ID` dan `GOOGLE_CLIENT_SECRET`, **atau**
   - Download `credentials.json` → taruh di `workspace/credentials.json`

### Connect (Generate Token)
Buka aplikasi desktop → **Settings → Google / Blogger → Connect Google**.
Consent terbuka di browser sistem; setelah approve, token tersimpan otomatis
di `workspace/token.json` dan status berubah jadi **Connected**.

> Catatan: token disimpan apa adanya (raw, termasuk `refresh_token`). Auto-refresh
> saat publish belum diwire — itu langkah lanjutan yang terpisah.

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
