"""Workspace paths — the single source of truth for where state lives on disk.

State lives in <repo>/workspace by default; a Workspace can be pointed
elsewhere via the BLOG_WORKSPACE env var (e.g. in tests).
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Workspace:
    root: Path

    @classmethod
    def default(cls) -> "Workspace":
        # Runtime state lives inside the project at <repo>/workspace. The path is
        # computed from this file, NOT from $HOME — the `blog` Hermes profile
        # remaps HOME, so Path.home() would resolve to the wrong, empty dir.
        # BLOG_WORKSPACE still overrides for tests / alternate locations.
        env = os.environ.get("BLOG_WORKSPACE")
        if env:
            return cls(Path(env))
        repo_root = Path(__file__).resolve().parents[2]
        return cls(repo_root / "workspace")

    @property
    def drafts(self) -> Path:
        return self.root / "drafts"

    @property
    def published(self) -> Path:
        return self.root / "published"

    @property
    def research(self) -> Path:
        return self.root / "research"

    @property
    def assets(self) -> Path:
        return self.root / "assets"

    @property
    def idea_bank(self) -> Path:
        return self.root / "idea-bank.md"

    @property
    def journal(self) -> Path:
        return self.root / "journal.jsonl"

    @property
    def config(self) -> Path:
        return self.root / "config.yaml"

    @property
    def token(self) -> Path:
        return self.root / "token.json"

    @property
    def logs(self) -> Path:
        return self.root / "logs"

    @property
    def notify_log(self) -> Path:
        return self.logs / "notify.log"

    def ensure_dirs(self) -> "Workspace":
        for d in (self.drafts, self.published, self.research, self.assets, self.logs):
            d.mkdir(parents=True, exist_ok=True)
        return self
