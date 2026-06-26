---
name: content-audit-inventory
description: "Use when auditing existing blog content at scale — content inventory, quality scoring, stale detection, consolidation planning. Based on Backlinko ICE model."
category: analyst
tags: [content-audit, inventory, stale-content, ice-scoring, consolidation, decay]
---

# Content Audit & Inventory (Research-Based)

## Research Basis
- **Backlinko**: audit existing content for hidden winners before creating new
- **HubSpot**: refreshed posts saw 106% traffic increase
- **Ahrefs**: 90% of pages get no organic traffic — audit to find which to fix vs remove

## When to Run Audit
- **Quarterly**: full comprehensive audit
- **After traffic drop**: immediate investigation
- **Before content strategy refresh**: baseline measurement
- **After major algorithm update**: impact assessment

## Step 1: Build Content Inventory

### Data Collection
Export from these sources:
- **Google Search Console**: all indexed URLs, impressions, clicks, position
- **Google Analytics**: pageviews, engagement time, conversions
- **Ahrefs/Screaming Frog**: word count, backlinks, internal links

### Inventory Spreadsheet Columns
```
URL | Title | Publish Date | Last Updated | Word Count | Category |
Organic Traffic | Impressions | Avg Position | Clicks | CTR |
Backlinks | Internal Links | Word Count | Status | Priority
```

### Status Classification
- **Keep**: traffic stable/growing, good quality
- **Update**: traffic declining, outdated content, thin
- **Consolidate**: multiple thin pages on same topic
- **Remove**: zero traffic, no backlinks, irrelevant
- **Redirect**: outdated URL but has backlinks

## Step 2: Content Quality Scoring (ICE Model)

### ICE Framework
**Impact (1-10)**: How much traffic/revenue if improved?
- Check: current traffic trend, keyword potential, commercial intent
- 10 = high traffic + commercial intent + growing niche
- 1 = zero traffic + no commercial value

**Confidence (1-10)**: How sure you can rank/improve?
- Check: current position, competition, content quality
- 10 = already ranking 5-15, weak competitors
- 1 = page 5+, strong competitors, thin content

**Ease (1-10)**: How easy to improve?
- Check: content age, word count, backlinks needed
- 10 = just needs update, no backlinks needed
- 1 = complete rewrite, needs many backlinks

### ICE Score = (Impact + Confidence + Ease) / 3

### Priority Matrix
| ICE Score | Action | Timeline |
|-----------|--------|----------|
| 7-10 | Update immediately | This week |
| 5-6 | Schedule update | This month |
| 3-4 | Monitor, low priority | Next quarter |
| 1-2 | Consider removing | After review |

## Step 3: Stale Content Detection

### Decay Signals
- **Traffic drop >30%** in 90 days (GA4 comparison)
- **Impressions declining** but position stable (GSC)
- **CTR below 2%** for position 1-10 (title issue)
- **No updates in 12+ months** (outdated risk)
- **Competitors outranking** with fresher content

### Decay Categories
```
Category A: High traffic + declining → URGENT update
Category B: Medium traffic + declining → schedule update
Category C: Low traffic + no backlinks → consolidate or remove
Category D: Zero traffic → redirect or delete
```

### Decay Curve by Content Type
| Type | Expected Half-Life | Refresh Frequency |
|------|-------------------|-------------------|
| News/Updates | 1-3 months | Monthly |
| How-to/Tutorial | 6-12 months | Quarterly |
| Evergreen Guide | 12-24 months | Semi-annually |
| Data/Research | 6-12 months | Quarterly |

## Step 4: Content Consolidation

### When to Consolidate
- 2+ pages targeting same keyword
- Thin pages (< 800 words) on related topics
- Similar content with different URLs
- Pages cannibalizing each other in SERPs

### Consolidation Process
1. Identify consolidation candidates (same keyword, similar content)
2. Choose best page (most traffic, most backlinks, best URL)
3. Merge content from other pages into best page
4. 301 redirect merged URLs to best page
5. Update internal links to point to consolidated page
6. Submit to GSC for re-crawling

## Step 5: Internal Linking Audit

### Orphan Page Detection
- Pages with 0 internal links pointing TO them
- Use Screaming Frog or Ahrefs Site Audit
- Target: every page has 3+ internal links

### Link Equity Distribution
- Pages with most backlinks should link to priority pages
- High-authority pages should link to conversion pages
- New content should get links from established pages

### Anchor Text Audit
- Check: varied anchor text (not all exact match)
- Fix: generic anchors ("click here") → descriptive
- Target: natural keyword variation in anchors

## Step 6: Quarterly Audit Report

### Report Template
```
## Content Audit Report — [Quarter] [Year]

### Summary
- Total pages audited: [count]
- Pages to keep: [count] ([%])
- Pages to update: [count] ([%])
- Pages to consolidate: [count] ([%])
- Pages to remove: [count] ([%])

### Top Update Candidates (by ICE score)
| URL | ICE | Traffic | Action | Deadline |
|-----|-----|---------|--------|----------|

### Consolidation Plan
| Primary URL | Merge From | Redirects | Status |
|-------------|------------|-----------|--------|

### Stale Content by Category
| Category | Total | Stale | % Stale | Action |
|----------|-------|-------|---------|--------|

### Internal Link Issues
- Orphan pages: [count]
- Missing anchor text: [count]
- Broken internal links: [count]

### Recommendations
1. [top priority]
2. [second priority]
3. [third priority]
```

## Pitfalls
1. Don't audit without data — need GSC + GA4 at minimum
2. Don't remove pages with backlinks — redirect instead
3. Don't consolidate too aggressively — one topic per page
4. Don't forget to update internal links after consolidation
5. Don't skip re-submitting to GSC after changes

## Verification
- Content inventory complete (all URLs cataloged)
- ICE scores assigned to all pages
- Stale content identified and prioritized
- Consolidation plan ready
- Internal link issues documented
- Quarterly report generated
