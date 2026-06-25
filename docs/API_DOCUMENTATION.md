# 📚 ContentPilot — API Documentation

> API documentation untuk ContentPilot Central Server.

---

## 🔗 Base URL

```
https://api.smartblogger.dev
```

---

## 🔐 Authentication

### License Key Validation

```bash
curl -X POST https://api.smartblogger.dev/api/validate \
  -H "Content-Type: application/json" \
  -d '{"key": "SB-XXXX-XXXX-XXXX", "machine_id": "abc123"}'
```

**Response:**
```json
{
  "valid": true,
  "tier": "pro",
  "expires_at": "2025-12-31T00:00:00"
}
```

### License Activation

```bash
curl -X POST https://api.smartblogger.dev/api/activate \
  -H "Content-Type: application/json" \
  -d '{"key": "SB-XXXX-XXXX-XXXX", "machine_id": "abc123"}'
```

**Response:**
```json
{
  "success": true,
  "message": "License activated"
}
```

---

## 📊 Usage Tracking

### Track Event

```bash
curl -X POST https://api.smartblogger.dev/api/track \
  -H "Content-Type: application/json" \
  -d '{"key": "SB-XXXX-XXXX-XXXX", "event": {"type": "research"}}'
```

### Get Usage Stats

```bash
curl https://api.smartblogger.dev/api/usage/SB-XXXX-XXXX-XXXX
```

**Response:**
```json
{
  "stats": {
    "articles": 15,
    "research": 20
  }
}
```

---

## 🔄 Updates

### Check for Updates

```bash
curl https://api.smartblogger.dev/api/updates?version=1.0.0
```

**Response:**
```json
{
  "update_available": true,
  "current_version": "1.0.0",
  "latest_version": "1.1.0",
  "download_url": "https://github.com/bagasunix/contentpilot/releases"
}
```

### Get Changelog

```bash
curl https://api.smartblogger.dev/api/changelog
```

---

## 🎫 Support

### Submit Ticket

```bash
curl -X POST https://api.smartblogger.dev/api/support \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "subject": "Help with installation",
    "message": "I cannot activate my license",
    "license_key": "SB-XXXX-XXXX-XXXX"
  }'
```

**Response:**
```json
{
  "success": true,
  "ticket": {
    "id": "SUP-A1B2C3D4",
    "status": "open",
    "created_at": "2024-06-25T10:00:00"
  }
}
```

---

## 📈 Statistics (Admin)

### Get Overall Stats

```bash
curl -H "X-API-Key: your-admin-key" https://api.smartblogger.dev/api/stats
```

**Response:**
```json
{
  "total_users": 1234,
  "active_users": 890,
  "total_articles": 5678,
  "tiers": {
    "free": 800,
    "pro": 400,
    "business": 34
  }
}
```

---

## ⚠️ Rate Limits

| Endpoint | Limit |
|----------|-------|
| `/api/validate` | 30/minute |
| `/api/activate` | 10/hour |
| `/api/track` | 100/hour |
| `/api/support` | 5/hour |
| `/api/updates` | Unlimited |

---

## ❌ Error Codes

| Code | Message | Solution |
|------|---------|----------|
| 400 | Missing required field | Check request body |
| 401 | Invalid API key | Check X-API-Key header |
| 404 | License not found | Check license key |
| 429 | Rate limit exceeded | Wait and retry |
| 500 | Server error | Contact support |

---

## 📝 License

MIT License
