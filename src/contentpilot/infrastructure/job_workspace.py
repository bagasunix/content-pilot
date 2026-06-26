"""Job workspace — isolated working directory per job_id.

Problem: All jobs share workspace/drafts/<idea_id>.md → race condition when
         two jobs work on similar topics.
Solution: Namespace artifacts under workspace/jobs/<job_id>/ → full isolation.

Structure:
    workspace/jobs/<job_id>/
    ├── research/<idea_id>.md
    ├── drafts/<idea_id>.md
    ├── assets/<idea_id>/
    └── state.json

Usage:
    from contentpilot.infrastructure.job_workspace import JobWorkspace
    jw = JobWorkspace(ws_root, job_id="BLG-001")
    jw.research_dir  # Path to research/
    jw.drafts_dir    # Path to drafts/
    jw.write_draft(idea_id, content)  # writes to drafts/<idea_id>.md
"""
from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import yaml

from ..domain.article import Draft
from .draft_store import file_lock, split_frontmatter


@dataclass
class JobState:
    """State of a single job (persisted as state.json)."""
    job_id: str
    topic: str
    idea_id: str
    current_phase: str = "brief"
    retry_count: int = 0
    processed_events: list[str] = None
    created_at: str = ""
    updated_at: str = ""

    def __post_init__(self):
        if self.processed_events is None:
            self.processed_events = []
        if not self.created_at:
            self.created_at = datetime.now(timezone.utc).isoformat()
        if not self.updated_at:
            self.updated_at = self.created_at

    def to_dict(self) -> dict:
        return {
            "job_id": self.job_id,
            "topic": self.topic,
            "idea_id": self.idea_id,
            "current_phase": self.current_phase,
            "retry_count": self.retry_count,
            "processed_events": self.processed_events,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "JobState":
        return cls(
            job_id=data["job_id"],
            topic=data.get("topic", ""),
            idea_id=data.get("idea_id", ""),
            current_phase=data.get("current_phase", "brief"),
            retry_count=data.get("retry_count", 0),
            processed_events=data.get("processed_events", []),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", ""),
        )


class JobWorkspace:
    """Isolated workspace for a single job_id.

    Provides the same interface as parts of the global Workspace, but scoped
    to a single job. Prevents cross-job file collisions.
    """

    def __init__(self, ws_root: Path, job_id: str):
        self._root = ws_root / "jobs" / job_id
        self._job_id = job_id

        # create directories
        self._root.mkdir(parents=True, exist_ok=True)
        (self._root / "research").mkdir(exist_ok=True)
        (self._root / "drafts").mkdir(exist_ok=True)

    @property
    def root(self) -> Path:
        return self._root

    @property
    def research_dir(self) -> Path:
        return self._root / "research"

    @property
    def drafts_dir(self) -> Path:
        return self._root / "drafts"

    @property
    def assets_dir(self) -> Path:
        d = self._root / "assets"
        d.mkdir(exist_ok=True)
        return d

    # ── state persistence ────────────────────────────────────────────────────

    def _state_file(self) -> Path:
        return self._root / "state.json"

    def load_state(self) -> JobState | None:
        f = self._state_file()
        if not f.exists():
            return None
        return JobState.from_dict(json.loads(f.read_text()))

    def save_state(self, state: JobState) -> None:
        state.updated_at = datetime.now(timezone.utc).isoformat()
        self._state_file().write_text(
            json.dumps(state.to_dict(), indent=2, ensure_ascii=False)
        )

    def create_state(self, topic: str, idea_id: str) -> JobState:
        state = JobState(
            job_id=self._job_id,
            topic=topic,
            idea_id=idea_id,
        )
        self.save_state(state)
        return state

    # ── idempotency ──────────────────────────────────────────────────────────

    def add_event(self, state: JobState, event: str) -> bool:
        """Add event if not duplicate. Returns True if added."""
        if event in state.processed_events:
            return False
        state.processed_events.append(event)
        self.save_state(state)
        return True

    def has_event(self, state: JobState, event: str) -> bool:
        return event in state.processed_events

    # ── research ─────────────────────────────────────────────────────────────

    def write_research(self, idea_id: str, content: str) -> str:
        path = self.research_dir / f"{idea_id}.md"
        path.write_text(content)
        return str(path)

    def read_research(self, idea_id: str) -> str | None:
        path = self.research_dir / f"{idea_id}.md"
        if path.exists():
            return path.read_text()
        return None

    # ── drafts ───────────────────────────────────────────────────────────────

    def write_draft(self, idea_id: str, content: str) -> str:
        path = self.drafts_dir / f"{idea_id}.md"
        with file_lock(path):
            path.write_text(content)
        return str(path)

    def load_draft(self, idea_id: str) -> Draft | None:
        path = self.drafts_dir / f"{idea_id}.md"
        if not path.exists():
            return None
        raw = path.read_text()
        fm, body = split_frontmatter(raw)
        return Draft(idea_id=idea_id, raw=raw, frontmatter=fm, body=body)

    def draft_path(self, idea_id: str) -> str:
        return str(self.drafts_dir / f"{idea_id}.md")

    def draft_exists(self, idea_id: str) -> bool:
        return (self.drafts_dir / f"{idea_id}.md").exists()

    def update_body(self, idea_id: str, new_body: str, featured_image: str = "") -> str:
        path = self.drafts_dir / f"{idea_id}.md"
        with file_lock(path):
            fm, _ = split_frontmatter(path.read_text()) if path.exists() else ({}, "")
            fm = fm or {}
            if featured_image:
                fm.setdefault("seo", {})["featured_image"] = featured_image
            front = yaml.safe_dump(fm, allow_unicode=True, sort_keys=False)
            path.write_text(f"---\n{front}---\n{new_body}")
        return str(path)

    # ── assets ───────────────────────────────────────────────────────────────

    def asset_dir(self, idea_id: str) -> Path:
        d = self.assets_dir / idea_id
        d.mkdir(exist_ok=True)
        return d

    def list_assets(self, idea_id: str) -> list[tuple[str, str]]:
        d = self.asset_dir(idea_id)
        exts = (".webp", ".png", ".jpg", ".jpeg")
        return [(p.name, str(p)) for p in sorted(d.iterdir())
                if p.suffix.lower() in exts]

    # ── lifecycle ────────────────────────────────────────────────────────────

    def transition(self, state: JobState, new_phase: str) -> bool:
        """Advance job to new phase. Returns True if valid transition."""
        VALID = ["brief", "research", "draft", "edit", "imagery", "publish", "archive"]
        if new_phase not in VALID:
            return False
        idx_old = VALID.index(state.current_phase) if state.current_phase in VALID else -1
        idx_new = VALID.index(new_phase)
        if idx_new <= idx_old:
            return False  # can't go backwards
        state.current_phase = new_phase
        self.save_state(state)
        return True

    def complete(self, state: JobState, phase: str, event: str | None = None) -> None:
        """Mark phase complete and optionally record event."""
        if event:
            self.add_event(state, event)
        self.transition(state, phase)

    def fail(self, state: JobState) -> bool:
        """Increment retry count. Returns True if under limit."""
        state.retry_count += 1
        self.save_state(state)
        return state.retry_count < 3

    def cleanup(self) -> None:
        """Remove job workspace directory."""
        if self._root.exists():
            shutil.rmtree(self._root)
