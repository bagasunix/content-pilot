---
name: content-calendar-automation
description: "Use when scheduling blog content based on analytics signals — auto-suggest topics, plan publish dates, maintain cadence. Based on professional editorial pipeline patterns."
category: content
tags: [content, calendar, automation, scheduling, analytics, pipeline]
---

# Content Calendar Automation

## Research Basis
- Professional editorial teams (NYT, BuzzFeed, HubSpot) use structured pipelines
- Quality gates between stages prevent downstream issues
- Parallel execution improves throughput without sacrificing quality

## Trigger Conditions
- User says "jadwal posting" / "content calendar"
- Weekly planning session
- After research delivers topic suggestions
- Content inventory needs new entries

## Pipeline Architecture (Professional Model)

### Stage 1: Ideation
**Input**: Trending topics, analytics data, competitor gaps
**Process**: Generate 10-15 topic ideas, score by business potential
**Output**: Ranked topic list
**Duration**: 1 hour

### Stage 2: Assignment
**Input**: Ranked topic list
**Process**: Match topics to content type, assign writer
**Output**: Assigned tasks with deadlines
**Duration**: 30 minutes

### Stage 3: Research
**Input**: Topic brief
**Process**: Keyword research, competitor analysis, content brief
**Output**: Research brief.md
**Duration**: 2 hours

### Stage 4: Writing
**Input**: Research brief
**Process**: Draft from brief, apply voice guide
**Output**: Draft.md (1000-2000 words)
**Duration**: 4 hours

### Stage 5: Review
**Input**: Draft
**Process**: Fact check, SEO review, readability
**Output**: Approved draft
**Duration**: 2 hours

### Stage 6: Visual
**Input**: Approved draft
**Process**: Cover image, in-article images
**Output**: Images folder
**Duration**: 1 hour (parallel with Stage 5)

### Stage 7: Publish
**Input**: Approved draft + images
**Process**: Upload, format, schedule
**Output**: Live URL
**Duration**: 30 minutes

### Stage 8: Promote
**Input**: Live URL
**Process**: Social media, newsletter, distribution
**Output**: Distribution report
**Duration**: 30 minutes

## Quality Gates (Research-Based)

### Gate 1: Research → Writing
- [ ] Content brief complete
- [ ] Keywords validated
- [ ] Competitor gaps identified
- [ ] Unique angle clear

### Gate 2: Writing → Review
- [ ] Word count 1000-2000
- [ ] All sections covered
- [ ] Internal links added
- [ ] Images referenced

### Gate 3: Review → Publish
- [ ] Fact check passed
- [ ] SEO optimization complete
- [ ] Readability score > 60
- [ ] No broken links

## Calendar Template

| Day | Category | Topic | Stage | Assign | Deadline |
|-----|----------|-------|-------|--------|----------|
| Mon | Technology | [topic] | Research | Researcher | Tue |
| Tue | Tutorial | [topic] | Writing | Writer | Thu |
| Wed | News | [topic] | Review | Editor | Thu |
| Thu | Entertainment | [topic] | Publish | Publisher | Fri |
| Fri | Download | [topic] | Promote | Publisher | Fri |

## Frequency Optimization

### Blog Size → Frequency
- **< 50 posts**: 3-4x/week (build foundation)
- **50-200 posts**: 2-3x/week (maintain momentum)
- **200+ posts**: 1-2x/week (focus on quality + refresh)

### Category Balance
- **Evergreen** (tutorials, guides): 40% — long-term traffic
- **Trending** (news, updates): 30% — immediate traffic
- **Engagement** (opinion, stories): 20% — community building
- **Refresh** (updates to old content): 10% — maintain existing

## Pipeline Metrics
- **Time per stage**: track and optimize
- **Pass/fail rate**: quality gate effectiveness
- **Total pipeline time**: target < 24 hours for standard article
- **Revision count**: target < 2 revisions

## Pitfalls
1. Don't overload — quality over quantity
2. Balance evergreen vs trending content
3. Account for holidays and events
4. Leave buffer for breaking news
5. Review calendar weekly, not just set-and-forget
6. Don't skip quality gates — they prevent downstream issues

## Verification
- Calendar published to team weekly
- All articles have target dates
- Categories balanced across week
- Pipeline capacity not exceeded
- Quality gates passing consistently
