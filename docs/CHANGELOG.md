# ContentPilot — Changelog

## 2026-06-30 — UI & Pagination Update

### Added
- **Google OAuth flow** — simplified, multi-user, server-side token storage
  - Server endpoints: `/api/google/auth-url`, `/api/google/callback`, `/api/google/status`, `/api/google/token`, `/api/google/disconnect`
  - GSC endpoints: `/api/google/gsc/sites`, `/api/google/gsc/add`
  - `google_tokens` table in PostgreSQL (per-user, keyed by `license_key`)
  - Client: Connect Google proxies to server, credential caching (local → server → cache)
  - `credentials.json` (OAuth client) bundled in server, NOT in git
  - `.gitignore` updated: `credentials.json`, `token.json`, `.license` excluded
- **Pagination** — reusable macro `_pagination.html` with prev/next + page numbers + ellipsis
  - Articles page: `/articles?page=1` (10/page, DB query, filter support)
  - Trending page: `/trending?page=1` (12/page, in-memory)
  - Pipeline page: `/pipeline?page=1` (10/page, DB query)
  - Indexing page: `/indexing?page=1` (10/page, DB query)
  - API: `/api/articles?page=1&per_page=10` (JSON, auth required)
- **Missing API endpoints** — `/api/eeat/score`, `/api/wordpress/publish`
- **CLI wrappers** — `scripts/pipeline.py`, `scripts/setup_wizard.py` (per SYSTEM_RULES.md)
- **Standalone mode** — `standalone/start.sh`, `standalone/requirements.txt`
- **Config template** — `config.template.yaml` now includes `ai:` and `notifications:` sections

### Fixed
- **Server Disconnected overlay** — changed from full-screen overlay to dismissible top banner (no longer blocks content)
- **License validation** — server-first validation with local fallback when server unreachable
- **License format** — now supports `SB-XXXX-XXXX-XXXX` (4 segments) per docs, plus legacy 3-segment format
- **Config path** — code now reads `config/config.yaml` (per INSTALLATION.md), falls back to `workspace/config.yaml`
- **API auth** — `/api/articles` now requires login + blog connection (was public)
- **Pricing consistency** — CONCEPT-INTERNAL.md updated to match FAQ ($9-19 Pro, $49-99 Enterprise)

### Updated
- **README.md** — project structure now lists all directories
- **SYSTEM_RULES.md** — CLI paths corrected
- **web/app.py** — +154 lines (pagination, API endpoints, license validation)
- **web/static/css/desktop.css** — removed 50+ lines overlay CSS, replaced with inline Tailwind
- **web/templates/base.html** — server status banner redesign
- **contentpilot.spec** — added API module to hiddenimports

### Database
- Full reset: all tables truncated (articles, pipeline_runs, job_queue, users, blogs, etc.)
- Added `google_tokens` table (per-user OAuth tokens, keyed by `license_key`)
- Local files cleaned: journal.jsonl, drafts/, cache/

### Architecture Notes
- Client: `~/Project/content-pilot/` (port 8080)
- Server: `~/Project/content-pilot-server/` (port 5001)
- Blog-lifecycle: `~/Project/blog-lifecycle/` (worker)
