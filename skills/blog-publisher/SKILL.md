---
name: blog-publisher
description: "Use when an approved blog draft is ready to be uploaded, formatted, and published on Blogger — Blogger API v3 deployment, schema validation."
category: publisher
tags: [publish, blogger, api, deployment, formatting, schema]
---

# Blog Publisher (Blogger Deployment)

## Blogger API v3 Setup

### Authentication
- OAuth 2.0 with {{EMAIL}}
- Token refresh handling
- API quota: 100 requests/100 seconds

### API Endpoints
- **List posts**: GET /blogs/{blogId}/posts
- **Get post**: GET /blogs/{blogId}/posts/{postId}
- **Create post**: POST /blogs/{blogId}/posts
- **Update post**: PUT /blogs/{blogId}/posts/{postId}

## Publishing Workflow

### Step 1: Pre-Publish Check
- [ ] Content approved by editor
- [ ] Images optimized (< 100KB)
- [ ] Alt text on all images
- [ ] Internal links added
- [ ] Meta description written

### Step 2: Format for Blogger
- **Title**: < 60 characters for SEO
- **Labels**: 2-3 relevant categories
- **Search Description**: meta description
- **URL slug**: keyword-rich, short

### Step 3: Upload
```python
from googleapiclient.discovery import build

service = build('blogger', 'v3', credentials=creds)

post = {
    'kind': 'blogger#post',
    'title': 'Article Title',
    'content': '<html content>',
    'labels': ['Technology', 'Tutorial']
}

service.posts().insert(blogId=BLOG_ID, body=post).execute()
```

### Step 4: Post-Publish
- [ ] Verify published URL
- [ ] Check mobile rendering
- [ ] Submit URL to GSC
- [ ] Share on social media

## Schema Markup

### Article Schema (Required)
```json
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "Article Title",
  "datePublished": "2026-06-20",
  "dateModified": "2026-06-20",
  "author": {
    "@type": "Person",
    "name": "Bagas"
  },
  "publisher": {
    "@type": "Organization",
    "name": "BagasUnix",
    "logo": {
      "@type": "ImageObject",
      "url": "https://{{DOMAIN}}/logo.png"
    }
  }
}
```

### Validation
- Use Google Rich Results Test
- Check for errors/warnings
- Verify all required fields
- Monitor in GSC

## Error Handling

### Common Errors
- **401 Unauthorized**: token expired → refresh
- **403 Forbidden**: API quota exceeded → wait
- **400 Bad Request**: invalid content → fix HTML
- **500 Internal**: Blogger issue → retry

### Retry Logic
1. Attempt 1: immediate
2. Attempt 2: wait 5 seconds
3. Attempt 3: wait 30 seconds
4. After 3 failures: log error, notify user

## Pitfalls
1. Don't publish without editor approval
2. Don't forget schema markup
3. Don't ignore mobile rendering
4. Don't skip GSC submission
5. Don't forget social media sharing

## Verification
- Post published successfully
- Schema valid and rendering
- Mobile rendering correct
- URL submitted to GSC
- Social media shared
