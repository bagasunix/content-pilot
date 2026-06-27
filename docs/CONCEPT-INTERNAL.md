# ContentPilot — Internal Concept

> Catatan internal arsitektur dan concept. BUKAN untuk publik.
> Last updated: 2026-06-27
> Updated: Online-backed + BYOM flexibility

## Overview

ContentPilot = blog automation desktop app dengan full pipeline (research → write → SEO → publish).

```
User (blogger)
    ↓
┌─────────────────────────────────────┐
│  CONTENTPILOT CLIENT (Desktop App)  │
│  ├── PyWebView (native window)      │
│  ├── Flask (localhost server)       │
│  ├── Dashboard (HTML/CSS/JS)        │
│  └── Settings (AI provider config)  │
└──────────────┬──────────────────────┘
               ↓ HTTP
┌─────────────────────────────────────┐
│  CONTENTPILOT SERVER                │
│  ├── Flask API endpoints            │
│  ├── Celery + Redis (background)    │
│  ├── PostgreSQL (database)          │
│  ├── AI Provider (BYOM - any)       │
│  ├── Research Tools (Exa, YouTube)  │
│  ├── Quality Gates (19 AI-tells)    │
│  ├── E-E-A-T Scoring (AI)          │
│  ├── Indexing Monitor (Google API)  │
│  └── Publisher (Blogger/WP API)     │
└─────────────────────────────────────┘
```

**Important:** ContentPilot = ONLINE-BACKED (not offline-first).
Most features require internet: research, AI, publishing, indexing.

## Core Concept: Zero Editing, Full Automation

User flow:
1. Buka ContentPilot dashboard
2. Lihat suggestions dari server (pre-computed, cronjob)
3. Klik "Start" → trigger blog-lifecycle pipeline
4. Monitor: Research → Draft → Gate → Approved
5. Klik "Approve" → publish ke Blogger
6. Selesai!

TIDAK ada:
- ❌ Manual writing
- ❌ Manual editing
- ❌ Draft editing
- ❌ Quality gate manual

## Design Journey

### Technology Choices

**Next.js → Cancelled → PyWebView**

```
 Awalnya consider Next.js untuk modern SPA experience.
 Tapi: ContentPilot = offline-capable product
├── Next.js butuh Node.js runtime (ribet untuk user)
├── User harus install Python + Node.js
├── Overhead besar untuk product yang harusnya simple
└── VERDICT: ❌ Overkill

 PyWebView dipilih:
├── Flask stays (Python only)
├── Native window feel (bukan browser tab)
├── User experience: double-click icon → window muncul
├── Dependencies: Python + PyQt5 + qtpy
└── VERDICT: ✅ Simple, native feel
```

**Testing Results:**
- PyWebView + Qt backend works on WSL
- Flask serves on localhost, PyWebView wraps in native window
- Tested: login page loads, Tailwind CSS renders
- Dependencies: pywebview, PyQt5, PyQtWebEngine, qtpy

**Cross-Platform Build:**
- GitHub Actions workflow ready
- Builds: .exe (Windows), .app (Mac), binary (Linux)
- PyInstaller bundles Python + all deps
- Trigger: push tag v* → auto build

### Architecture Clarification

**ContentPilot is NOT a writing tool**

```
 Awalnya assume ContentPilot = writing tool (draft + edit + publish).
 Tapi: blog-lifecycle sudah handle semua itu.
├── ContentPilot = monitoring + intelligence
├── Blog-lifecycle = worker (does the work)
├── Server = brain (provides intelligence)
└── Client = remote control (monitor + trigger + approve)
```

**ContentPilot is NOT fully offline**

```
 Awalnya assume "offline-first" product.
 Tapi: needs internet for many things:
├── Research → search, competitor analysis
├── Publishing → Blogger API
├── Smart suggestions → server intelligence
├── Trending → HN, Google News, Reddit
├── License → server validation
├── Rules update → server
└── Only truly offline: draft editing + quality gates
```

