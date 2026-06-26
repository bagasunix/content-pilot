---
name: blog-performance
description: "Use when the blog loads slowly or Core Web Vitals fail — LCP, INP, CLS optimization. Specific fixes for Blogger platform."
category: analyst
tags: [performance, core-web-vitals, lcp, inp, cls, speed]
---

# Blog Performance (Core Web Vitals)

## Core Web Vitals Metrics

### LCP (Largest Contentful Paint)
**Target**: < 2.5 seconds
**What**: Time to render largest visible element
**Common Issues on Blogger**:
- Large hero images
- Render-blocking CSS/JS
- Server response time

**Fixes**:
1. Compress images (< 200KB)
2. Use WebP format
3. Lazy load below-fold images
4. Minimize CSS/JS

### INP (Interaction to Next Paint)
**Target**: < 200 milliseconds
**What**: Time from interaction to visual response
**Common Issues on Blogger**:
- Heavy JavaScript
- Third-party widgets
- Slow event handlers

**Fixes**:
1. Defer non-critical JS
2. Minimize third-party scripts
3. Use async loading for widgets

### CLS (Cumulative Layout Shift)
**Target**: < 0.1
**What**: Unexpected layout movement
**Common Issues on Blogger**:
- Ad loading causing shift
- Images without dimensions
- Font loading (FOUT)

**Fixes**:
1. Set explicit width/height on images
2. Use font-display: swap
3. Reserve space for ads
4. Preload critical fonts

## Blogger-Specific Optimizations

### Template Optimization
- Switch to minimal/lightweight theme
- Remove unused widgets
- Minimize external scripts
- Use CSS sprites for icons

### Image Optimization
- Compress before upload (< 100KB ideal)
- Use responsive images (srcset)
- Lazy load with loading="lazy"
- Use WebP with fallback

### Third-Party Scripts
- **Analytics**: async loading
- **Ads**: defer loading
- **Social widgets**: lazy load
- **Fonts**: preload + display: swap

## PageSpeed Insights Interpretation

### Scores
- **90-100**: Good (green)
- **50-89**: Needs improvement (orange)
- **0-49**: Poor (red)

### Key Metrics to Watch
- **First Contentful Paint (FCP)**: < 1.8s
- **Speed Index**: < 3.4s
- **Total Blocking Time**: < 200ms
- **Time to Interactive**: < 3.8s

## Monitoring Tools

### Free Tools
- **PageSpeed Insights**: page-specific analysis
- **Google Search Console**: field data (real users)
- **Chrome DevTools**: lab data (simulated)
- **Web Vitals Extension**: real-time monitoring

### Monitoring Frequency
- **Daily**: check for regressions
- **Weekly**: full audit
- **Monthly**: trend analysis

## Pitfalls
1. Don't chase perfect score — focus on real user experience
2. Don't ignore mobile — 60%+ traffic is mobile
3. Don't sacrifice UX for speed (remove all images)
4. Don't ignore field data (real users) vs lab data
5. Don't forget to test after template changes

## Verification
- LCP < 2.5s on mobile
- INP < 200ms
- CLS < 0.1
- PageSpeed score > 80 (mobile)
- No regressions after template changes
