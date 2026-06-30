# Setup Credentials

Panduan setup credentials untuk ContentPilot.

---

## 1. Blogger OAuth (Wajib untuk publish)

### Setup (Server-Side)
Google OAuth sekarang ditangani sepenuhnya oleh server. Tidak perlu lagi
membuat Cloud Project atau mengunduh `credentials.json` sendiri.

### Connect Google
1. Buka aplikasi desktop → **Settings → Google / Blogger**
2. Klik **Connect Google**
3. Browser terbuka → login & approve consent
4. Token disimpan otomatis di server (database `google_tokens`)
5. Status berubah jadi **Connected**

### Bagaimana cara kerjanya
- OAuth client (`credentials.json`) sudah disediakan di server
- Token disimpan per-user di database (keyed by `license_key`)
- Token refresh otomatis (via `google-auth` library)
- Client tidak menyimpan credential — semua di-proxy ke server

### Disconnect
Settings → Google / Blogger → **Disconnect**. Token dihapus dari server.

> Catatan: Tidak perlu `workspace/credentials.json` atau `workspace/token.json` lagi.
> Semua credential ditangani server-side.

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

- [ ] Google account connected (Settings → Connect Google)
- [ ] AI provider configured di `workspace/config.yaml`
- [ ] `workspace/config.yaml` punya domain + blog_id
