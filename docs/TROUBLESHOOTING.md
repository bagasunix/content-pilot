# 📚 ContentPilot — Troubleshooting Guide

> Panduan mengatasi masalah umum ContentPilot.

---

## 🔧 Installation Issues

### "Python not found"

**Masalah:** Command `python3` tidak dikenali.

**Solusi:**
```bash
# Check Python version
python3 --version

# Windows: Download dari python.org
# Linux: sudo apt install python3
# Mac: brew install python
```

### "Module not found: flask"

**Masalah:** Flask belum terinstall.

**Solusi:**
```bash
# Aktifkan virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows

# Install Flask
pip install flask
```

### "Permission denied"

**Masalah:** Tidak punya akses tulis.

**Solusi:**
```bash
# Linux/Mac: gunakan sudo (hati-hati)
sudo python3 scripts/setup.py

# Atau buat virtual environment di folder user
python3 -m venv ~/venvs/smartblogger
```

---

## 🔑 License Issues

### "License key invalid"

**Masalah:** Key tidak dikenali.

**Solusi:**
1. Cek format key: `SB-XXXX-XXXX-XXXX`
2. Pastikan tidak ada spasi
3. Cek status: `python3 scripts/activate.py --check`
4. Dapatkan key baru: https://smartblogger.dev/free

### "License already activated"

**Masalah:** Key sudah dipakai di machine lain.

**Solusi:**
1. Hubungi support untuk reset
2. Atau gunakan key baru

### "License expired"

**Masalah:** Key sudah kedaluwarsa.

**Solusi:**
1. Hubungi support untuk perpanjang
2. Atau beli subscription baru

---

## 🤖 AI Provider Issues

### "OpenAI API error"

**Masalah:** Koneksi ke OpenAI gagal.

**Solusi:**
```bash
# 1. Cek API key valid
curl -s https://api.openai.com/v1/models \
  -H "Authorization: Bearer sk-your-key"

# 2. Cek koneksi internet
ping api.openai.com

# 3. Cek rate limit
# Tunggu beberapa menit lalu coba lagi
```

### "DeepSeek API error"

**Masalah:** Koneksi ke DeepSeek gagal.

**Solusi:**
```bash
# 1. Cek API key
curl -s https://api.deepseek.com/v1/models \
  -H "Authorization: Bearer sk-your-key"

# 2. Cek saldo
# Login ke platform.deepseek.com
```

### "Ollama not running"

**Masalah:** Ollama server tidak aktif.

**Solusi:**
```bash
# Start Ollama
ollama serve

# Cek status
curl http://localhost:11434/api/tags
```

### "Model not found"

**Masalah:** Model AI tidak tersedia.

**Solusi:**
```bash
# OpenAI: cek model yang tersedia
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer sk-your-key"

# Ollama: download model
ollama pull llama2
```

---

## 📝 Pipeline Issues

### "WIP limit reached"

**Masalah:** Terlalu banyak artikel in-progress.

**Solusi:**
```bash
# Cek status
python3 -m blog.pipeline status

# Selesaikan atau hapus artikel yang stuck
python3 -m blog.pipeline approve <idea_id>
```

### "Draft not found"

**Masalah:** File draft tidak ada.

**Solusi:**
```bash
# Cek workspace/drafts/
ls workspace/drafts/

# Jika tidak ada, jalankan research lagi
python3 -m blog.pipeline research "topik"
```

### "Gate failed"

**Masalah:** Artikel tidak lolos quality gate.

**Solusi:**
1. Cek AI-tells: `grep -i "di era digital" workspace/drafts/*/draft.md`
2. Cek word count: minimal 600 kata
3. Cek SEO fields: title, meta, slug, keywords
4. Cek featured image

### "Publish failed"

**Masalah:** Gagal publish ke Blogger.

**Solusi:**
```bash
# 1. Cek OAuth token
ls -la workspace/token.json

# 2. Re-setup credentials
python3 scripts/setup_credentials.py

# 3. Cek koneksi internet
curl https://www.blogger.com
```

---

## 🌐 Network Issues

### "Connection timeout"

**Masalah:** Koneksi ke server lambat.

**Solusi:**
1. Cek koneksi internet
2. Gunakan VPN jika perlu
3. Coba lagi beberapa menit kemudian

### "SSL certificate error"

**Masalah:** Sertifikat SSL tidak valid.

**Solusi:**
```bash
# Update CA certificates
sudo apt update && sudo apt install ca-certificates

# Atau skip SSL (tidak disarankan)
export PYTHONHTTPSVERIFY=0
```

---

## 🖥️ Platform Issues

### Windows

**Path issues:**
```bash
# Gunakan forward slash
python3 scripts/setup.py  # ✅
python3 scripts\setup.py  # ❌

# Atau gunakan raw string
python3 r"scripts\setup.py"  # ✅
```

### Linux

**Permission issues:**
```bash
# Buat executable
chmod +x start.sh

# Jalankan
./start.sh
```

### Mac

**Gatekeeper issues:**
```bash
# Jika Python diblock
xattr -d com.apple.quarantine /usr/local/bin/python3
```

---

## 📞 Support

Jika masalah belum teratasi:

1. **Cek Documentation**: https://docs.smartblogger.dev
2. **GitHub Issues**: https://github.com/bagasunix/contentpilot/issues
3. **Email**: support@smartblogger.dev

**Sertakan info:**
- OS & versi
- Python versi
- Error message lengkap
- Langkah yang sudah dicoba

---

## 📝 License

MIT License
