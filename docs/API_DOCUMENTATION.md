# 📚 ContentPilot — API Documentation

> API documentation untuk ContentPilot Central Server.

---

## 🔗 Base URL

```
https://api.contentpilot.dev
```

---

## 🔐 Authentication

### License Key Validation

```bash
curl -X POST https://api.contentpilot.dev/api/validate \
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
curl -X POST https://api.contentpilot.dev/api/activate \
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
curl -X POST https://api.contentpilot.dev/api/track \
  -H "Content-Type: application/json" \
  -d '{"key": "SB-XXXX-XXXX-XXXX", "event": {"type": "research"}}'
```

### Get Usage Stats

```bash
curl https://api.contentpilot.dev/api/usage/SB-XXXX-XXXX-XXXX
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
curl https://api.contentpilot.dev/api/updates?version=1.0.0
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
curl https://api.contentpilot.dev/api/changelog
```

---

## 🎫 Support

### Submit Ticket

```bash
curl -X POST https://api.contentpilot.dev/api/support \
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
curl -H "X-API-Key: your-admin-key" https://api.contentpilot.dev/api/stats
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

## 📝 Blog Management

### Check Active Processes

```bash
curl -X GET "https://api.contentpilot.dev/api/blogs/check-active?key=SB-XXXX-XXXX-XXXX"
```

**Response:**
```json
{
  "has_active": true,
  "articles": [
    {"id": 1, "title": "Article Title", "stage": "writing", "created_at": "2026-07-01 10:00:00"}
  ],
  "jobs": [
    {"id": 1, "job_type": "suggestion", "status": "pending", "created_at": "2026-07-01 10:00:00"}
  ],
  "pipelines": [
    {"id": 1, "article_id": 1, "stage": "researching", "started_at": "2026-07-01 10:00:00"}
  ],
  "total_active": 3
}
```

### Cancel Active Processes

```bash
curl -X POST https://api.contentpilot.dev/api/blogs/cancel-active \
  -H "Content-Type: application/json" \
  -d '{"license_key": "SB-XXXX-XXXX-XXXX"}'
```

**Response:**
```json
{
  "success": true,
  "cancelled_articles": 2,
  "cancelled_jobs": 1,
  "cancelled_pipelines": 1,
  "total_cancelled": 4
}
```

### Switch Platform

```bash
curl -X POST https://api.contentpilot.dev/api/blogs/switch-platform \
  -H "Content-Type: application/json" \
  -d '{"license_key": "SB-XXXX-XXXX-XXXX", "platform": "wordpress", "domain": "myblog.com", "blog_id": ""}'
```

**Response (success):**
```json
{
  "success": true,
  "platform": "wordpress"
}
```

**Response (has active processes):**
```json
{
  "error": "has_active_processes",
  "message": "Masih ada artikel dalam proses. Batalkan dulu."
}
```

### Check Blog Status

```bash
curl -X GET "https://api.contentpilot.dev/api/blogs/check?key=SB-XXXX-XXXX-XXXX"
```

**Response:**
```json
{
  "connected": true,
  "blog": {
    "id": 1,
    "domain": "myblog.com",
    "blog_id": "1234567890",
    "platform": "blogger"
  }
}
```

### List User Blogs

```bash
curl -X GET "https://api.contentpilot.dev/api/blogs/list?key=SB-XXXX-XXXX-XXXX"
```

**Response:**
```json
{
  "blogs": [
    {
      "id": 1,
      "domain": "myblog.com",
      "blog_id": "1234567890",
      "platform": "blogger",
      "created_at": "2026-07-01 10:00:00"
    }
  ]
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
