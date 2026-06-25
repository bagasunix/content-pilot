"""Reconcile-on-boot — reconstruct in-flight state from journal at startup.

Problem: Orchestrator restart → forgets what's in-flight → jobs stall forever.
Solution: On boot, read journal.jsonl → identify stale phases → trigger watchdog.

Usage:
    from blog.infrastructure.reconciler import Reconciler
    r = Reconciler(journal_path, watchdog)
    report = r.reconcile()
    # report = {'stale': [...], 'healthy': [...], 'recovered': [...]}
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field

log = logging.getLogger(__name__)

# stages that are "active" (in-flight, not terminal)
ACTIVE_STAGES = frozenset({
    "researching", "outlined", "drafted", "reviewing", "gated", "approved",
})

# terminal stages (pipeline done for this article)
TERMINAL_STAGES = frozenset({"published", "promoted"})


@dataclass
class ReconcileReport:
    """Result of a reconciliation pass."""
    total_articles: int = 0
    active_articles: int = 0
    stale_phases: list[dict] = field(default_factory=list)
    healthy_phases: list[dict] = field(default_factory=list)
    recovered: list[dict] = field(default_factory=list)
    actions_taken: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "total_articles": self.total_articles,
            "active_articles": self.active_articles,
            "stale_count": len(self.stale_phases),
            "healthy_count": len(self.healthy_phases),
            "recovered_count": len(self.recovered),
            "actions": self.actions_taken,
            "stale": self.stale_phases,
            "healthy": self.healthy_phases,
        }


class Reconciler:
    """Reconstruct in-flight state from journal + watchdog at startup."""

    def __init__(self, journal_path, watchdog=None):
        """
        Args:
            journal_path: Path to journal.jsonl
            watchdog: PhaseWatchdog instance (optional — if provided, auto-fails stale)
        """
        self._path = journal_path
        self._watchdog = watchdog

    def _read_journal(self) -> list[dict]:
        if not self._path.exists():
            return []
        entries = []
        for line in self._path.read_text().splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        return entries

    def _build_state(self) -> dict[str, dict]:
        """Build current state from journal: {idea_id: {stage, updated, ...}}."""
        state: dict[str, dict] = {}
        for entry in self._read_journal():
            idea_id = entry.get("idea_id", "")
            if not idea_id:
                continue
            to_stage = entry.get("to", "")
            ts = entry.get("timestamp", "")
            meta = entry.get("metadata", {})

            if idea_id not in state or ts > state[idea_id].get("updated", ""):
                state[idea_id] = {
                    "stage": to_stage,
                    "updated": ts,
                    "metadata": meta,
                    "from": entry.get("from", ""),
                }
        return state

    def reconcile(self, auto_fail: bool = True) -> ReconcileReport:
        """Run reconciliation.

        Args:
            auto_fail: if True and watchdog is set, auto-fail stale phases

        Returns:
            ReconcileReport with findings
        """
        report = ReconcileReport()
        state = self._build_state()
        report.total_articles = len(state)

        for idea_id, info in state.items():
            stage = info["stage"]

            if stage not in ACTIVE_STAGES:
                continue  # terminal or initial — nothing to reconcile

            report.active_articles += 1
            phase_info = {
                "idea_id": idea_id,
                "stage": stage,
                "updated": info["updated"],
                "from": info["from"],
            }

            # check if stale via watchdog
            if self._watchdog:
                stale = self._watchdog.check_stale()
                stale_match = [s for s in stale if s.idea_id == idea_id]
                if stale_match:
                    s = stale_match[0]
                    phase_info["stale_reason"] = (
                        f"elapsed {s.elapsed_secs}s > deadline {s.deadline_secs}s"
                    )
                    report.stale_phases.append(phase_info)

                    if auto_fail:
                        self._watchdog.mark_failed(
                            idea_id, stage,
                            reason=f"reconcile: {phase_info['stale_reason']}"
                        )
                        report.actions_taken.append(
                            f"auto-failed {idea_id} stage '{stage}' (stale)"
                        )
                        report.recovered.append(phase_info)
                    continue

            report.healthy_phases.append(phase_info)

        log.info(
            "Reconcile: %d total, %d active, %d stale, %d healthy",
            report.total_articles, report.active_articles,
            len(report.stale_phases), len(report.healthy_phases),
        )
        return report

    def summary(self) -> dict:
        """Quick summary without auto-failing."""
        return self.reconcile(auto_fail=False).to_dict()
