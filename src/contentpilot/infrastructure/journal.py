"""Append-only JSONL journal adapter — the source of truth for stage history."""
from __future__ import annotations

import json
from datetime import datetime, timezone

from ..application.ports import JournalPort
from .paths import Workspace


class JsonlJournal(JournalPort):
    def __init__(self, ws: Workspace):
        self._path = ws.journal

    def append(self, idea_id, from_stage, to_stage, metadata=None) -> None:
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "idea_id": idea_id,
            "from": from_stage,
            "to": to_stage,
            "by": "pipeline-runner",
        }
        if metadata:
            entry["metadata"] = metadata
        with self._path.open("a") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def latest_stages(self) -> dict:
        stages: dict = {}
        if not self._path.exists() or self._path.stat().st_size == 0:
            return stages
        for line in self._path.read_text().strip().split("\n"):
            if not line:
                continue
            entry = json.loads(line)
            idea_id = entry.get("idea_id")
            if idea_id:
                stages[idea_id] = {"stage": entry["to"], "updated": entry["timestamp"]}
        return stages

    def get_failures(self, idea_id: str) -> list[dict]:
        failures = []
        if not self._path.exists():
            return failures
        for line in self._path.read_text().splitlines():
            entry = json.loads(line)
            if entry.get("idea_id") == idea_id and entry.get("metadata", {}).get("gate") == "fail":
                failures.append(entry)
        return failures

    def mark_complete(self, idea_id: str, phase: str, result: dict | None = None) -> None:
        """Explicit completion signal — append an atomic completion entry.

        This replaces implicit detection (polling latest stage + file mtime).
        The 'complete' metadata field makes it unambiguous.
        """
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "idea_id": idea_id,
            "from": phase,
            "to": phase,  # stays in same phase (completed, not advanced)
            "by": "pipeline-runner",
            "metadata": {
                "complete": True,
                **(result or {}),
            },
        }
        with self._path.open("a") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def is_phase_complete(self, idea_id: str, phase: str) -> bool:
        """Check if a phase has an explicit completion entry."""
        if not self._path.exists():
            return False
        for line in self._path.read_text().splitlines():
            entry = json.loads(line)
            if (entry.get("idea_id") == idea_id
                    and entry.get("from") == phase
                    and entry.get("metadata", {}).get("complete") is True):
                return True
        return False
