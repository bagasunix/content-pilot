---
name: ab-test-headlines
description: "Use when a published article gets impressions but low CTR — test new titles against GSC data, iterate for improvement."
category: analyst
tags: [ab-testing, headlines, ctr, gsc, optimization, testing]
---

# A/B Test Headlines (Research-Based)

## Research Basis
- **CTR optimization**: 20-30% improvement possible
- **GSC data**: real user behavior signals
- **Statistical significance**: 1000+ impressions needed

## Detection: When to Test

### Low CTR Signals (GSC)
- **CTR < 2%** with position < 10 = title issue
- **Impressions high, clicks low** = not compelling
- **Position stable, CTR declining** = title fatigue

### GSC Analysis Steps
1. Performance > Pages
2. Sort by impressions (descending)
3. Filter: CTR < 2%
4. Identify: high impressions + low CTR

## Testing Framework

### Step 1: Analyze Current Title
- Is keyword included?
- Is it specific enough?
- Is there emotional hook?
- Does it match search intent?

### Step 2: Generate Variations
- **Number formula**: "7 Cara..."
- **How-to formula**: "Cara..."
- **Question formula**: "Pernahkah..."
- **Curiosity gap**: "Ini Alasannya..."

### Step 3: Test One at a Time
- Change title only
- Wait 2-4 weeks
- Compare CTR before/after
- Check for statistical significance

### Step 4: Measure Results
- **Primary metric**: CTR change
- **Secondary metric**: position change
- **Tertiary metric**: engagement metrics

## Statistical Significance

### Requirements
- **Minimum impressions**: 1000 per variation
- **Minimum clicks**: 50 per variation
- **Time period**: 2-4 weeks minimum

### Calculation
```
Significant if: |CTR_new - CTR_old| > 2 × Standard Error
Standard Error = sqrt(p × (1-p) / n)
```

## Title Formulas That Work

### Formula 1: [Number] + [Adjective] + [Noun] + [Promise]
"7 Cara Mudah Meningkatkan Traffic Blog"

### Formula 2: How to [Achieve] Without [Pain Point]
"Cara Mendapatkan Backlink Tanpa Spam"

### Formula 3: [Year] Guide: [Topic] for [Audience]
"Panduan SEO 2026 untuk Blogger Pemula"

### Formula 4: [Topic]: [Number] Things You're Doing Wrong
"SEO: 5 Kesalahan yang Membunuh Traffic"

## Pitfalls
1. Don't change multiple elements at once
2. Don't test too frequently (wait for data)
3. Don't ignore statistical significance
4. Don't forget to track changes
5. Don't test on low-traffic pages

## Verification
- CTR improved by > 20%
- Statistical significance reached
- Position maintained or improved
- Changes documented
- Systematic testing process established
