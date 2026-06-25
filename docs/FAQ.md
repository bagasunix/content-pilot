# 📚 ContentPilot — FAQ

> Frequently Asked Questions tentang ContentPilot.

---

## 🔧 Umum

### Q: Apa itu ContentPilot?

A: ContentPilot adalah tool blog automation yang menggunakan AI untuk:
- Riset topik & keyword
- Tulis artikel SEO-friendly
- Review otomatis
- Publish ke Blogger

### Q: Berapa harganya?

A: | Tier | Harga | Features |
|------|-------|----------|
| Free | $0 | 10 articles/month |
| Pro | $29/bulan | Unlimited |
| Business | $99/bulan | Unlimited + Priority |

### Q: Bisa dipakai di Windows/Linux/Mac?

A: Ya! ContentPilot cross-platform. Butuh Python 3.10+.

### Q: Butuh internet?

A: Ya. ContentPilot butuh internet untuk:
- Validasi license
- Call AI API
- Publish ke Blogger

---

## 🤖 AI Provider

### Q: AI provider apa yang didukung?

A: | Provider | Model | Cost |
|----------|-------|------|
| OpenAI | GPT-4, GPT-3.5 | Paid |
| DeepSeek | DeepSeek Chat | Paid |
| Ollama | Llama2, Mistral | Free (local) |

### Q: Berapa biaya AI usage?

A: Tergantung provider:
- OpenAI GPT-4: ~$0.03-0.10/artikel
- DeepSeek: ~$0.01-0.03/artikel
- Ollama: Gratis (local)

### Q: Bisa pakai AI local (offline)?

A: Ya! Pakai Ollama. Install dari https://ollama.ai

### Q: Ganti AI provider gimana?

A: Buka Settings → ubah provider → masukkan API key baru → Save.

---

## 📝 Pipeline

### Q: Berapa lama proses 1 artikel?

A: Tergantung AI provider:
- OpenAI GPT-4: ~2-5 menit
- DeepSeek: ~1-3 menit
- Ollama: ~5-10 menit (tergantung hardware)

### Q: Bisa batch generate?

A: Ya! Gunakan CLI:
```bash
contentpilot research "topik1"
contentpilot research "topik2"
contentpilot research "topik3"
```

### Q: Hasil artikel jelek gimana?

A: Coba:
1. Ganti model AI (GPT-4 lebih bagus)
2. Update voice guide
3. Review manual sebelum publish
4. Kasih feedback ke AI

### Q: Bisa custom voice/tone?

A: Ya! Edit `workspace/voice.md` untuk customize writing style.

---

## 🔑 License

### Q: Gimana cara dapat license key?

A: 
1. Buka https://contentpilot.dev/free
2. Masukkan email
3. Dapatkan key via email

### Q: Key invalid gimana?

A: 
1. Cek format: `SB-XXXX-XXXX-XXXX`
2. Cek status: `contentpilot license`
3. Hubungi support jika masih error

### Q: Bisa dipakai di multiple machine?

A: Free tier: 1 machine. Pro: 3 machines. Business: Unlimited.

### Q: Expired gimana?

A: 
1. Hubungi support untuk perpanjang
2. Atau beli subscription baru

---

## 🌐 Publish

### Q: Platform apa yang didukung?

A: Saat ini: **Blogger** (Google). Update: Social media (TikTok, Instagram, YouTube).

### Q: Gimana cara setup Blogger?

A: 
1. Buat Google Cloud Project
2. Enable Blogger API v3
3. Buat OAuth credentials
4. Jalankan: `contentpilot setup`

### Q: Bisa auto-publish?

A: Ya! Set `publish_mode: live` di config. Tapi disarankan pakai `draft` dulu.

### Q: Bisa schedule publish?

A: Belum. Fitur ini dalam roadmap.

---

## 🛠️ Troubleshooting

### Q: Error "Python not found"

A: Install Python 3.10+ dari https://python.org

### Q: Error "Module not found"

A: 
```bash
source venv/bin/activate
pip install -r requirements.txt flask
```

### Q: Error "License key invalid"

A: Cek format key dan pastikan tidak ada spasi.

### Q: Error "AI API error"

A: 
1. Cek API key valid
2. Cek koneksi internet
3. Cek rate limit

### Q: Error "Publish failed"

A: 
1. Cek OAuth token
2. Re-setup credentials
3. Cek koneksi internet

---

## 💡 Tips

### Q: Gimana cara dapat artikel bagus?

A: 
1. Riset topik dengan baik
2. Kasih angle yang unik
3. Review manual sebelum publish
4. Pakai voice guide yang konsisten

### Q: Gimana cara hemat AI cost?

A: 
1. Pakai DeepSeek (lebih murah)
2. Pakai Ollama (gratis)
3. Batch generate
4. Review manual, jangan regenerate terus

### Q: Gimana cara scale?

A: 
1. Upgrade ke Pro/Business tier
2. Pakai multiple API keys
3. Automate dengan cron job
4. Gunakan analytics untuk optimasi

---

## 📞 Masih ada pertanyaan?

- **Documentation**: https://docs.contentpilot.dev
- **GitHub Issues**: https://github.com/bagasunix/contentpilot/issues
- **Email**: support@contentpilot.dev

---

## 📝 License

MIT License
