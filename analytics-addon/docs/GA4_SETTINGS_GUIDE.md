# GA4 Settings Configuration Guide

## 1. Property Settings

### Basic Settings
```
Property Name: {{DOMAIN}}
Industry Category: Technology / Education
Business Size: Small
Time Zone: (GMT+07:00) Jakarta
Currency: Indonesian Rupiah (IDR)
```

### Data Retention
```
Event data retention: 14 months (recommended)
Reset user data on new activity: ON
Enable data collection for Google products: ON
```

---

## 2. Data Streams Settings

### Enhanced Measurement Events
| Event | Status | Description |
|-------|--------|-------------|
| Page views | ✅ ON | Track page loads |
| Scrolls | ✅ ON | Track 90% scroll depth |
| Outbound clicks | ✅ ON | Track external link clicks |
| Site search | ✅ ON | Track search queries |
| Video engagement | ✅ ON | Track video plays |
| File downloads | ✅ ON | Track file downloads |

### Tag Settings
```
Collect Universal Analytics events: OFF
Allow Google signals data collection: ON
Enable data collection in Google Analytics 4: ON
```

---

## 3. Event Configuration

### Recommended Events (Custom)
| Event Name | Trigger | Parameters |
|------------|---------|------------|
| `cta_click` | CTA button click | button_text, page_location |
| `form_submit` | Form submission | form_id, form_name |
| `newsletter_signup` | Email signup | method |
| `download` | File download | file_name, file_type |
| `video_play` | Video start | video_title, video_url |
| `internal_click` | Internal link click | link_text, link_url |

### Conversion Events
| Event | Mark as Conversion | Value |
|-------|-------------------|-------|
| `page_view` | ❌ OFF | - |
| `form_submit` | ✅ ON | Optional |
| `cta_click` | ✅ ON | Optional |
| `newsletter_signup` | ✅ ON | Optional |

---

## 4. Audience Settings

### Default Audiences
| Audience | Condition |
|----------|-----------|
| All Users | Default |
| New Users | First visit = today |
| Returning Users | Session count > 1 |

### Custom Audiences (Recommended)
| Audience | Condition |
|----------|-----------|
| Engaged Users | Session duration > 30s AND pages > 2 |
| Blog Readers | page_view + scroll_depth > 50% |
| Active Readers | time_on_page > 60s |
| Bounced Users | session_duration < 10s AND pages = 1 |

---

## 5. Attribution Settings

### Reporting Attribution Model
```
Recommended: Data-driven attribution
Alternative: Last click
Window: 90-day click, 30-day lookback
```

### Channel Grouping
```
- Organic Search
- Direct
- Social
- Referral
- Email
- Paid Search
- Display
- Affiliate
```

---

## 6. Debug & Testing

### Debug Mode Settings
```
Enable DebugView: ON
Debug mode trigger: 
  - URL parameter: ?debug_mode=true
  - GA Debugger Chrome extension
```

### Realtime Report
- Active users in last 30 minutes
- Events by event name
- Users by device
- Users by country
- Users by page

---

## 7. Internal Traffic Rules

### Filter Internal Traffic
```
Rule name: Internal Traffic
Traffic type: internal
Match type: IP address equals
Value: [YOUR_IP_ADDRESS]
```

### Common Internal IPs to Exclude
- Home IP: [Add your home IP]
- Office IP: [Add office IP if applicable]
- VPN IP: [Add VPN IP if applicable]

**How to find your IP:**
```bash
curl ifconfig.me
```

---

## 8. Custom Dimensions

### Recommended Custom Dimensions
| Dimension | Scope | Description |
|-----------|-------|-------------|
| `content_category` | Event | Article category |
| `content_type` | Event | Tutorial, Review, etc |
| `author` | Event | Article author |
| `publish_date` | Event | Publication date |

---

## 9. Custom Metrics

### Recommended Custom Metrics
| Metric | Scope | Description |
|--------|-------|-------------|
| `read_time` | Event | Time spent reading |
| `scroll_depth` | Event | Scroll percentage |
| `video_duration` | Event | Video watch time |
| `cta_clicks` | Event | CTA interaction count |

---

## 10. Data Filters

### Exclude Spam Traffic
```
Filter name: Exclude Spam
Filter type: Include
Dimension: Traffic source
Expression: Does not match regex: (spam|bot|crawler)
```

### Filter Internal Traffic
```
Filter name: Internal Traffic
Filter type: Exclude
Dimension: IP address
Expression: Matches regex: (YOUR_IP)
```

---

## 11. Notification Settings

### Email Notifications
```
Weekly report: ✅ ON
Monthly report: ✅ ON
Anomaly detection: ✅ ON
Data quality alerts: ✅ ON
```

---

## 12. Integration Settings

### Google Search Console
```
Link account: ✅ ON
Data sharing: ✅ ON
Default channel grouping: ✅ ON
```

### Google Ads (Optional)
```
Link account: ON/OFF
Auto-tagging: ON
Import goals: ON
```

### BigQuery Export (Optional)
```
Link project: ON/OFF
Export frequency: Daily
```

---

## 13. Consent Mode

### Cookie Consent Settings
```
Grant consent: ON
Consent type: analytics_storage
Region: Indonesia (ID)
```

---

## 14. Quick Setup Checklist

- [ ] Property name correct
- [ ] Time zone set to Jakarta
- [ ] Currency set to IDR
- [ ] Data retention set to 14 months
- [ ] Enhanced measurement all ON
- [ ] Debug mode enabled
- [ ] Internal traffic filter added
- [ ] Conversion events configured
- [ ] Custom dimensions/metrics added
- [ ] Search Console linked
- [ ] Email notifications ON

---

## 15. GA4 vs Universal Analytics Settings

| Setting | UA | GA4 | Action |
|---------|-----|-----|--------|
| Sessions | ✅ | ❌ | Use Engagement rate |
| Bounce Rate | ✅ | ✅ | Now available |
| Pages/Session | ✅ | ❌ | Use Views per user |
| Avg. Session Duration | ✅ | ❌ | Use Avg. engagement time |
| Goals | ✅ | ❌ | Use Conversions |
| Custom Reports | ✅ | ✅ | Use Explorations |

---

**Status:** Settings Reference
**Author:** Blog Orchestrator
**Date:** 2026-06-17