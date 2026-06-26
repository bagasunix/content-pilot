---
name: engagement-rate-metrics
description: "Use when implementing GA4's engagement metrics as primary KPIs — engagement rate, engaged sessions, engaged time."
category: analyst
tags: [engagement, metrics, ga4, kpi, analytics, user-behavior]
---

# Engagement Rate Metrics (Research-Based)

## GA4 Engagement Metrics

### Engagement Rate
**Definition**: Engaged sessions / Total sessions
**Target**: > 60% (good), > 70% (excellent)
**Calculation**: (Sessions > 10s + Conversions + Pageviews > 1) / Total

### Engaged Sessions
**Definition**: Sessions lasting > 10 seconds, OR had conversion event, OR had 2+ pageviews
**Target**: > 60% of sessions

### Engaged Time
**Definition**: Average time users actively engage
**Target**: > 2 minutes

### Events per Session
**Definition**: Average events triggered per session
**Target**: > 3 events

## Implementation

### Step 1: Configure Engagement Events
```javascript
gtag('event', 'engagement', {
  'engagement_time_msec': 30000,
  'session_engaged': 1
});
```

### Step 2: Set Up Custom Metrics
1. GA4 > Admin > Custom Definitions
2. Create: engagement_rate, engaged_sessions
3. Create: engaged_time, events_per_session

### Step 3: Create Dashboard
1. GA4 > Explore
2. Add: engagement metrics
3. Filter: by content category
4. Compare: over time

## Content Performance Analysis

### High Engagement Content
- **Characteristics**: long read time, multiple events
- **Action**: create more similar content
- **Promote**: feature in newsletter

### Low Engagement Content
- **Characteristics**: short time, single pageview
- **Action**: improve content quality
- **Test**: new hooks, better structure

## Benchmarks by Content Type

| Content Type | Target Engagement Rate |
|--------------|----------------------|
| Tutorials | > 70% |
| News | > 50% |
| Reviews | > 60% |
| Listicles | > 55% |
| Long-form | > 75% |

## Pitfalls
1. Don't ignore engagement for pageviews
2. Don't compare engagement across different content types
3. Don't forget mobile engagement is different
4. Don't ignore time-on-page as engagement signal
5. Don't set unrealistic targets

## Verification
- Engagement metrics configured in GA4
- Dashboard created and monitored
- Benchmarks set by content type
- Low engagement content identified and improved
- Trends tracked over time
