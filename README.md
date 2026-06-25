# ✨ ContentPilot

> **Blog automation yang bikin kamu produktif 10x lipat.**
> 
> Research → Write → Review → Publish — semuanya otomatis pakai AI.

---

## 🚀 Apa Itu ContentPilot?

ContentPilot adalah tool blog automation yang membantu kamu:

- **Riset topik** — AI carikan keyword, competitor, dan angle terbaik
- **Tulis artikel** — AI generate konten yang engaging dan SEO-friendly
- **Review otomatis** — Quality gate cek AI-tells, SEO, word count
- **Publish langsung** — Auto-post ke Blogger (draft/live mode)

**Tanpa ribet, tanpa coding, tanpa Hermes dependency.**

---

## 🎯 Kenapa ContentPilot?

### ❌ Masalah yang Sering Terjadi

| Masalah | Solusi |
|---------|--------|
| Bingung mau nulis apa | AI riset topik + keyword untuk kamu |
| Artikel terlihat "AI-generated" | Quality gate deteksi & fix AI-tells |
| SEO-nya jelek | Auto-score SEO 0-100 + rekomendasi |
| Publish manual satu-satu | Auto-publish ke Blogger |
| Proses lama & ribet | Pipeline 5 langkah, fully automated |

### ✅ Yang Kamu Dapat

| Fitur | Benefit |
|-------|---------|
| **AI Research** | Topik relevan + keyword volume |
| **AI Writing** | Artikel 600+ kata, SEO-optimized |
| **Quality Gates** | 19 AI-tell checks, link validation |
| **Voice Guide** | Konsisten, natural, bukan robot |
| **Auto Publish** | Langsung ke Blogger, draft/live mode |

---

## 📦 Quick Start (3 Menit!)

### 1. Install

```bash
git clone https://github.com/bagasunix/contentpilot.git
cd contentpilot
pip install -r requirements.txt
```

### 2. Setup

```bash
python3 scripts/setup.py
```

Ikuti wizard:
- Masukkan domain blog
- Pilih AI provider (OpenAI/DeepSeek/Ollama)
- Masukkan API key

### 3. Jalankan!

```bash
# Cek status
python3 -m blog.pipeline status

# Mulai riset
python3 -m blog.pipeline research "cara install docker"

# Lihat hasilnya
ls workspace/drafts/
```

**Selesai! 🎉**

---

## 🔄 How It Works

```
┌─────────────────────────────────────────────────────────────┐
│                    SMART BLOGGER PIPELINE                     │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  1️⃣ RESEARCH                                                  │
│     └─ AI carikan: keyword, competitor, angle                 │
│                                                               │
│  2️⃣ WRITE                                                     │
│     └─ AI tulis artikel: 600+ kata, SEO-optimized            │
│                                                               │
│  3️⃣ REVIEW                                                    │
│     └─ Quality gate: AI-tells, word count, links              │
│                                                               │
│  4️⃣ GATE                                                      │
│     └─ Auto-score SEO 0-100, rekomendasi perbaikan           │
│                                                               │
│  5️⃣ PUBLISH                                                   │
│     └─ Auto-post ke Blogger (draft/live mode)                 │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 🤖 AI Providers

Pilih AI provider yang kamu suka:

### OpenAI (GPT-4)
```yaml
ai:
  provider: openai
  model: gpt-4
  api_key: "sk-..."
```

### DeepSeek
```yaml
ai:
  provider: deepseek
  model: deepseek-chat
  api_key: "..."
```

### Ollama (Local — Gratis!)
```yaml
ai:
  provider: ollama
  model: llama2
  base_url: "http://localhost:11434"
```

---

## 📊 Quality Gates

ContentPilot otomatis cek:

| Check | Description |
|-------|-------------|
| ✅ Word Count | Minimal 600 kata |
| ✅ SEO Fields | Title, meta, slug, keywords |
| ✅ AI-Tells | 19 phrases terdeteksi & dihapus |
| ✅ Link Validation | No hoax/dead links |
| ✅ Voice Consistency | Tone konsisten, natural |

**Contoh AI-Tells yang Dicegah:**
- ❌ "Di era digital saat ini..."
- ❌ "Sangat penting untuk..."
- ❌ "Tidak dapat dipungkiri..."
- ❌ "Perlu diketahui..."

---

## 🎨 Fitur Lengkap

### Research
- Keyword research otomatis
- Competitor analysis
- Content angle suggestion
- Search volume estimate

### Writing
- AI-powered content generation
- Voice guide untuk konsistensi
- Template berbagai jenis artikel
- Internal linking otomatis

### Review
- SEO scoring (0-100)
- Readability check
- Fact-check suggestion
- Improvement recommendation

### Publishing
- Auto-publish ke Blogger
- Draft/live mode
- Featured image upload
- Schedule publishing

---

## 📁 Project Structure

```
contentpilot/
├── blog/                    # Core pipeline code
│   ├── __init__.py
│   └── pipeline.py         # Main pipeline logic
├── scripts/
│   └── setup.py            # Setup wizard
├── config/
│   └── config.yaml         # Configuration
├── workspace/
│   ├── drafts/             # Generated articles
│   ├── published/          # Published articles
│   └── journal.jsonl       # Activity log
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

