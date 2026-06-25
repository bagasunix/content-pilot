# 📚 ContentPilot — User Manual

> Panduan lengkap pakai ContentPilot.

---

## 🎯 Overview

ContentPilot adalah tool blog automation yang membantu kamu:
- **Riset topik** — AI carikan keyword & competitor
- **Tulis artikel** — AI generate konten SEO-friendly
- **Review otomatis** — Quality gate cek AI-tells
- **Publish langsung** — Auto-post ke Blogger

---

## 🚀 Quick Start

### 1. Buka Dashboard

```bash
./start.sh
# Buka http://localhost:8080
```

### 2. Activate License

1. Buka halaman activation
2. Masukkan license key: `SB-XXXX-XXXX-XXXX`
3. Klik "Activate License"

### 3. Setup AI Provider

1. Buka Settings
2. Pilih AI provider (OpenAI/DeepSeek/Ollama)
3. Masukkan API key
4. Klik "Save Settings"

### 4. Buat Artikel Pertama

1. Klik "New Article" di dashboard
2. Masukkan topik (misal: "cara install docker")
3. Klik "Start Research"
4. Tunggu proses selesai

---

## 📝 Pipeline Flow

```
1. Research    → AI riset keyword & competitor
2. Write       → AI tulis artikel
3. Review      → Review otomatis
4. Gate        → Quality check
5. Publish     → Publish ke Blogger
```

### Status Artikel

| Status | Artinya |
|--------|---------|
| **researching** | Sedang riset |
| **drafted** | Sudah jadi draft |
| **reviewing** | Sedang di-review |
| **gated** | Lolos quality gate |
| **published** | Sudah di-publish |

---

## ⚙️ Settings

### Domain

```yaml
domain: "yourblog.com"
```

### AI Provider

```yaml
ai:
  provider: openai  # openai | deepseek | ollama
  model: gpt-4
  api_key: "***"
```

### Pipeline

```yaml
pipeline:
  wip_limit: 3      # Max artikel in-flight
  publish_mode: draft  # draft | live
```

---

## 📊 Dashboard

### Stats

- **Total Articles** — Jumlah artikel yang sudah dibuat
- **In Progress** — Artikel yang sedang dikerjakan
- **Published** — Artikel yang sudah di-publish

### Quick Actions

- **New Article** — Mulai artikel baru
- **View Articles** — Lihat semua artikel
- **Settings** — Pengaturan

---

## 🤖 AI Providers

### OpenAI

1. Daftar di https://platform.openai.com
2. Buat API key
3. Masukkan di Settings

**Model yang tersedia:**
- `gpt-4` — Best quality
- `gpt-3.5-turbo` — Faster, cheaper

### DeepSeek

1. Daftar di https://platform.deepseek.com
2. Buat API key
3. Masukkan di Settings

**Model yang tersedia:**
- `deepseek-chat` — General purpose
- `deepseek-coder` — Code-focused

### Ollama (Local)

1. Install Ollama: https://ollama.ai
2. Jalankan: `ollama serve`
3. Pilih model di Settings

**Model yang tersedia:**
- `llama2` — General purpose
- `mistral` — Fast & efficient
- `codellama` — Code-focused

---

## 🔧 Commands Reference

### CLI Commands

```bash
# Status
python3 -m blog.pipeline status

# Research
python3 -m blog.pipeline research "topik anda"

# Draft
python3 -m blog.pipeline draft "topik-slug"

# Review
python3 -m blog.pipeline review "topik-slug"

# Gate
python3 -m blog.pipeline gate "topik-slug"

# Approve
python3 -m blog.pipeline approve "topik-slug"

# Publish
python3 -m blog.pipeline publish "topik-slug"
```

### Web UI

Buka `http://localhost:8080` di browser.

---

## 📈 Analytics (Addon)

### Install Analytics Addon

```bash
cp -r analytics-addon/skills/* skills/
cp -r analytics-addon/docs/* workspace/docs/
python3 analytics-addon/scripts/setup_analytics.py
```

### Features

- **GA4 Integration** — Track pageviews
- **GSC Integration** — Monitor search performance
- **Weekly Reports** — Automated reports

---

## 📣 Promotion (Addon)

### Install Promotion Addon

```bash
cp -r promotion-addon/skills/* skills/
```

### Features

- **Social Media Auto-Post** — TikTok, Instagram, YouTube
- **Content Recycling** — Repurpose articles
- **Analytics Tracking** — Track performance

---

## ❓ FAQ

### Q: Berapa biaya AI usage?

A: Tergantung provider dan model:
- OpenAI GPT-4: ~$0.03-0.10 per artikel
- DeepSeek: ~$0.01-0.03 per artikel
- Ollama: Gratis (local)

### Q: Bisa offline?

A: Tidak bisa. ContentPilot butuh internet untuk:
- Validasi license
- Call AI API
- Publish ke Blogger

### Q: Ganti AI provider?

A: Buka Settings → ubah provider → masukkan API key baru → Save.

### Q: Artikel gagal publish?

A: Cek:
1. OAuth token valid (run `setup_credentials.py`)
2. Blog ID benar
3. Koneksi internet stabil

### Q: Hasil artikel jelek?

A: Coba:
1. Ganti model AI (gpt-4 lebih bagus)
2. Update voice guide
3. Review manual sebelum publish

---

## 📞 Support

- **Documentation**: https://docs.smartblogger.dev
- **GitHub Issues**: https://github.com/bagasunix/contentpilot/issues
- **Email**: support@smartblogger.dev

---

## 📝 License

MIT License
