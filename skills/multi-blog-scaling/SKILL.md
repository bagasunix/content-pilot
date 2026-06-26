---
name: multi-blog-scaling
description: "Use when managing multiple blogs from a single pipeline — cross-blog scheduling, resource allocation."
category: orchestrator
tags: [multi-blog, scaling, resource-allocation, scheduling]
---

# Multi-Blog Scaling

## Scaling Model

### Blog Tiers

**Tier 1: Core Blog ({{DOMAIN}})**
- Priority: highest
- Frequency: 3-4 posts/week
- Resources: full pipeline
- Quality: highest standard

**Tier 2: Niche Blog**
- Priority: high
- Frequency: 2-3 posts/week
- Resources: shared pipeline
- Quality: good standard

**Tier 3: Experimental Blog**
- Priority: medium
- Frequency: 1-2 posts/week
- Resources: minimal pipeline
- Quality: acceptable

## Resource Allocation

### Bot Distribution
- **Orchestrator**: manages all blogs
- **Researcher**: shared across blogs
- **Writer**: 1 writer per blog
- **Editor**: shared across blogs
- **Analyst**: per-blog analytics
- **Publisher**: per-blog publishing

### Time Allocation
- **Research**: 30% core, 50% niche, 20% experimental
- **Writing**: 40% core, 40% niche, 20% experimental
- **Editing**: 50% core, 30% niche, 20% experimental
- **Publishing**: per-blog, automated

## Cross-Blog Scheduling

### Calendar Management
- **Master calendar**: all blogs combined
- **Per-blog calendar**: individual scheduling
- **Conflict resolution**: no same topic same day
- **Cross-promotion**: share across blogs

### Scheduling Rules
- **No overlap**: different topics per day
- **Balance**: even distribution across blogs
- **Priority**: core blog gets first pick
- **Flexibility**: experimental can shift

## Quality Control

### Per-Blog Standards
- **Core**: highest quality, full pipeline
- **Niche**: good quality, standard pipeline
- **Experimental**: acceptable quality, minimal pipeline

### Cross-Blog Consistency
- **Brand voice**: different per blog
- **Visual identity**: per-blog branding
- **SEO**: per-blog optimization
- **Analytics**: per-blog tracking

## Scaling Challenges

### Content Quality
- **Risk**: spreading too thin
- **Solution**: prioritize core blog
- **Metric**: maintain quality score > 7

### Resource Constraints
- **Risk**: bot overload
- **Solution**: load balancing, queuing
- **Metric**: average response time < 5 min

### Management Overhead
- **Risk**: complexity
- **Solution**: automation, templates
- **Metric**: time per blog decreasing

## Pitfalls
1. Don't scale before core blog stable
2. Don't ignore quality for quantity
3. Don't overload bots
4. Don't forget per-blog analytics
5. Don't skip cross-blog coordination

## Verification
- Multi-blog pipeline working
- Resources allocated correctly
- Quality maintained across blogs
- Scheduling conflict-free
- Analytics per blog
