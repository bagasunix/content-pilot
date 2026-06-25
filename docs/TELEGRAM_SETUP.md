# Telegram Notification Setup

> Setup notifikasi Telegram untuk Blog Lifecycle Pro.

## Kenapa Telegram?

- **Gratis** — gak perlu bayar
- **Real-time** — notifikasi langsung sampai
- **Rich media** — support HTML formatting
- **Populer** — banyak user di Indonesia

## Step 1: Buat Bot Telegram

1. Buka Telegram, cari **@BotFather**
2. Ketik `/newbot`
3. Isi nama bot (contoh: `MyBlogNotifier`)
4. Isi username bot (contoh: `myblognotify_bot`)
5. Simpan **bot token** yang diberikan

```
Contoh bot token:
1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
```

## Step 2: Dapatkan Chat ID

### Cara 1: Manual
1. Buka bot yang baru dibuat
2. Ketik `/start`
3. Buka URL ini di browser:
```
https://api.telegram.org/bot<BOT_TOKEN>/getUpdates
```
4. Cari `"chat":{"id":` — itu chat ID Anda

### Cara 2: Pakai Bot Lain
1. Cari **@userinfobot** di Telegram
2. Ketik `/start`
3. Bot akan memberikan chat ID Anda

## Step 3: Config

Edit `workspace/config.yaml`:

```yaml
notifications:
  telegram:
    enabled: true
    bot_token: "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
    chat_id: "987654321"
```

## Step 4: Test

```bash
# Jalankan test
python3 scripts/telegram_notify.py test

# Atau manual
python3 -c "
from scripts.telegram_notify import TelegramNotifier
n = TelegramNotifier('BOT_TOKEN', 'CHAT_ID')
n.send('✅ Blog Lifecycle Pro connected!')
"
```

## Notifikasi yang Dikirim

| Event | Notifikasi |
|-------|------------|
| Draft dibuat | "Draft Dibuat: [judul]" |
| Review selesai | "Artikel Siap: [judul], Score: 85/100" |
| Gate pass/fail | "Quality Gate: PASS/FAIL" |
| Error | "Error: [pesan error]" |
| Daily summary | "WIP: 2/3, Published: 5" |

## Troubleshooting

### Bot gak kirim pesan

1. Cek bot token benar
2. Cek chat ID benar
3. Pastikan sudah `/start` ke bot
4. Test manual:
```bash
curl "https://api.telegram.org/bot<BOT_TOKEN>/getMe"
```

### Pesan error format

Cek parse_mode. Default HTML. Bisa ganti ke Markdown:
```python
n.send("*bold text*", parse_mode="Markdown")
```

### Rate limit

Telegram limit: 30 pesan per detik ke chat yang sama. Plugin otomatis handle.

## Contoh Notifikasi

```
✅ Artikel Siap

📝 Cara Install Docker di Ubuntu 24.04
📊 Score: 85/100
🆔 docker-install-ubuntu

Jalankan: python3 scripts/pipeline.py approve docker-install-ubuntu
```

## Advanced: Custom Notifikasi

```python
from scripts.telegram_notify import TelegramNotifier

# Load dari config
n = load_notifier()

# Kirim custom
n.send("🎯 Custom notification!")

# Kirim dengan Markdown
n.send("*Bold* and _italic_", parse_mode="Markdown")
```

## Support

- Telegram: @YourSupportBot
- Email: support@bloglifecyclepro.com
