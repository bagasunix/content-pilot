# ContentPilot — Implementation Plan

> Roadmap implementasi semua konsep. Server + Client + Integration.
> Last updated: 2026-06-26

---

## Phase 0: Foundation (Week 1)

### Server Setup

```
Task 0.1: Database Schema
├── Create tables: user_schedules, job_queue, rules, trending_cache, suggestions_cache
├── Run schema.sql updates
├── Test: connection, CRUD operations
└── File: schema.sql (update)

Task 0.2: Server Structure
├── Organize central-server/ folder
├── Add requirements: redis (queue), celery (background jobs)
├── Update requirements.txt
└── File: central-server/requirements.txt

Task 0.3: Environment Setup
├── .env file: DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
├── .env file: REDIS_URL, SECRET_KEY
├── .env.example for documentation
└── File: .env, .env.example
```

### Client Setup

```
Task 0.4: Client Structure
├── Verify web/desktop.py works
├── Verify Flask app starts
├── Test PyWebView window opens
└── File: web/desktop.py, web/app.py

Task 0.5: Requirements Update
├── Add pywebview, PyQt5, qtpy to requirements.txt
├── Verify: pip install -r requirements.txt
└── File: requirements.txt
```

---

## Phase 1: Server Brain (Week 2-3)

### 1.1 Rules Engine

```
Task 1.1.1: Rules Model
├── Create: server/rules.py
├── Functions: get_rules(), update_rules(), sync_from_blog_lifecycle()
├── Data: AI-tells (19 phrases), hoax domains (30), SEO rules
└── File: central-server/rules.py

Task 1.1.2: Rules API
├── GET /api/rules → serve current rules
├── PUT /api/rules → admin update rules
├── POST /api/rules/sync → sync from blog-lifecycle
├── Auth: license key
└── File: central-server/app.py (add routes)

Task 1.1.3: Rules Sync
├── Script: sync_rules.py
├── Fetch gates.py from blog-lifecycle
├── Extract AI-tells, hoax domains
├── Update rules table
└── File: central-server/sync_rules.py
```

### 1.2 Content Analysis Engine

```
Task 1.2.1: Blog Analyzer
├── Create: server/analyzer.py
├── Class: BlogAnalyzer
├── Methods: analyze_blog(), extract_categories(), find_gaps()
├── Input: blog URL/domain
├── Output: categories, style, gaps
└── File: central-server/analyzer.py

Task 1.2.2: Analysis API
├── POST /api/blog/analyze → analyze user's blog
├── GET /api/blog/analysis/:user_id → get cached analysis
├── Auth: license key
├── Rate limit: per tier
└── File: central-server/app.py (add routes)

Task 1.2.3: Analysis Cronjob
├── Job: analyze_user_blogs()
├── Frequency: 24h (configurable per user)
├── Process: fetch posts → analyze → cache results
├── Queue: job_queue table
└── File: central-server/jobs/analysis.py
```

### 1.3 Topic Suggestion Engine

```
Task 1.3.1: Suggestion Generator
├── Create: server/suggestions.py
├── Class: SuggestionEngine
├── Methods: generate_suggestions(), score_relevance(), rank_topics()
├── Input: blog analysis + trending data
├── Output: ranked suggestions with reasons
└── File: central-server/suggestions.py

Task 1.3.2: Suggestion API
├── GET /api/suggest → get suggestions for user
├── GET /api/suggest/:blog_id → get suggestions for specific blog
├── Auth: license key
├── Rate limit: per tier
└── File: central-server/app.py (add routes)

Task 1.3.3: Suggestion Cronjob
├── Job: generate_user_suggestions()
├── Frequency: 6h (configurable per user)
├── Process: combine gaps + trends → score → rank → cache
├── Queue: job_queue table
└── File: central-server/jobs/suggestions.py
```

### 1.4 Trending Aggregation

