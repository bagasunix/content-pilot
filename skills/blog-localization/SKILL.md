---
name: blog-localization
description: "Use when translating blog content between Indonesian and English — hreflang, cultural adaptation, SEO localization beyond translation."
category: writer
tags: [localization, translation, indonesian, english, hreflang, cultural]
---

# Blog Localization (Research-Based)

## Research Basis
- **Google**: hreflang is signal (not directive)
- **Moz**: localization > translation
- **Ahrefs**: localized keywords have different search volume

## Localization vs Translation

### Translation
- Word-for-word conversion
- Preserves original structure
- May miss cultural context

### Localization
- **Cultural adaptation** of meaning
- **Localized keywords** (not direct translation)
- **Cultural examples** (local brands, events)
- **Adapted tone** (Indonesian: more casual)

## hreflang Implementation

### Basic Tag
```html
<link rel="alternate" hreflang="id" href="https://{{DOMAIN}}/artikel-slug" />
<link rel="alternate" hreflang="en" href="https://{{DOMAIN}}/en/article-slug" />
<link rel="alternate" hreflang="x-default" href="https://{{DOMAIN}}/en/article-slug" />
```

### Rules
- **Bidirectional**: both pages must link to each other
- **Self-referencing**: each page includes its own hreflang
- **x-default**: fallback for unmatched languages
- **Consistent**: same URL structure per language

## Keyword Localization

### Direct Translation Pitfalls
- "SEO" → same in both languages
- "Backlink" → same in both languages
- "Traffic blog" → "blog traffic" (English) vs "traffic blog" (Indonesian)
- **Search volume differs** per language!

### Process
1. Find primary keyword in source language
2. Research equivalent in target language
3. Check search volume for target language
4. Use localized keyword (not direct translation)

## Cultural Adaptation

### Indonesian Blog Style
- **More casual** than English
- **Personal tone** preferred
- **Local examples** (Tokopedia, Shopee, etc.)
- **Indonesian colloquialisms** appropriate

### English Blog Style
- **Professional** but approachable
- **Data-driven** claims preferred
- **International examples** (Amazon, Shopify, etc.)
- **English idioms** acceptable

## Content Structure Differences

### Indonesian
- Longer introductions
- More personal anecdotes
- Conversational tone throughout
- Direct address: "kamu"

### English
- Hook-driven introductions
- Data and examples
- Professional tone
- Second person: "you"

## Workflow

### Step 1: Research
- Target language keyword research
- Cultural context analysis
- Competitor content in target language

### Step 2: Adaptation
- Rewrite for cultural context
- Localize examples and references
- Adjust tone for target audience
- Add hreflang tags

### Step 3: SEO
- Localized meta titles and descriptions
- Localized alt text for images
- Internal links in target language
- Submit to GSC per language version

## Pitfalls
1. **Don't auto-translate** — always human review
2. **Don't ignore search volume differences** per language
3. **Don't forget hreflang** — duplicate content risk
4. **Don't translate cultural references** — replace with local equivalents
5. **Don't assume same tone works** for both languages

## Verification
- Hreflang tags correct and bidirectional
- Localized keywords have search volume
- Cultural examples are target-audience relevant
- Content reads naturally in target language
- GSC shows correct language targeting
