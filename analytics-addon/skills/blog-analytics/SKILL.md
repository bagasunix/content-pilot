---
name: blog-analytics
description: "GA4 setup + data pulling for blogs — custom events, engagement metrics, content grouping, GA4 Data API, Blogger API content inventory."
category: analyst
tags: [analytics, ga4, events, engagement, conversion, tracking, blogger-api, content-inventory]
---

# Blog Analytics (GA4 + Content Inventory)

## GA4 Setup for Blogger

### Initial Configuration
1. **Property Settings**: {{DOMAIN}}, Indonesia timezone
2. **Data Streams**: Web stream, enhanced measurement ON
3. **Data Retention**: 14 months (free), 50 months (GA360)
4. **IP Anonymization**: automatic in GA4

### Required Custom Events

**Content Engagement**
- `article_read` — user scrolls past 70%
- `time_on_page_5min` — engaged session
- `scroll_depth` — max scroll percentage
- `click_outbound` — external link click

**Conversions**
- `newsletter_signup` — email subscription
- `affiliate_click` — affiliate link click
- `download_asset` — PDF/tool download

### Event Parameters
```javascript
gtag('event', 'article_read', {
  'article_title': 'Article Title',
  'article_category': 'Technology',
  'word_count': 1500,
  'author': 'Bagas'
});
```

## Content Grouping

### Dimensions
- **Category**: Technology, Entertainment, News, Tutorial, Download
- **Author**: Bagas, Guest
- **Word Count**: < 1000, 1000-2000, 2000+
- **Publication Month**: for trend analysis

### Setup
1. GA4 > Admin > Custom Definitions
2. Create custom dimensions for each grouping
3. Send with every event

## Engagement Metrics

### Key Metrics
- **Engagement Rate**: engaged sessions / total sessions
- **Engaged Time**: average time on page
- **Scroll Depth**: average scroll percentage
- **Events per Session**: engagement intensity

### Benchmarks
- Engagement Rate: > 60% (good), > 70% (excellent)
- Avg Engaged Time: > 2 minutes
- Scroll Depth: > 50%
- Events per Session: > 3

## GA4 Data API — Pulling Analytics Data

### Auth Requirements (DIFFERENT from Blogger OAuth!)
The Blogger OAuth token (`blogger` scope) **cannot** access GA4. You need separate credentials:
- **Property ID** (numeric, e.g., `properties/123456789`) — from GA4 Admin → Property Settings
- **OAuth scope:** `https://www.googleapis.com/auth/analytics.readonly`
- **OR** a service account with GA4 Reader role

### Python: Pull Top Pages
```python
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/analytics.readonly'])
if creds.expired:
    creds.refresh(Request())

service = build('analyticsdata', 'v1beta', credentials=creds)
property_id = 'properties/YOUR_PROPERTY_ID'

result = service.properties().runReport(
    property=property_id,
    body={
        'dateRanges': [{'startDate': '30daysAgo', 'endDate': 'today'}],
        'dimensions': [{'name': 'pagePath'}],
        'metrics': [{'name': 'screenPageViews'}, {'name': 'averageSessionDuration'}, {'name': 'engagementRate'}],
        'orderBys': [{'metric': {'metricName': 'screenPageViews'}, 'sort': 'DESCENDING'}],
        'limit': 10
    }
).execute()

for row in result.get('rows', []):
    path = row['dimensionValues'][0]['value']
    views = row['metricValues'][0]['value']
    print(f"{path}: {views} views")
```

### Python: Pull Traffic Sources
```python
result = service.properties().runReport(
    property=property_id,
    body={
        'dateRanges': [{'startDate': '30daysAgo', 'endDate': 'today'}],
        'dimensions': [{'name': 'sessionSource'}, {'name': 'sessionMedium'}],
        'metrics': [{'name': 'sessions'}],
        'orderBys': [{'metric': {'metricName': 'sessions'}, 'sort': 'DESCENDING'}],
        'limit': 10
    }
).execute()
```

### Common Pitfalls — GA4 API Auth
1. **Blogger token ≠ GA4 token** — they use different OAuth scopes; don't try to reuse
2. **Property ID is numeric** — not the Measurement ID (G-XXXXXXXXXX); found in GA4 Admin
3. **Service account needs GA4 Reader role** — grant in GA4 Admin → Property Access Management
4. **Data freshness** — GA4 reports have 24-48h delay (free tier)
5. **Quota** — 100K tokens/day, 1500 requests/project/day (free tier)

## Content Inventory from Blogger API

### Pull All Published Posts
```python
from googleapiclient.discovery import build

service = build('blogger', 'v3', credentials=blogger_creds)
blog_id = 'YOUR_BLOG_ID'

all_posts = []
page_token = None
while True:
    result = service.posts().list(blogId=blog_id, maxResults=20, pageToken=page_token, fetchBodies=False).execute()
    all_posts.extend(result.get('items', []))
    page_token = result.get('nextPageToken')
    if not page_token:
        break

# Each post has: id, title, url, published, updated, labels, author
```

### Key Fields per Post
- `title` — post title
- `url` — canonical URL
- `published` — publish timestamp (ISO 8601)
- `updated` — last modification timestamp
- `labels` — array of category tags
- `status` — not returned by default; use `fetchBodies=False` for efficiency

### Note on Status
Blogger API v3 does NOT return `status` field in posts().list(). All returned posts are published. Drafts require `isDraft=True` filter on posts().list().

## Free GA4 vs GA360

| Feature | Free | GA360 |
|---------|------|-------|
| Events/month | 10M | unlimited |
| Data retention | 14 months | 50 months |
| Custom dimensions | 50 | 125 |
| BigQuery export | yes | yes |
| Freshness | 24-48 hours | < 4 hours |
| Cost | free | ~$150K/year |

## Pitfalls
1. Don't track PII (personally identifiable information)
2. Don't send > 500 unique events (diminishing returns)
3. Don't ignore enhanced measurement (auto-tracking)
4. Don't forget data retention settings
5. Don't mix UA and GA4 data
6. Don't try to use Blogger OAuth for GA4 — different scopes, different tokens
7. Don't confuse Measurement ID (G-XXX) with Property ID (numeric) — GA4 API needs the numeric one

## Verification
- GA4 property created and verified
- Enhanced measurement enabled
- Custom events defined and firing
- Content grouping configured
- Engagement metrics visible in reports
- GA4 Data API accessible (test with a simple runReport call)
- Blogger API content inventory pullable (test with posts().list)