```
Task 1.4.1: Trend Fetcher
├── Create: server/trending.py
├── Class: TrendAggregator
├── Methods: fetch_hn(), fetch_google_news(), fetch_reddit()
├── Input: category filter
├── Output: trending topics with heat scores
└── File: central-server/trending.py

Task 1.4.2: Trending API
├── GET /api/trends → get trending topics
├── GET /api/trends/:category → get by category
├── Auth: license key
├── Cache: trending_cache table
└── File: central-server/app.py (add routes)

Task 1.4.3: Trending Cronjob
├── Job: aggregate_trends()
├── Frequency: 1h
├── Process: fetch → categorize → score → cache
├── Queue: job_queue table
└── File: central-server/jobs/trending.py
```

### 1.5 Job Queue System

```
Task 1.5.1: Queue Manager
├── Create: server/queue.py
├── Class: JobQueue
├── Methods: enqueue(), dequeue(), process(), get_status()
├── Priority: Business > Pro > Free
├── Max concurrent: 50 jobs
└── File: central-server/queue.py

Task 1.5.2: Queue API
├── GET /api/queue/status → user's queue status
├── GET /api/queue/history → user's job history
├── POST /api/queue/trigger → manually trigger job
├── Auth: license key
└── File: central-server/app.py (add routes)

Task 1.5.3: Queue Worker
├── Create: server/worker.py
├── Process: dequeue → execute → update status
├── Handle: retries, failures, timeouts
├── Run: background process or cron
└── File: central-server/worker.py
```

### 1.6 User Scheduling

```
Task 1.6.1: Schedule Manager
├── Create: server/schedule.py
├── Class: UserSchedule
├── Methods: get_schedule(), update_schedule(), check_limits()
├── Table: user_schedules
└── File: central-server/schedule.py

Task 1.6.2: Schedule API
├── GET /api/user/schedule → get user's settings
├── PUT /api/user/schedule → update user's settings
├── GET /api/user/limits → get user's rate limits
├── Auth: license key
└── File: central-server/app.py (add routes)
```

---

## Phase 2: Client Dashboard (Week 3-4)

### 2.1 Dashboard UI

```
Task 2.1.1: Dashboard Template
├── Update: web/templates/dashboard.html
├── Show: pipeline status, articles, suggestions
├── Style: Tailwind CSS + Alpine.js
├── Auto-refresh: every 30s
└── File: web/templates/dashboard.html

Task 2.1.2: Dashboard API
├── GET /api/dashboard → aggregated dashboard data
├── GET /api/pipeline/status → pipeline status
├── GET /api/articles → article list
├── Auth: session-based
└── File: web/app.py (add routes)
```

### 2.2 Suggestions Page

```
Task 2.2.1: Suggestions Template
├── Create: web/templates/suggestions.html
├── Show: ranked topic suggestions
├── Show: reasons (gap + trending)
├── Action: "Start" button → trigger pipeline
└── File: web/templates/suggestions.html

Task 2.2.2: Suggestions Integration
├── Fetch from server: GET /api/suggest
├── Cache locally: workspace/cache/suggestions.json
├── Fallback: use cache if offline
└── File: web/app.py (add route)
```

### 2.3 Settings Page

```
Task 2.3.1: Settings Template
├── Update: web/templates/settings.html
├── Sections: Blog config, AI provider, Cronjob settings
├── Cronjob: suggestion frequency, analysis frequency
├── Save: PUT /api/user/schedule
└── File: web/templates/settings.html

Task 2.3.2: Settings API
├── GET /api/settings → load user settings
├── PUT /api/settings → save user settings
├── Sync with server: PUT /api/user/schedule
└── File: web/app.py (add routes)
```

### 2.4 Monitor Page

```
Task 2.4.1: Monitor Template
├── Create: web/templates/monitor.html
├── Show: real-time pipeline progress
├── Show: quality gate results
├── Show: publishing status
├── Auto-refresh: every 10s
└── File: web/templates/monitor.html

Task 2.4.2: Monitor API
├── GET /api/monitor → real-time status
├── GET /api/monitor/:idea_id → specific article status
├── WebSocket or polling for live updates
└── File: web/app.py (add routes)
```

---

## Phase 3: Integration (Week 4-5)

### 3.1 Server ↔ Client

