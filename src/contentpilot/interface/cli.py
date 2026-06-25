"""CLI — composition root + argv dispatch.

This is the only place that knows about both the concrete infrastructure and
the use cases: it wires them together (the composition root) and translates
argv into service calls + presenter output.
"""
from __future__ import annotations

import sys

from ..application.service import PipelineService
from ..domain import stages
from ..infrastructure.clock import SystemClock
from ..infrastructure.config import YamlConfig
from ..infrastructure.draft_store import FileDraftStore
from ..infrastructure.idea_bank import MarkdownIdeaBank
from ..infrastructure.image_host import DriveImageHost
from ..infrastructure.journal import JsonlJournal
from ..infrastructure.notifier import ConsoleNotifier
from ..infrastructure.paths import Workspace
from ..infrastructure.publisher import BloggerPublisher
from . import presenter

USAGE = """\
Blog Lifecycle Pipeline Runner — FASE 0-3 (state machine + mechanical gates)

Usage:
    pipeline.py status                 — semua artikel + stage
    pipeline.py next                   — pilih ide berikutnya (hormati WIP)
    pipeline.py research <topic>       — FASE 1: buat research brief
    pipeline.py draft <idea_id>        — FASE 2: buat draft template (cek WIP)
    pipeline.py review <idea_id>       — drafted → reviewing (editor mulai)
    pipeline.py gate <idea_id>         — jalankan gate mekanis; lolos → gated
    pipeline.py approve <idea_id>      — human go-live gate: gated → approved
    pipeline.py publish <idea_id>      — approved → published (butuh OAuth)
    pipeline.py push-draft <idea_id>   — upload approved ke Blogger sbg DRAFT post (butuh OAuth)
    pipeline.py attach-images <idea_id>— host gambar + sisip ke body + update post (jalan stlh push-draft)
    pipeline.py start <idea_id>        — research + draft dari idea-bank (id stabil) ← automation
    pipeline.py full <topic>           — research + draft topik ad-hoc (id dari slug judul)
    pipeline.py run-job <job_id> <topic> — research dalam isolated job workspace

Reliability:
    pipeline.py watchdog               — cek phase yang stale (melebihi deadline)
    pipeline.py watchdog --auto-fail   — auto-fail phase yang stale + log ke journal
    pipeline.py reconcile              — scan journal, identifikasi in-flight, report status
    pipeline.py reconcile --auto-fail  — reconcile + auto-fail stale phases
    pipeline.py throttle-stats         — tampilkan statistika rate limiter
"""


def build_service(workspace: Workspace | None = None) -> PipelineService:
    """Composition root: wire concrete adapters into the use-case service."""
    ws = (workspace or Workspace.default()).ensure_dirs()
    return PipelineService(
        config=YamlConfig(ws),
        clock=SystemClock(),
        journal=JsonlJournal(ws),
        drafts=FileDraftStore(ws),
        idea_bank=MarkdownIdeaBank(ws),
        notifier=ConsoleNotifier(log_path=ws.notify_log),
        publisher=BloggerPublisher(ws),
        image_host=DriveImageHost(),
    )


def _emit(lines: list[str]) -> None:
    print("\n".join(lines))


def _run_pipeline(steps: list, idea_id: str, header: str) -> int:
    d = dict(steps)
    print(f"═══ {header} ═══")
    print(f"    idea_id: {idea_id}\n")
    print("── FASE 1: Research ──")
    _emit(presenter.render_research(d["research"]))
    if "draft" not in d:
        return 0  # research blocked / idea not found — stop
    print("\n── FASE 2: Draft ──")
    _emit(presenter.render_draft(d["draft"]))
    print(f"\n═══ Done ═══")
    print(f"Draft siap diisi agent. Lalu: review {idea_id} → gate {idea_id}")
    return 0


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv:
        print(USAGE)
        return 0

    svc = build_service()
    cmd, rest = argv[0], argv[1:]

    if cmd == "status":
        _emit(presenter.render_status(svc.status()))
    elif cmd == "next":
        _emit(presenter.render_next(svc.next_idea()))
    elif cmd == "research" and rest:
        _emit(presenter.render_research(svc.research(" ".join(rest))))
    elif cmd == "draft" and rest:
        _emit(presenter.render_draft(svc.draft(rest[0])))
    elif cmd == "review" and rest:
        _emit(presenter.render_review(svc.review(rest[0])))
    elif cmd == "gate" and rest:
        lines, code = presenter.render_gate(svc.gate(rest[0]))
        _emit(lines)
        return code
    elif cmd == "approve" and rest:
        _emit(presenter.render_approve(svc.approve(rest[0])))
    elif cmd == "publish" and rest:
        pub = svc.publish(rest[0])
        _emit(presenter.render_publish(pub))
        if pub.status == "pre_publish_fail":
            return 1
    elif cmd == "push-draft" and rest:
        lines, code = presenter.render_push_draft(svc.push_draft(rest[0]))
        _emit(lines)
        return code
    elif cmd == "attach-images" and rest:
        lines, code = presenter.render_attach_images(svc.attach_images(rest[0]))
        _emit(lines)
        return code
    elif cmd == "full" and rest:
        _emit(presenter.render_research(svc.research(" ".join(rest))))
        _emit(presenter.render_draft(svc.draft(rest[0])))
    elif cmd == "start" and rest:
        _emit(presenter.render_research(svc.research(" ".join(rest))))
        _emit(presenter.render_draft(svc.draft(rest[0])))

    # ── reliability commands ──────────────────────────────────────────────
    elif cmd == "watchdog":
        from ..infrastructure.watchdog import PhaseWatchdog
        ws = Workspace.default()
        wd = PhaseWatchdog(ws.journal)
        auto_fail = "--auto-fail" in rest
        if auto_fail:
            stale = wd.check_stale()
            for s in stale:
                wd.mark_failed(s.idea_id, s.phase,
                               reason=f"deadline exceeded ({s.elapsed_secs}s > {s.deadline_secs}s)")
            print(f"Watchdog: {len(stale)} stale phases auto-failed")
        else:
            report = wd.summary()
            print(f"Watchdog: {report['total_phases_tracked']} phases tracked, "
                  f"{report['stale_count']} stale")
            for s in report["stale"]:
                print(f"  STALE: {s['idea_id']} phase '{s['phase']}' — {s['elapsed']}")
        return 0

    elif cmd == "reconcile":
        from ..infrastructure.reconciler import Reconciler
        from ..infrastructure.watchdog import PhaseWatchdog
        ws = Workspace.default()
        wd = PhaseWatchdog(ws.journal)
        rc = Reconciler(ws.journal, watchdog=wd)
        auto_fail = "--auto-fail" in rest
        report = rc.reconcile(auto_fail=auto_fail)
        print(f"Reconcile: {report.total_articles} total, "
              f"{report.active_articles} active, "
              f"{len(report.stale_phases)} stale, "
              f"{len(report.healthy_phases)} healthy")
        for a in report.actions_taken:
            print(f"  ACTION: {a}")
        for h in report.healthy_phases:
            print(f"  OK: {h['idea_id']} stage '{h['stage']}'")
        return 0

    elif cmd == "throttle-stats":
        from ..infrastructure.throttle import get_throttled_client
        client = get_throttled_client()
        stats = client.stats()
        print("Throttle stats:")
        for k, v in stats.items():
            print(f"  {k}: {v}")
        return 0
    else:
        print(USAGE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
