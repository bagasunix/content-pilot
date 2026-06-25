"""System clock adapter."""
from __future__ import annotations

from datetime import datetime, timezone

from ..application.ports import Clock


class SystemClock(Clock):
    def now_iso(self) -> str:
        return datetime.now(timezone.utc).isoformat()