**Better positioning: "Online-backed application"**
- Core editing: offline capable
- Smart features: online required
- "Write and edit articles offline"
- "Smart suggestions require internet"

## Relationship with Blog-Lifecycle

```
Blog-lifecycle = UPSTREAM (source of truth, always updated)
├── Core pipeline logic
├── Quality gates (AI-tells, SEO, hoax links)
├── Domain rules
└── Multi-agent protocol

ContentPilot = DOWNSTREAM (productized, commercial)
├── Fork dari blog-lifecycle
├── + License system (CP- keys)
├── + Web UI (Flask + PyWebView)
├── + Desktop wrapper
├── + Server intelligence
└── Should TRACK upstream changes
```

## Sync Rules

**SYNC (core logic, no commercial value):**
- domain/gates.py
- domain/stages.py
- domain/article.py
- domain/link_validator.py
- domain/images.py
- infrastructure/*.py (14 files)

**DON'T SYNC (commercial differentiators):**
- license.py
- seo.py
- blogger.py
- web/*
- .github/*
- Server endpoints

**Prinsip:**
- Blog-lifecycle = "brain" (logic, rules, pipeline)
- ContentPilot = "product" (brain + UI + license + desktop + server)
- Sync = update the "brain"
- Don't sync = keep the "product" unique

## Offline Capability

```
Bisa offline:
├── View cached dashboard data
├── Edit settings
└── View cached suggestions

Butuh internet:
├── Server suggestions (brain)
├── Pipeline execution (blog-lifecycle)
├── Publishing (Blogger API)
├── Trending topics
└── License validation
```

## User-Configurable Cronjobs

Users can set their own scheduling:

```
Suggestion Frequency:
├── Every 1 hour (Business only)
├── Every 2 hours (Pro+)
├── Every 6 hours (Free+) ← default
└── Every 12 hours (Free+)

Analysis Frequency:
├── Every 12 hours (Pro+)
└── Every 24 hours (Free+) ← default
```

## Tier-Based Limits

| Tier | Suggestions/Day | Analysis | Trending | Rate Limit |
|------|-----------------|----------|----------|------------|
| Free | 1 | 1/week | 1/day | 20 req/day |
| Pro ($29/mo) | 12 | 1/day | 6/day | 100 req/day |
| Business ($99/mo) | 24 | 1/day | 24/day | 500 req/day |

## Job Queue System

Priority: Business > Pro > Free

Max concurrent: 50 analysis jobs
Max queue: 200 jobs
Overflow: reject with "server busy, try later"

## Database Additions

```sql
user_schedules (user's cronjob settings)
job_queue (pending/processing/completed jobs)
rules (AI-tells, hoax domains, SEO rules)
trending_cache (cached trending topics)
suggestions_cache (cached suggestions per user)
```

## Code Protection

```
PyInstaller .exe:
├── Bundle Python bytecode, not source
├── But: .pyc bisa di-decompile
├── Semi-protection, bukan full protection
└── Cukup untuk target user biasa

Protection levels:
├── Level 2: PyInstaller .exe (current)
├── Level 3: Nuitka (compile to C) — harder
├── Level 4: PyArmor (runtime obfuscation) — commercial
└── Level 5: Server-side logic — best (code never shared)

Recommendation:
├── PyInstaller sudah cukup untuk sekarang
├── Focus: user acquisition, feature iteration
└── Code protection bukan competitive advantage
```

## Key Decisions

1. ContentPilot = zero editing, full automation
2. Server = brain + scheduler (proactive suggestions)
3. Blog-lifecycle = worker (does the work)
4. Client = remote control + monitor
5. User can configure cronjob frequency
6. Tier-based limits prevent server overload
7. Sync from blog-lifecycle = core logic only
8. PyWebView for desktop (not Next.js)
9. ContentPilot is NOT fully offline
10. ContentPilot is NOT a writing tool

## Files

- Client: ~/Project/content-pilot/
- Server: ~/Project/content-pilot-server/
- Blog-lifecycle: ~/Project/blog-lifecycle/
- Architecture review: docs/architecture-review-v2.md
