---
name: link-validator
description: "Use when checking external links in blog drafts for hoaxes, misinformation, and broken links — validation against known databases."
category: editor
tags: [links, validation, fact-check, broken, misinfo, seo]
---

# Link Validator (Research-Based)

## Research Basis
- **Google**: broken links hurt UX and crawl budget
- **Trust signals**: links to authoritative sources improve E-E-A-T
- **SEO**: outbound link quality affects rankings

## Validation Criteria

### Link Quality Assessment
1. **Domain Authority**: DR > 30 preferred
2. **HTTPS**: required (HTTP = penalty)
3. **Noindex**: don't link to noindex pages
4. **Relevance**: topical match to your content
5. **Freshness**: content < 2 years old preferred

### Source Reliability Check
- **Government**: .gov, .go.id — high trust
- **Academic**: .edu, university sites — high trust
- **Industry**: established publications — medium trust
- **Blog**: unknown — verify manually
- **Wikipedia**: use as reference, not primary source

## Validation Workflow

### Step 1: Automated Check
- Extract all links from content
- Check HTTP status (200 = OK, 404 = broken)
- Verify HTTPS
- Check response time (< 3 seconds)

### Step 2: Quality Assessment
- Domain authority check
- Topical relevance check
- Content freshness check
- Anchor text appropriateness

### Step 3: Manual Review
- Visit flagged links
- Verify content accuracy
- Check for misinformation
- Confirm relevance

### Step 4: Fix/Replace
- Broken links: find alternative or remove
- Low quality: find better source
- Outdated: find newer version
- Irrelevant: remove or replace

## Broken Link Detection

### Tools
- **Check My Links** (Chrome extension)
- **Ahrefs Site Audit**
- **Screaming Frog**
- **Google Search Console** (coverage report)

### Fix Strategy
1. **Same site**: internal redirect
2. **Different site**: find alternative or remove
3. **Archive.org**: use cached version if available
4. **Contact**: reach out to site owner

## Misinformation Check

### Red Flags
- Claims without sources
- Extreme language ("always", "never")
- Unverifiable statistics
- Opinion presented as fact

### Verification Steps
- Cross-reference with 2+ sources
- Check primary source (original study)
- Verify statistics with original publication
- Look for peer review or expert consensus

## Output Format

### Validation Report
```
## Link Validation Report

### Total Links: [count]
### Valid: [count] ✓
### Broken: [count] ✗
### Low Quality: [count] ⚠
### Needs Review: [count] ?

### Broken Links
1. [URL] — HTTP [status]
   - Fix: [replacement URL] or [remove]

### Low Quality Links
1. [URL] — DR: [score]
   - Issue: [reason]
   - Fix: [replacement URL]

### Recommended Actions
1. [action 1]
2. [action 2]
```

## Pitfalls
1. Don't link to sites with malware or phishing
2. Don't link to competitor pages (helps them)
3. Don't over-link (3-5 external links per 1000 words)
4. Don't use "click here" as anchor text
5. Don't link to noindex pages

## Verification
- All links return HTTP 200
- External links have DR > 30
- No broken links
- Anchor text descriptive
- Link count appropriate (3-5 per 1000 words)
