# Blog Analytics Addon

> Analytics integration untuk Blog Lifecycle Pro — GA4, GSC, GTM.

## Features

- **GA4 Integration** — Track pageviews, events, conversions
- **GSC Integration** — Monitor search performance, keywords
- **GTM Integration** — Manage tags, triggers, variables
- **Weekly Reports** — Automated analytics reports
- **SEO Monitoring** — Track rankings, impressions, clicks

## Installation

```bash
cd blog-lifecycle-pro
cp -r analytics-addon/skills/* skills/
cp -r analytics-addon/docs/* workspace/docs/
```

## Setup

### 1. GA4 Setup

1. Buat Google Cloud Project
2. Enable GA4 Data API
3. Buat Service Account
4. Download credentials.json
5. Setup di GA4 Settings Guide

### 2. GSC Setup

1. Enable Search Console API
2. Buat OAuth credentials
3. Verify ownership via DNS/CSP

### 3. GTM Setup

1. Buat GTM container
2. Install GTM snippet di blog
3. Setup triggers & variables

## Usage

### GA4 Events

```python
# Track custom events
from analytics import GA4Tracker

tracker = GA4Tracker(property_id="YOUR_PROPERTY_ID")
tracker.track_event("article_view", {"article_id": "123", "category": "tutorial"})
```

### GSC Queries

```python
# Get search performance
from analytics import GSCClient

client = GSCClient(credentials_path="credentials.json")
data = client.get_search_analytics(
    start_date="2024-01-01",
    end_date="2024-01-31",
    dimensions=["query", "page"]
)
```

### Weekly Reports

```bash
# Generate weekly report
python3 scripts/generate_report.py --period weekly

# Generate monthly report
python3 scripts/generate_report.py --period monthly
```

## Configuration

Add to `workspace/config.yaml`:

```yaml
# Analytics (optional)
analytics:
  enabled: true
  ga4_property_id: "YOUR_PROPERTY_ID"
  gsc_property_url: "https://yourdomain.com"
  gtm_container_id: "GTM-XXXXXXX"
```

## Troubleshooting

### GA4 not tracking

1. Check if GA4 snippet is installed
2. Verify property ID
3. Check browser console for errors

### GSC not showing data

1. Verify ownership
2. Check if API is enabled
3. Wait 24-48 hours for data

## License

MIT License (same as Blog Lifecycle Pro)
