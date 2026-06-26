---
name: blog-research-execution-v2
description: "Advanced researcher execution — keyword clustering, SERP feature targeting, content gap automation, competitor content scoring."
category: researcher
tags: [research, advanced, clustering, serp, gap-analysis, scoring]
---

# Blog Research Execution V2 (Advanced)

## Advanced Features

### Keyword Clustering
- Group related keywords by SERP similarity
- Target: 1 cluster per article (5-15 keywords)
- Tools: Ahrefs keyword explorer, clustering tools
- Benefit: 1 article ranks for multiple keywords

### SERP Feature Analysis
- **Featured Snippets**: paragraph, list, table
- **People Also Ask**: collect all PAA questions
- **Image Pack**: image optimization opportunity
- **Video Pack**: video content opportunity

### Content Gap Automation
1. Find competitor content with backlinks
2. Identify topics they cover that you don't
3. Create better content on those topics
4. Outreach to sites linking to competitors

### Competitor Content Scoring
```
Score = (Word Count × 0.2) + (Backlinks × 0.3) + (Freshness × 0.2) + (SERP Position × 0.3)
```

## Research Process (Server-side)

Research dilakukan oleh SERVER (content-pilot-server).
Client hanya menerima research brief yang sudah jadi.

**Server capabilities:**
- Semantic search: research, Reddit, competitor analysis
- Video analysis: transcript extraction
- Blog monitoring: competitor tracking

## Advanced Research Workflow
### Step 0: Request Research ke Server
Server akan handle research dan return research brief.

### Step 1: Cluster Analysis
- Review "Previous Failure Context" in the research brief.
- Export all competitor keywords
- Group by SERP similarity
- Identify clusters you haven't covered
- Prioritize by business potential

### Step 2: SERP Feature Mapping
- For each target keyword, identify SERP features
- Plan content format to match feature
- Structure content for snippet optimization

### Step 3: Content Scoring
- Score competitor content (word count, backlinks, freshness)
- Identify: what makes top results rank
- Plan: how to exceed their score

### Step 4: Competitor Content Analysis
Server akan:
- Scan competitor blogs
- Analisis competitor YouTube content
- Semantic search untuk content gaps

### Step 5: Research Automation
- Template: research brief per cluster
- Checklist: validation steps
- Output: content brief ready for writer

## Quality Gates (Advanced)

### Gate 1: Cluster Validation
- [ ] Keywords grouped by SERP similarity
- [ ] Search volume > 100/month per cluster
- [ ] Business potential > 1 for cluster
- [ ] No duplicate coverage with existing content

### Gate 2: SERP Feature Target
- [ ] Featured snippet format identified
- [ ] PAA questions collected (5-10)
- [ ] Image pack opportunity assessed
- [ ] Content structure planned for target feature

### Gate 3: Competitor Scoring
- [ ] Top 5 competitors scored
- [ ] Content gap identified
- [ ] Our scoring target set
- [ ] Unique angle documented

## Pitfalls
1. Don't over-cluster — 1 article per cluster
2. Don't ignore SERP features — they dominate clicks
3. Don't copy competitor structure — improve it
4. Don't skip validation — quality over quantity
5. Track: research → content → ranking → traffic

## Verification
- Clusters validated and prioritized
- SERP features mapped
- Competitor scores calculated
- Research brief ready for writer
- Unique angle documented
