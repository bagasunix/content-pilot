# SOUL.md — Blog Lifecycle System (bagasunix.com)

## Apa Ini

Sistem multi-agent pipeline produksi artikel blog untuk **bagasunix.com** (Blogger).
7 bot Hermes yang dikoordinasi via Discord, dikendalikan 1 orchestrator, semua lewat scripts.

Pipeline: `idea → researching → outlined → drafted → reviewing → gated → approved → published`

Blog ini punya 142 post (2014-2024) tapi dormant sejak 2024. Misi: hidupkan kembali dengan konten berkualitas, voice personal, tanpa AI-tell.

---

## Hierarchy

```
User
  └── Command Center (main Hermes gateway, port 8642, bot ID 1514647800024010954)
        └── Blog Orchestrator (port 8651, bot ID 1516806348875104367)
              ├── Researcher
              ├── Writer
              ├── Editor
              ├── Analyst
              ├── Imagery
              └── Publisher
```

User hanya bicara ke Command Center. Command Center hanya beri tugas ke Orchestrator. Orchestrator satu-satunya yang routing ke Worker. Worker tidak boleh terima instruksi langsung dari User atau Command Center.

---

## Architecture

Clean/hexagonal architecture. 4 layer, dependency mengarah ke dalam:

```
interface/  →  application/  →  domain/  →  (no deps)
                    ↓
             infrastructure/
```

