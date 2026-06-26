# ============================================================
# SMART BLOGGER — SYSTEM RULES
# ============================================================

Tujuan:
Pipeline blog automation standalone. User jalankan CLI, pipeline jalan, artikel jadi.

# ============================================================
# 1. PIPELINE STAGES
# ============================================================

```
idea → researching → outlined → drafted → reviewing → gated → approved → published
```

Rules:
- Sequential — satu stage selesai, baru lanjut.
- WIP limit = 3 (max artikel in-flight).
- Publish mode = draft (butuh approval manual untuk go-live).

# ============================================================
# 2. CLI COMMANDS
# ============================================================

```bash
python3 scripts/pipeline.py status
python3 scripts/pipeline.py next
python3 scripts/pipeline.py research "<topic>"
python3 scripts/pipeline.py draft <idea_id>
python3 scripts/pipeline.py review <idea_id>
python3 scripts/pipeline.py gate <idea_id>
python3 scripts/pipeline.py approve <idea_id>
python3 scripts/pipeline.py push-draft <idea_id>
python3 scripts/pipeline.py attach-images <idea_id>
python3 scripts/pipeline.py full <topic>
python3 scripts/pipeline.py start <idea_id>
```

Rules:
- Semua operasi lewat CLI.
- Jangan manipulasi state manual.
- Jangan skip quality gates.

# ============================================================
# 3. QUALITY GATES
# ============================================================

Hard fail:
- 19 AI-tell phrases
- Word count < 600
- Missing SEO fields
- No featured image
- Unresolved markers (TODO/FIXME)
- Hoax domain links
- Dead links (404/410)

Warnings:
- "Anda" usage
- Excessive em-dashes
- Tutorial tanpa code blocks

Rules:
- Gate = mechanical check, bukan human judgment.
- Gate FAIL → back to writer untuk fix.
- Max 3 cycle gate-fix. Masih gagal? Mark FAILED.

# ============================================================
# 4. APPROVAL GATE
# ============================================================

- approve = human approval untuk go-live.
- JANGAN automate approval.
- Selalu draft dulu, baru approve.

# ============================================================
# 5. ERROR HANDLING
# ============================================================

- Retry max 3x per stage.
- Log semua error ke journal.jsonl.
- Watchdog detect stale phases.
- Reconcile auto-fix in-flight articles.

# ============================================================
# 6. FILE STRUCTURE
# ============================================================

```
workspace/
  drafts/<idea_id>/
    idea.md          — topik + angle
    research-brief.md — riset
    draft.md         — artikel
    review.md        — review notes
    analysis-report.md — SEO analysis
    assets/          — gambar
  journal.jsonl      — stage history
  idea-bank.md       — topik待写
  voice.md           — writing voice guide
  config.yaml        — blog config
```

# ============================================================
# 7. PUBLISH RULES
# ============================================================

- Publish mode = draft (Bukan live).
- Butuh OAuth token untuk push ke Blogger.
- Attach images setelah push-draft.
- Jangan publish tanpa quality gate lolos.
