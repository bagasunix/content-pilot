---
name: technical-seo-audit
description: "Use when auditing the blog's technical health — sitemap, robots.txt, crawl budget, structured data, mobile-first, Core Web Vitals."
category: analyst
tags: [technical-seo, audit, sitemap, robots, crawl, schema]
---

# Technical SEO Audit (Research-Based)

## Audit Checklist

### 1. Crawling & Indexing

**Sitemap**
- [ ] sitemap.xml exists and accessible
- [ ] All important URLs included
- [ ] No 404 or redirect URLs
- [ ] Submitted to Google Search Console
- [ ] Update frequency set correctly

**Robots.txt**
- [ ] No important pages blocked
- [ ] Sitemap URL referenced
- [ ] No accidental disallows
- [ ] User-agent rules correct

**Crawl Budget**
- [ ] No infinite crawl loops
- [ ] Parameters handled correctly
- [ ] Internal links optimized
- [ ] No orphan pages

### 2. Mobile-First Indexing

**Mobile Rendering**
- [ ] Content visible on mobile
- [ ] No hidden content
- [ ] Responsive design works
- [ ] Touch elements sized correctly

**Mobile Performance**
- [ ] LCP < 2.5s on mobile
- [ ] INP < 200ms
- [ ] CLS < 0.1
- [ ] PageSpeed score > 80

### 3. Structured Data

**Schema Markup**
- [ ] Article schema on all posts
- [ ] Organization schema on homepage
- [ ] Breadcrumb schema implemented
- [ ] No validation errors

**Rich Results**
- [ ] Eligible for rich results
- [ ] Preview looks correct
- [ ] No warnings in GSC
- [ ] Regular monitoring

### 4. Security & HTTPS

**HTTPS**
- [ ] All pages HTTPS
- [ ] No mixed content
- [ ] SSL certificate valid
- [ ] HTTP redirects to HTTPS

### 5. Internal Linking

**Structure**
- [ ] Logical hierarchy
- [ ] No orphan pages
- [ ] Anchor text descriptive
- [ ] Link equity distributed

### 6. Page Speed

**Core Web Vitals**
- [ ] LCP < 2.5s (75th percentile)
- [ ] INP < 200ms (75th percentile)
- [ ] CLS < 0.1 (75th percentile)

**Additional Metrics**
- [ ] FCP < 1.8s
- [ ] Speed Index < 3.4s
- [ ] Total Blocking Time < 200ms

## Audit Tools

### Free Tools
- **Google Search Console**: crawl errors, mobile issues
- **PageSpeed Insights**: performance analysis
- **Mobile-Friendly Test**: mobile rendering
- **Rich Results Test**: structured data validation

### Paid Tools
- **Screaming Frog**: comprehensive crawl
- **Ahrefs Site Audit**: automated audits
- **SEMrush Site Audit**: technical issues
- **Sitebulb**: visual audit reports

## Audit Schedule

### Monthly
- Full technical audit
- Core Web Vitals check
- Crawl error review
- Schema validation

### Quarterly
- Comprehensive sitemap review
- Internal link audit
- Mobile rendering check
- Security scan

### After Changes
- Template updates
- New features added
- Content restructuring
- URL changes

## Pitfalls
1. Don't ignore mobile issues (60%+ traffic)
2. Don't forget to resubmit sitemap after changes
3. Don't block important pages in robots.txt
4. Don't ignore structured data errors
5. Don't skip security checks (HTTPS)

## Verification
- All checklist items pass
- No critical issues found
- Performance targets met
- Schema valid and rendering
- Sitemap submitted and indexed