- **domain/** — entities (Article, IdeaBank), value objects, gates (19 AI-tell checks, SEO validation, hoax domain list), ports (interfaces)
- **application/** — use cases (research, draft, review, gate, publish), orchestrator logic
- **infrastructure/** — adapters (Blogger API, DraftStore, DiscordNotifier, Watchdog, Reconciler, Throttle, JobWorkspace)
- **interface/** — CLI entry point (`cli.py` → `scripts/pipeline.py`)

Tests ada di `tests/` dengan in-memory fakes untuk semua ports.

---

## Aturan Fundamental

### 1. Semua operasi lewat scripts
```bash
python3 ~/Project/blog-lifecycle/scripts/pipeline.py <command>
python3 ~/Project/blog-lifecycle/scripts/discord_dispatch.py <command>
python3 ~/Project/blog-lifecycle/scripts/auto_pipeline.py <topic>
```
Jangan manipulasi state manual. Jangan kirim Discord message manual. Selalu pakai scripts.

### 2. Sequential, bukan parallel
Satu worker selesai dulu, baru dispatch ke worker berikutnya. Jangan dispatch ke 2 worker sekaligus. Urutan default: Researcher → Writer → Editor → Analyst → Imagery → Publisher.

### 3. Human approval wajib sebelum publish
`autonomy: gated` — setiap artikel butuh approval eksplisit user sebelum di-push ke Blogger. Tidak ada auto-publish. `publish_mode: draft` — bahkan setelah approve, artikel di-upload sebagai UNPUBLISHED draft di Blogger.

### 4. WIP limit = 3
Maksimal 3 artikel in-flight. Jangan mulai artikel baru kalau 3 masih jalan.

### 5. [DONE] = stop
Kalau worker kirim `[DONE]`, task selesai. Jangan reply, jangan lanjut. Orchestrator yang tentukan step berikutnya.

---

## Pipeline Commands

```bash
# Status semua artikel
pipeline.py status

# Mulai riset topik baru
pipeline.py research <topic>

# Lanjut ke draft (setelah research selesai)
pipeline.py draft <idea_id>

# Kirim ke review (setelah draft selesai)
pipeline.py review <idea_id>

# Jalankan quality gate (mechanical check)
pipeline.py gate <idea_id>

# Human approval
pipeline.py approve <idea_id>

# Push ke Blogger sebagai draft
pipeline.py push-draft <idea_id>

# Attach images ke draft
pipeline.py attach-images <idea_id>

# Watchdog — detect stale articles
pipeline.py watchdog

# Reconcile — fix inconsistent state
pipeline.py reconcile
```

`pipeline.py full`, `pipeline.py start`, dan `pipeline.py run-job` sengaja di-block. Harus lewat Discord orchestrator atau `auto_pipeline.py`.

---

## Discord Routing

**Guild**: Command Server (`1514656047611121784`)

Setiap bot punya dedicated channel. Bot hanya boleh kirim di channel sendiri + staff-chat (via mention). Channel IDs ada di `discord_routing.env` — satu-satunya sumber kebenaran untuk Discord IDs.

```bash
# Dispatch task ke worker
discord_dispatch.py dispatch --to <worker> --msg "pesan"

# Lapor ke Command Center
discord_dispatch.py report --msg "status"

# Baca response worker
discord_dispatch.py read --channel <worker> --limit 5
```

### Communication rules
- **Boleh kirim**: sedang kerja + report hasil, di-mention + ada pertanyaan, selesai + [DONE]
- **Harus diam**: tidak di-mention, bot lain sedang kerja, sudah kirim [DONE]
- **Dilarang**: emoji doang, "standby"/"noted", message kosong, reply ke message bukan untukmu, ping-pong loop

---

## Quality Gate

Gate di `blog/domain/gates.py` — mechanical check, bukan AI judgment.

**Hard fail** (block progression):
- 19 banned AI-tell phrases ("di era digital", "panduan lengkap", "dalam artikel ini", dll)
- Word count < 600
- Missing SEO fields (title, meta_description, slug, keywords)
- No featured image
- Unresolved markers (TODO/FIXME/HACK/XXX)
- Hoax domain links (30 blocklisted domains)
- Dead links (HTTP 404/410)

**Warnings** (logged, tidak block):
- "Anda" instead of "kamu"/"sobat"
- Excessive em-dashes
- Tutorial tanpa code blocks

Gate punya self-heal: auto-fill missing SEO fields dari draft content sebelum evaluasi.

---

## Voice — BagasUnix

Artikel harus terasa ditulis manusia. Referensi lengkap: `workspace/voice.md`

**Inti**:
- Bahasa Indonesia informal, campur EN-ID natural (istilah teknis English, penjelasan Indonesia)
- Sapaan: "sobat", "kamu" — BUKAN "Anda"
- Tone: santai kayak ngobrol, bukan dosen. Antusias tapi genuine.
- Kalimat pendek, paragraf 2-3 kalimat max
- Pengalaman pribadi wajib — artikel tanpa personal touch = gagal
- Emoticon hemat: ^_^ :D :v max 1-2x per artikel

**Frasa khas**: "langsung aja", "semoga bermanfaat", "Gimana?", "BACA JUGA"

**Dilarang keras**: "Di era digital...", "menjadi sumber daya yang sangat berharga", "hadir sebagai solusi", "Perlu diingat bahwa...", "Tidak dapat dipungkiri...", "Sebagai penutup..."

---

## Message Protocol

Format pesan antar bot (line-based, bukan bracket):

**Orchestrator → Worker (dispatch):**
```
<@bot_id>
TARGET: researcher
STATUS: PENDING

TASK_ID: BLOG-003
WORKFLOW_ID: WF-001

Riset topik: Cara Install Redis di Ubuntu 24.04.
```
`discord_dispatch.py` auto-inject `TARGET:` dan `STATUS: PENDING`. Orchestrator cukup tulis TASK_ID, WORKFLOW_ID, dan instruksi.

**Worker → Orchestrator (selesai):**
```
[DONE] Research brief selesai.

TASK_ID: BLOG-003
OUTPUT: workspace/drafts/BLOG-003/research-brief.md
Primary keyword: install redis ubuntu 24.04
```

**Worker → Orchestrator (gagal):**
```
TASK_ID: BLOG-003
STATUS: FAILED
ERROR: Search API down.
```

Anti-loop plugin (`plugins/anti-loop/`) enforce protocol ini:
- Worker HANYA proses pesan dengan `TARGET: <role>` + `STATUS: PENDING`
- Worker SKIP `[DONE]`, emoji, "ok", acknowledgment, pesan tanpa header
- Orchestrator ALLOW `[DONE]` (perlu tau worker selesai)
- Bracket format `[TARGET:x][STATUS:PENDING]` masih supported (backward compat)

---

## Reliability

- **Anti-loop plugin**: protocol-level message filter — drop casual bot-to-bot replies, enforce TARGET/STATUS headers
- **Watchdog**: detect artikel stale (research >1h, draft >1h, gated/approved >24h)
- **Reconciler**: on-boot reconciliation artikel in-flight
- **Throttle**: token-bucket rate limiter, 2 max concurrent, 1 req/sec
- **Job Workspace**: isolated directory per job di `workspace/jobs/`
- **File Lock**: spin-lock via .lock file, 5s timeout
- **Retry**: max 3x per worker. Gagal? Mark FAILED, lapor Command Center. Jangan retry lebih dari 3x.

---

## File Structure

```
~/Project/blog-lifecycle/
├── AGENTS.md              # Master reference (1687 lines) — semua agent specs
├── SYSTEM_RULES.md        # 18 formal rules
├── SOUL.md                # (file ini)
├── blog/                  # Python source (clean arch)
│   ├── domain/            # entities, gates, ports
│   ├── application/       # use cases
│   ├── infrastructure/    # adapters (Blogger, Discord, store)
│   └── interface/         # CLI
├── plugins/               # anti-loop protocol filter (symlinked ke ~/.hermes/plugins/)
├── profiles/              # 7 Hermes bot profiles (symlinked ke ~/.hermes/profiles/)
├── skills/                # blog skills (symlinked ke ~/.hermes/skills/content)
├── scripts/               # 14 operational scripts
├── workspace/
│   ├── config.yaml        # Blog config, auth, Google services
│   ├── voice.md           # Writing style guide
│   ├── idea-bank.md       # 11 queued topics
│   ├── INTER-BOT-PROTOCOL.md
│   ├── journal.jsonl      # Pipeline run log
│   ├── drafts/            # Per-article working directories
│   ├── state/jobs/        # Job state tracking
│   └── published/         # Published article archives
├── templates/             # 5 article templates
├── tests/                 # 8 test files
├── docs/                  # 13 doc files
└── data/                  # Content calendar
```

---

## Blog Config

- **Domain**: bagasunix.com (Blogger, custom domain, SSL)
- **Blog ID**: 4609850969039659967
- **Template**: LinkMagz v3.2.0 (Mas Sugeng)
- **AdSense**: active (6 units)
- **Auth**: OAuth token via dfuck1504@gmail.com

---

## Known Issues

1. Blog dormant sejak 2024 — 0 post di 2025-2026
3. Structured data publisher name = "Blogger" (harusnya "BagasUnix")
4. twitter:site dan twitter:creator tidak diset
5. Featured image pakai lazyload (buruk untuk LCP)
6. jQuery 3.6.0 render-blocking (tidak di-defer)
7. ~100KB+ inline CSS dari template
8. Pipeline belum pernah complete full run — journal kosong, published/ kosong
9. Worker bot services perlu provider/API key fix (OpenRouter 401, xiaomi 429) sebelum bisa jalan

---

## Yang TIDAK Boleh

- Publish langsung ke live (selalu draft dulu)
- Skip human approval
- Dispatch parallel ke multiple workers
- Worker komunikasi langsung antar sesama (harus via orchestrator)
- Manipulasi state tanpa lewat pipeline.py
- Kirim Discord message tanpa lewat discord_dispatch.py
- Retry worker lebih dari 3x
- Sembunyikan error dari Command Center
- Tulis artikel tanpa load voice.md dulu
- Pakai frasa AI-tell yang sudah dilarang di gate

---

## Relationship dengan AGENTS.md

SOUL.md ini adalah ringkasan eksekutif. AGENTS.md (1687 lines) adalah referensi lengkap untuk semua agent specs, protocol details, error handling, dan edge cases. Kalau ada konflik, AGENTS.md yang menang. Kalau butuh detail spesifik per-bot, baca AGENTS.md.

SYSTEM_RULES.md berisi 18 formal rules yang berlaku untuk semua agent. Tidak boleh diubah tanpa perintah user.
