# AGENTS.md — Blog Lifecycle System (bagasunix.com)

> Entry point untuk semua agent. Baca ini dulu, lalu baca file yang relevan untuk role kamu.
> Berlaku untuk SEMUA model (Gemini, mimo, Claude, GPT).

---

## Hierarchy

```
User → Command Center → Orchestrator → Worker
```

- User hanya bicara ke Command Center.
- Command Center hanya beri tugas ke Orchestrator.
- Worker TIDAK BOLEH terima instruksi dari User atau Command Center.
- Orchestrator satu-satunya pengendali workflow.

## Pipeline

```
idea → researching → outlined → drafted → reviewing → gated → approved → published → promoted
```

WIP limit: 3. Publish mode: draft. Autonomy: gated (human approval wajib).

## Rules Fundamental

1. **Sequential** — satu worker selesai, baru dispatch berikutnya
2. **Semua lewat scripts** — `pipeline.py`, `discord_dispatch.py`, `auto_pipeline.py`
3. **Protocol header wajib** — pesan antar bot HARUS punya `TARGET:` + `STATUS: PENDING` (line-based). Anti-loop plugin drop pesan tanpa header.
4. **Worker tidak boleh**: memanggil worker lain, mengubah workflow, menentukan step berikutnya, menghubungi Command Center
5. **Retry max 3x** — oleh Orchestrator saja. Worker tidak boleh retry sendiri
6. **[DONE] = stop** — setelah kirim [DONE], jangan reply lagi. Orchestrator terima [DONE], worker lain ignore.
7. **Dilarang**: emoji doang, "standby"/"noted", message kosong, ping-pong loop — anti-loop plugin enforce ini

## Dimana Baca Detail

| Topik | File | Isi |
|-------|------|-----|
| **Overview system** | `SOUL.md` | Pipeline, architecture, voice, gate, file structure, known issues |
| **18 formal rules** | `SYSTEM_RULES.md` | Hierarchy, communication, state, retry, logging rules |
| **Inter-bot protocol** | `workspace/INTER-BOT-PROTOCOL.md` | Channel structure, boleh/diam/dilarang, [DONE] signal |
| **Anti-loop plugin** | `plugins/anti-loop/__init__.py` | Protocol-level message filter, TARGET/STATUS enforcement |
| **Test plan** | `docs/test-plan-multi-bot-v2.md` | 25 test scenarios untuk protocol, anti-loop, pipeline |
| **Voice guide** | `workspace/voice.md` | BagasUnix persona, tone, diksi, frasa khas/terlarang |
| **Blog config** | `workspace/config.yaml` | Domain, blog_id, Google services, known issues |

### Per-Role SOUL.md

Setiap bot punya SOUL.md sendiri di `profiles/`. Baca yang sesuai role kamu:

| Role | File | Isi |
|------|------|-----|
| **Orchestrator** | `profiles/blog_orchestrator-SOUL.md` | Pipeline commands, dispatch templates, error recovery, bot IDs |
| **Researcher** | `profiles/researcher-SOUL.md` | Research brief template, quality criteria, tools, failure modes |
| **Writer** | `profiles/writer-SOUL.md` | Voice rules inline, 19 AI-tell blacklist, article templates, self-check |
| **Editor** | `profiles/editor-SOUL.md` | Gate details inline, fact-check process, review.md template |
| **Analyst** | `profiles/analyst-SOUL.md` | SEO checklist, weighted scoring 0-100, readability grading |
| **Imagery** | `profiles/imagery-SOUL.md` (direct file) | Image specs, naming convention, alt text rules, tools |
| **Publisher** | `profiles/publisher-SOUL.md` (direct file) | Pre-flight checklist, publish commands, safety rules |

Semua profile punya: task-driven protocol, anti-loop rules, role-specific response voice & examples.

### Reference Docs (Opsional, Baca Kalau Butuh Detail)

| Topik | File |
|-------|------|
| Writer cheatsheet | `workspace/reference/writer-cheatsheet.md` |
| Editor checklist | `workspace/reference/editor-checklist.md` |
| Architecture review | `docs/architecture-review.md` |
| Setup credentials | `docs/setup-credentials.md` |
| Test scenarios | `docs/test-scenarios.md` |
| Reliability architecture | `docs/RELIABILITY_ARCHITECTURE.md` |

---

## Architecture (Ringkas)

Clean/hexagonal architecture — dependency mengarah ke dalam:

```
interface/ → application/ → domain/ → (no deps)
                  ↓
           infrastructure/
```

