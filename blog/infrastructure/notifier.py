"""Discord notifier — stage alerts via `hermes send`, with failure logging.

A notify must never break the pipeline, so this never raises. But unlike a
fire-and-forget-to-/dev/null, it now records every failed send to a log file
so a misconfigured channel / down gateway is visible instead of silent.
"""
from __future__ import annotations

import subprocess
from datetime import datetime, timezone
from pathlib import Path

from ..application.ports import NotifierPort

DEFAULT_CHANNEL = "discord:#📝・content-workshop"
SEND_TIMEOUT = 20

STAGE_MESSAGES = {
    "researching": ("🔍", "Researching"),
    "outlined": ("📋", "Outline ready"),
    "drafted": ("✍️", "Draft created"),
    "reviewing": ("👀", "Ready for review"),
    "gated": ("🚦", "Eligible — awaiting approval"),
    "approved": ("✅", "Approved for go-live"),
    "published": ("🎉", "Published"),
    "promoted": ("📣", "Distributed"),
}

_ACTION_HINTS = {
    "reviewing": "\n   ⏳ Menunggu review — cek draft di `~/Project/blog-lifecycle/workspace/drafts/`",
    "drafted": "\n   Next: Hermes agent fills the draft via blog-writer",
    "gated": "\n   ⛔ Butuh approval manual sebelum go-live (autonomy:gated)",
    "published": "\n   🔗 Check live URL",
}


class DiscordNotifier(NotifierPort):
    def __init__(self, channel: str = DEFAULT_CHANNEL, log_path: Path | None = None):
        self._channel = channel
        self._log_path = log_path

    def _format(self, idea_id, from_stage, to_stage, title) -> str:
        emoji, label = STAGE_MESSAGES.get(to_stage, ("🔄", to_stage.capitalize()))
        display = title or idea_id.replace("-", " ").title()
        msg = f"{emoji} **{label}:** {display}\n   `{from_stage}` → `{to_stage}`"
        return msg + _ACTION_HINTS.get(to_stage, "")

    def _log_failure(self, idea_id, to_stage, reason) -> None:
        if not self._log_path:
            return
        line = (f"{datetime.now(timezone.utc).isoformat()}\t{idea_id}\t->{to_stage}"
                f"\t{self._channel}\tFAIL: {reason}\n")
        try:
            self._log_path.parent.mkdir(parents=True, exist_ok=True)
            with self._log_path.open("a") as f:
                f.write(line)
        except Exception:
            pass  # logging must never break the pipeline either

    def notify(self, idea_id, from_stage, to_stage, title="") -> None:
        msg = self._format(idea_id, from_stage, to_stage, title)
        try:
            res = subprocess.run(
                ["hermes", "send", "-t", self._channel, msg],
                capture_output=True, text=True, timeout=SEND_TIMEOUT,
            )
            if res.returncode != 0:
                self._log_failure(idea_id, to_stage,
                                  (res.stderr or res.stdout or "non-zero exit").strip())
        except Exception as e:
            self._log_failure(idea_id, to_stage, repr(e))


class NullNotifier(NotifierPort):
    """No-op notifier (tests, or when notifications are unwanted)."""

    def notify(self, idea_id, from_stage, to_stage, title="") -> None:
        return None