## ⚙️ Configuration

Edit `config/config.yaml`:

```yaml
# Blog settings
domain: "myblog.com"
blog_id: "1234567890"

# AI provider
ai:
  provider: openai  # openai | deepseek | ollama
  model: gpt-4
  api_key: "sk-..."

# Pipeline settings
pipeline:
  wip_limit: 3
  publish_mode: draft
```

---

## 🛠️ Commands Reference

```bash
# Status
python3 -m blog.pipeline status

# Research
python3 -m blog.pipeline research "topik anda"

# Draft
python3 -m blog.pipeline draft "topik-slug"

# Review
python3 -m blog.pipeline review "topik-slug"

# Quality Gate
python3 -m blog.pipeline gate "topik-slug"

# Approve
python3 -m blog.pipeline approve "topik-slug"

# Publish
python3 -m blog.pipeline publish "topik-slug"
```

---

## 💡 Use Cases

### 🎯 Blogger Pemula
- Tidak perlu paham SEO
- AI bantu riset & tulis
- Quality gate jaga kualitas

### 🏢 Content Creator
- Produksi konten massal
- Konsisten dengan brand voice
- Auto-publish hemat waktu

### 📈 SEO Specialist
- Keyword research otomatis
- SEO scoring real-time
- Competitor analysis built-in

### 💼 Agency/ Freelancer
- Kelola banyak blog sekaligus
- Workflow terstandarisasi
- Quality assurance otomatis

---

## 🆚 Comparison

| Fitur | ContentPilot | Manual | Tool Lain |
|-------|---------------|--------|-----------|
| AI Research | ✅ | ❌ | ⚠️ Limited |
| AI Writing | ✅ | ❌ | ✅ |
| Quality Gates | ✅ | ❌ | ❌ |
| Voice Guide | ✅ | ⚠️ | ❌ |
| Auto Publish | ✅ | ❌ | ✅ |
| SEO Scoring | ✅ | ❌ | ⚠️ |
| Open Source | ✅ | - | ❌ |
| Free | ✅ | - | ❌ |

---

## 🤝 Contributing

Contributions welcome! Lihat `CONTRIBUTING.md` untuk details.

---

## 📝 License

MIT License — gratis untuk personal & commercial use.

---

## 🙏 Credits

Dibuat dengan ❤️ oleh [BagasUnix](https://github.com/bagasunix)

---

<div align="center">

**ContentPilot** — Blog automation yang bikin kamu produktif 10x lipat.

[![GitHub stars](https://img.shields.io/github/stars/bagasunix/contentpilot?style=social)](https://github.com/bagasunix/contentpilot)
[![GitHub forks](https://img.shields.io/github/forks/bagasunix/contentpilot?style=social)](https://github.com/bagasunix/contentpilot)
[![GitHub issues](https://img.shields.io/github/issues/bagasunix/contentpilot)](https://github.com/bagasunix/contentpilot/issues)

</div>

## 🔑 License Activation

ContentPilot membutuhkan license key untuk digunakan.

### Get Free Key

1. Buka https://smartblogger.dev/free
2. Masukkan email kamu
3. Dapatkan license key via email

### Activate

```bash
# During setup
python3 scripts/setup.py

# Or manually
python3 scripts/activate.py --key SB-XXXX-XXXX-XXXX
```

### Check Status

```bash
python3 scripts/activate.py --check
```

## 💰 Pricing

| Tier | Price | Articles | Features |
|------|-------|----------|----------|
| **Free** | $0 | 10/month | Basic pipeline |
| **Pro** | $29/month | Unlimited | + Analytics, Auto publish |
| **Business** | $99/month | Unlimited | + Priority support, Multi-blog |

### Upgrade

```bash
# Upgrade to Pro
python3 scripts/activate.py --key PRO-KEY-HERE

# Upgrade to Business
python3 scripts/activate.py --key BIZ-KEY-HERE
```