- **domain/** — entities, gates (19 AI-tells, SEO, hoax), ports
- **application/** — use cases (research, draft, review, gate, publish)
- **infrastructure/** — adapters (Blogger API, DraftStore, Discord, Watchdog, Throttle)
- **interface/** — CLI (`cli.py` → `scripts/pipeline.py`)

Pipeline = pure Python, TIDAK pakai LLM. Stage transitions, gates, journal = deterministic. LLM hanya dipakai bot untuk generate content.

---

## CLI Quick Reference

```bash
cd ~/Project/blog-lifecycle

# Pipeline
python3 scripts/pipeline.py status
python3 scripts/pipeline.py next
python3 scripts/pipeline.py research "<topic>"
python3 scripts/pipeline.py draft <idea_id>
python3 scripts/pipeline.py review <idea_id>
python3 scripts/pipeline.py gate <idea_id>
python3 scripts/pipeline.py approve <idea_id>
python3 scripts/pipeline.py push-draft <idea_id>
python3 scripts/pipeline.py attach-images <idea_id>
python3 scripts/pipeline.py watchdog
python3 scripts/pipeline.py reconcile

# Discord dispatch
python3 scripts/discord_dispatch.py dispatch --to <worker> --msg "pesan"
python3 scripts/discord_dispatch.py report --msg "status"
python3 scripts/discord_dispatch.py read --channel <worker> --limit 5

# Auto pipeline (full sequential via Discord)
python3 scripts/auto_pipeline.py <topic>

# Tests
python3 -m unittest discover -s tests -t . -v
```

---

## Quality Gate (domain/gates.py)

**Hard fail:**
- 19 AI-tell phrases (lihat writer SOUL.md untuk daftar lengkap)
- Word count < 600
- Missing SEO fields (title, meta_description, slug, keywords)
- No featured image
- Unresolved markers (TODO/FIXME/HACK/XXX)
- Hoax domain links (30 blocklisted)
- Dead links (HTTP 404/410)

**Warnings:** "Anda" usage, excessive em-dashes, tutorial tanpa code blocks

---

## Discord Channel Map

| Channel | Bot | Channel ID | Bot ID |
|---------|-----|------------|--------|
| staff-chat | Orchestrator + CC | 1514656047611121784 | — |
| orchestrator | Orchestrator | 1514656283897106463 | 1516806348875104367 |
| researcher | Researcher | 1517360169430814850 | 1516807610685194250 |
| writer | Writer | 1517360180214366219 | 1516808178564599931 |
| editor | Editor | 1517360191702827068 | 1516808772406870046 |
| analyst | Analyst | 1517360201727082596 | 1516808427622633604 |
| imagery | Imagery | 1517360212087148675 | 1516809145934675968 |
| publisher | Publisher | 1517360222275108967 | 1516809765769052200 |

Sumber kebenaran: `discord_routing.env`

---

## Troubleshooting

### Pipeline status kosong
```bash
cat workspace/journal.jsonl | tail -5
python3 -c "from blog.infrastructure.paths import Workspace; print(Workspace.default())"
```

### Gate FAIL — AI-tells
```bash
grep -i "di era digital\|sangat penting\|tidak dapat dipungkiri" workspace/drafts/<idea_id>/draft.md
```
Fix: rewrite pakai voice guide.

### Gate FAIL — link dead/hoax
```bash
python3 -c "
from blog.domain.link_validator import validate_links
from pathlib import Path
body = Path('workspace/drafts/<idea_id>/draft.md').read_text().split('---', 2)[-1]
print(validate_links(body).failures)
"
```

### OAuth token expired
```bash
ls -la workspace/token.json
# Re-setup: lihat docs/setup-credentials.md
```

### Bot not responding
```bash
systemctl --user list-units 'hermes-gateway-*' --no-pager
systemctl --user restart hermes-gateway-<profile>.service
journalctl --user -u hermes-gateway-<profile>.service --no-pager -n 20
```

### WIP limit tercapai
```bash
python3 scripts/pipeline.py status
# Selesaikan atau drop artikel yang stuck
```

### Lock file nyangkut
```bash
find workspace/drafts/ -name "*.lock" -delete
```

### Bot loop / ping-pong
Cek: anti-loop plugin loaded (`journalctl` grep "anti-loop"), protocol headers (TARGET/STATUS di pesan), channel isolation. Plugin di `plugins/anti-loop/` auto-drop casual bot-to-bot replies.

---

## Pitfalls

1. JANGAN skip quality gates — mechanical dulu, baru human
2. JANGAN auto-approve — `approve` = gate MANUAL, never automate
3. JANGAN tulis tanpa voice.md — output generik = auto-fail
4. JANGAN pakai "Anda" — voice guide minta "kamu"/"sobat"
5. JANGAN tulis AI-tells — frasa generic = hard fail gate
6. JANGAN lupa WIP limit — cek status sebelum mulai baru
7. JANGAN publish live — `push-draft` = unpublished draft, go-live = manual
8. JANGAN edit skill di `~/.hermes/skills/` — edit di sini, karena symlink
9. JANGAN force overwrite `.lock` files — ada concurrent write protection
10. JANGAN bypass Orchestrator — semua task lewat chain: CC → Orchestrator → Worker

---

> Backup AGENTS.md lama (1687 lines): `AGENTS.md.bak`
> Slim version ini: ~190 lines. Detail per-role ada di masing-masing SOUL.md.
