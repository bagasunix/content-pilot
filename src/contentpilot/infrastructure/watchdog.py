"""Watchdog — timeout enforcement for pipeline phases.

Problem: Worker hang → stall forever (no timeout mechanism).
Solution: Track started_at + deadline per phase. Expired phases auto-fail.

Usage:
    from contentpilot.infrastructure.watchdog import PhaseWatchdog
    wd = PhaseWatchdog(journal_path, deadline_seconds=1800)
    stale = wd.check_stale()       # returns list of stale phases
    wd.mark_failed(idea_id, phase) # auto-fail a stale phase
"""
from __future__ import annotations

import json
import logging
import os
import time
from dataclasses import dataclass

log = logging.getLogger(__name__)

# default deadline per phase (seconds) — override via env
DEFAULT_DEADLINES = {
    "researching": int(os.getenv("WD_RESEARCHING_SECS", "3600")),    # 1h
    "outlined":    int(os.getenv("WD_OUTLINED_SECS", "1800")),       # 30m
    "drafted":     int(os.getenv("WD_DRAFTED_SECS", "3600")),        # 1h
    "reviewing":   int(os.getenv("WD_REVIEWING_SECS", "1800")),      # 30m
    "gated":       int(os.getenv("WD_GATED_SECS", "86400")),         # 24h (waiting human)
    "approved":    int(os.getenv("WD_APPROVED_SECS", "86400")),      # 24h (waiting publish)
}


@dataclass
class StalePhase:
    """A phase that has exceeded its deadline."""
    idea_id: str
    phase: str
    started_at: str
    elapsed_secs: float
    deadline_secs: float


class PhaseWatchdog:
    """Monitor journal.jsonl for stale (timed-out) phases."""

    def __init__(self, journal_path, deadlines: dict | None = None):
        """
        Args:
            journal_path: Path to journal.jsonl
            deadlines: {phase_name: max_seconds} override
        """
        self._path = journal_path
        self._deadlines = deadlines or DEFAULT_DEADLINES

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

    def _latest_phases(self) -> dict[str, dict]:
        """Build {idea_id: {phase, started_at, timestamp}} from journal."""
        phases: dict[str, dict] = {}
        for entry in self._read_journal():
            idea_id = entry.get("idea_id", "")
            to_stage = entry.get("to", "")
            ts = entry.get("timestamp", "")
            meta = entry.get("metadata", {})

            # Track the latest stage for each idea
            if idea_id not in phases or ts > phases[idea_id].get("timestamp", ""):
                phases[idea_id] = {
                    "phase": to_stage,
                    "started_at": meta.get("started_at", ts),
                    "timestamp": ts,
                }
        return phases

    def check_stale(self, now: float | None = None) -> list[StalePhase]:
        """Return list of phases that have exceeded their deadline.

        Args:
            now: current time (epoch seconds), defaults to time.time()
        """
        now = now or time.time()
        phases = self._latest_phases()
        stale = []

        for idea_id, info in phases.items():
            phase = info["phase"]
            deadline = self._deadlines.get(phase)
            if deadline is None:
                continue  # no deadline for this phase

            started_str = info.get("started_at", "")
            if not started_str:
                continue  # can't compute without started_at

            try:
                # Parse ISO timestamp
                started_epoch = self._parse_iso(started_str)
                if started_epoch is None:
                    continue
            except Exception:
                continue

            elapsed = now - started_epoch
            if elapsed > deadline:
                stale.append(StalePhase(
                    idea_id=idea_id,
                    phase=phase,
                    started_at=started_str,
                    elapsed_secs=round(elapsed, 1),
                    deadline_secs=deadline,
                ))

        return stale

    def mark_failed(self, idea_id: str, phase: str, reason: str = "") -> dict:
        """Append a failure entry to journal for a stale phase.

        Returns the journal entry dict.
        """
        from datetime import datetime, timezone
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "idea_id": idea_id,
            "from": phase,
            "to": phase,  # stays in same phase (failed, not advanced)
            "by": "watchdog",
            "metadata": {
                "gate": "fail",
                "failures": [reason or f"phase '{phase}' exceeded deadline"],
                "watchdog": True,
            },
        }
        with self._path.open("a") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        log.warning("Watchdog: auto-failed %s phase '%s' — %s", idea_id, phase, reason)
        return entry

    @staticmethod
    def _parse_iso(ts: str) -> float | None:
        """Parse ISO-8601 timestamp to epoch seconds."""
        from datetime import datetime
        try:
            # handle +07:00, Z, etc.
            ts_clean = ts.replace("Z", "+00:00")
            dt = datetime.fromisoformat(ts_clean)
            return dt.timestamp()
        except (ValueError, TypeError):
            return None

    def summary(self) -> dict:
        """Return watchdog status summary."""
        stale = self.check_stale()
        return {
            "total_phases_tracked": len(self._latest_phases()),
            "stale_count": len(stale),
            "deadlines": self._deadlines,
            "stale": [
                {
                    "idea_id": s.idea_id,
                    "phase": s.phase,
                    "elapsed": f"{s.elapsed_secs}s / {s.deadline_secs}s",
                }
                for s in stale
            ],
        }
