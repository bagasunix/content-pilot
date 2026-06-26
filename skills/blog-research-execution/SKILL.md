---
name: blog-research-execution
description: "Researcher bot execution patterns — check-first for existing content, then research with Ahrefs framework. Validates keywords before writing."
category: content
tags: [research, seo, keyword, execution, ahrefs, validation]
---

# Blog Research Execution (Research-Based)

## Research Basis
- **Ahrefs**: 90% of pages get no organic traffic
- **Google**: content must be helpful, reliable, people-first
- **Keyword validation**: check demand before creation

## Execution Protocol

### Step 1: Check Existing
**Before creating new content, check:**
- Search `site:{{DOMAIN}} [keyword]`
- Search GSC for existing rankings
- Check content inventory for similar topic
- Check `workspace/drafts/` for existing research briefs
- Avoid: duplicate content (Google penalty)

**If brief already exists in workspace/drafts/:**
- DO NOT create new brief
- Report to orchestrator with status
- Suggest alternatives: different angle, related topic, or brief refresh

### Step 2: Keyword Research (Ahrefs Framework)

**Seed Keywords**
- What does your audience search?
- What do competitors rank for?
- What does your site already rank for?

**Keyword Metrics (Priority Order)**
1. **Business Potential** (1-3): How valuable?
2. **Traffic Potential**: Total if ranking #1
3. **Keyword Difficulty** (0-100): How hard?
4. **Search Volume**: Monthly searches
5. **CPC**: Commercial intent indicator

**Search Intent Classification**
- **Informational**: "how to", "what is", "cara", "apa itu"
- **Navigational**: brand/product searches
- **Transactional**: "buy", "price", "beli", "harga"
- **Commercial Investigation**: "best", "review", "terbaik"

### Step 3: Competitor Analysis

**What to Analyze**
1. Top 10 SERP results for target keyword
2. Content structure (headings, word count, images)
3. Topics covered vs missing
4. Backlink profile
5. Content freshness

**Gap Analysis Template**
```
Competitor: [domain]
Content Length: [word count]
Structure: [heading count]
Topics Covered: [list]
Topics Missing: [what they don't cover]
Our Angle: [unique differentiator]
```

### Step 4: Content Brief

**Research Brief Structure**
```
# [Topic] — Research Brief

## Primary Keyword
- Target: [keyword]
- Search Volume: [volume]
- Difficulty: [KD]
- Intent: [type]

## Secondary Keywords
1. [keyword 1] — [volume]
2. [keyword 2] — [volume]
3. [keyword 3] — [volume]

## Competitor Analysis
[Gap analysis from Step 3]

## Unique Angle
[What we cover that competitors don't]

## Content Outline
1. [H2: topic]
   - [H3: subtopic]
   - [H3: subtopic]
2. [H2: topic]
   - [H3: subtopic]

## SERP Features to Target
- [ ] Featured snippet
- [ ] PAA
- [ ] Image pack

## Internal Links
- [existing article 1]
- [existing article 2]

## Research Sources
- [source 1]
- [source 2]
```

## Quality Gates

### Gate 1: Research → Content Brief
- [ ] Primary keyword validated (search demand confirmed)
- [ ] Intent classified correctly
- [ ] Competitor gaps identified
- [ ] Unique angle clear

### Gate 2: Content Brief → Writer
- [ ] Content outline complete
- [ ] Secondary keywords included
- [ ] SERP features targeted
- [ ] Internal links identified

## Pitfalls
1. **90% of pages get no traffic** — validate search demand first
2. Don't target keywords without business potential
3. Traffic Potential > Search Volume (better metric)
4. Intent mismatch = high bounce rate
5. Don't keyword stuff — Google's language matching is sophisticated
6. **Check workspace/drafts/ for existing briefs** — avoid creating duplicates

## Verification
- Keywords validated for search demand
- Intent classified correctly
- Competitor gaps identified
- Content brief includes SEO data
- Unique angle documented
