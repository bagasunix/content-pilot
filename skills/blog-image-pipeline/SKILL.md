---
name: blog-image-pipeline
description: "Use when generating, optimizing, or managing images for blog — AI generation, stock sourcing, compression, alt text strategy."
category: imagery
tags: [images, optimization, ai-generation, stock, compression, alt-text]
---

# Blog Image Pipeline (Research-Based)

## Research Basis
- **Google**: high-quality images near relevant text improve ranking
- **Page speed**: images account for 50%+ of page weight
- **Visual search**: images drive discovery

## Image Generation

### AI Image Generation
- **DALL-E**: OpenAI, high quality
- **Midjourney**: artistic, creative
- **Stable Diffusion**: open source, customizable

### Prompt Template
```
[Subject] [Style] [Colors] [Composition] [Mood]
Example: "Blog analytics dashboard, flat design, blue and white, clean layout, professional"
```

### Stock Photo Sources
- **Unsplash**: free, high quality
- **Pexels**: free, good variety
- **Pixabay**: free, large library
- **Shutterstock**: paid, premium

## Image Optimization

### Compression
- **Target**: < 100KB per image
- **Tools**: TinyPNG, Squoosh, ShortPixel
- **Format**: WebP with fallback to JPEG

### Responsive Images
```html
<img srcset="image-300.webp 300w,
             image-600.webp 600w,
             image-900.webp 900w"
     sizes="(max-width: 600px) 100vw,
            (max-width: 900px) 50vw,
            33vw"
     src="image-600.webp"
     alt="Descriptive alt text">
```

### Lazy Loading
```html
<img src="image.webp" loading="lazy" alt="description">
```

## Alt Text Strategy

### Rules
- **Descriptive**: explain image content
- **Concise**: < 125 characters
- **Keyword-rich**: include target keyword naturally
- **No "image of"**: start directly with description

### Examples
- ❌ "Image of a laptop"
- ✅ "Dashboard showing blog analytics with traffic trends"

### Template
```
[Subject] [Action/State] [Context/Location]
Example: "Analytics dashboard displaying monthly traffic growth for technology blog"
```

## Image Placement

### Best Practices
- **Near relevant text**: helps Google understand context
- **Above fold**: hero image for engagement
- **In-content**: every 300-500 words
- **Before CTA**: visual break before action

### Image-Text Relationship
- Text near image helps Google understand image
- Image provides visual context for text
- Both benefit from proximity

## Workflow

### Step 1: Source
- Generate or find appropriate image
- Check licensing (Creative Commons)
- Verify quality and relevance

### Step 2: Optimize
- Compress (< 100KB)
- Convert to WebP
- Create responsive sizes

### Step 3: Add Metadata
- Write descriptive alt text
- Add caption if appropriate
- Include in sitemap

### Step 4: Place
- Position near relevant text
- Add lazy loading
- Test on mobile

## Pitfalls
1. Don't use images without proper licensing
2. Don't forget alt text (SEO + accessibility)
3. Don't use oversized images (page speed)
4. Don't use generic stock photos (authenticity)
5. Don't ignore mobile rendering

## Verification
- All images < 100KB
- Alt text on all images
- Responsive images implemented
- Lazy loading enabled
- Images in sitemap