```
Task 3.1.1: Client Sync Module
├── Create: src/contentpilot/sync/
├── Files: client.py, cache.py, updater.py
├── Function: fetch suggestions, rules, trends from server
├── Cache: workspace/cache/
├── Fallback: use cache if offline
└── File: src/contentpilot/sync/

Task 3.1.2: Client Startup Sync
├── On app start: check server for updates
├── Download: rules, suggestions, trends
├── Cache locally
└── File: web/app.py (add startup hook)
```

### 3.2 Server ↔ Blog-Lifecycle

```
Task 3.2.1: Rules Sync Script
├── Create: sync_rules.py
├── Fetch: domain/gates.py from blog-lifecycle
├── Extract: AI-tells, hoax domains
├── Update: server rules table
├── Schedule: every 7d
└── File: central-server/sync_rules.py

Task 3.2.2: Pipeline Trigger
├── API: POST /api/pipeline/trigger
├── Input: topic, user_id
├── Process: send task to blog-lifecycle
├── Output: task_id, status
└── File: central-server/app.py (add route)
```

### 3.3 Client ↔ Blog-Lifecycle

```
Task 3.3.1: Pipeline Trigger (Client)
├── Button: "Start" → POST /api/pipeline/trigger
├── Server sends task to blog-lifecycle
├── Client polls for status updates
└── File: web/app.py (add route)

Task 3.3.2: Status Polling
├── Client polls: GET /api/pipeline/status/:task_id
├── Update dashboard: real-time progress
├── Notify user: on completion or failure
└── File: web/app.py (add route)
```

---

## Phase 4: Polish & Deploy (Week 5-6)

### 4.1 Testing

```
Task 4.1.1: Server Tests
├── Test: all API endpoints
├── Test: cronjob execution
├── Test: queue system
├── Test: rate limiting
└── File: tests/

Task 4.1.2: Client Tests
├── Test: dashboard loads
├── Test: settings save/load
├── Test: suggestions display
├── Test: desktop wrapper
└── File: tests/
```

### 4.2 Deployment

```
Task 4.2.1: Server Deploy
├── Setup: VPS (DigitalOcean/Hetzner)
├── Setup: PostgreSQL, Redis
├── Deploy: gunicorn + nginx
├── Setup: SSL certificate
└── File: docs/DEPLOY.md

Task 4.2.2: Client Deploy
├── Build: PyInstaller for all platforms
├── Test: Windows, Mac, Linux
├── Publish: GitHub Releases
└── File: .github/workflows/build.yml
```

### 4.3 Documentation

```
Task 4.3.1: User Documentation
├── Update: docs/INSTALLATION.md
├── Update: docs/USER_MANUAL.md
├── Update: docs/FAQ.md
└── File: docs/

Task 4.3.2: Developer Documentation
├── Update: docs/API_DOCUMENTATION.md
├── Update: docs/SETUP_GUIDE.md
└── File: docs/
```

---

## Timeline

```
Week 1: Foundation (DB, server structure, client verification)
Week 2: Server Brain Part 1 (rules, analysis, suggestions)
Week 3: Server Brain Part 2 (trending, queue, scheduling) + Client Dashboard
Week 4: Client Dashboard (suggestions, settings, monitor) + Integration
Week 5: Integration (server↔client, server↔blog-lifecycle, client↔blog-lifecycle)
Week 6: Polish, testing, deployment
```

## Dependencies

```
Phase 0 → Phase 1 (foundation before brain)
Phase 1 → Phase 2 (server before client)
Phase 2 → Phase 3 (client before integration)
Phase 3 → Phase 4 (integration before polish)
```

## Risk

```
HIGH:
├── Server overload (mitigated by queue + rate limits)
├── Blog-lifecycle sync drift (mitigated by rules sync)
└── Rate limit abuse (mitigated by tier-based limits)

MEDIUM:
├── Content analysis accuracy
├── Suggestion relevance
└── Trending data freshness

LOW:
├── Desktop wrapper bugs
├── Dashboard UI issues
└── Documentation gaps
```
