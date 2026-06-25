"""Generic notifier — prints stage transitions to console.

A notify must never break the pipeline, so this never raises.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from ..application.ports import NotifierPort

STAGE_MESSAGES = {
    "researching": ("🔍", "Researching"),
    "outlined": ("📋", "Outline ready"),
    "drafted": ("✍️", "Draft created"),
    "reviewing": ("👀", "Ready for review"),
    "gated": ("🚦", "Eligible — awaiting approval"),
    "approved": ("✅", "Approved for go-live"),
    "published": ("🎉", "Published"),
}


class ConsoleNotifier(NotifierPort):
    """Prints stage notifications to stdout and optionally to a log file."""

    def __init__(self, log_path: Path | None = None):
        self.log_path = log_path

    def notify(self, idea_id: str, from_stage: str, to_stage: str, title: str = "") -> None:
        emoji, label = STAGE_MESSAGES.get(to_stage, ("📢", to_stage))
        msg = f"{emoji} {idea_id}: {from_stage} → {to_stage}"
        if title:
            msg += f" ({title})"

        print(msg)

        if self.log_path:
            try:
                ts = datetime.now(timezone.utc).isoformat()
                line = f"[{ts}] {msg}\n"
                self.log_path.parent.mkdir(parents=True, exist_ok=True)
                with open(self.log_path, "a") as f:
                    f.write(line)
            except Exception:
                pass  # never break pipeline

    def error(self, idea_id: str, stage: str, error: str) -> None:
        msg = f"❌ {idea_id} @ {stage}: {error}"
        print(msg)

        if self.log_path:
            try:
                ts = datetime.now(timezone.utc).isoformat()
                line = f"[{ts}] ERROR {msg}\n"
                self.log_path.parent.mkdir(parents=True, exist_ok=True)
                with open(self.log_path, "a") as f:
                    f.write(line)
            except Exception:
                pass
