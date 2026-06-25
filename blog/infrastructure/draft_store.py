"""Filesystem draft/published store — parses raw files into domain Drafts."""
from __future__ import annotations

import json
import time
import os
from pathlib import Path
from contextlib import contextmanager

import yaml

from ..application.ports import DraftStorePort
from ..domain.article import Draft
from .paths import Workspace


@contextmanager
def file_lock(path: Path, timeout: int = 5):
    lock_path = path.with_suffix(path.suffix + ".lock")
    start = time.time()
    while lock_path.exists():
        if time.time() - start > timeout:
            raise TimeoutError(f"Timeout waiting for lock: {lock_path}")
        time.sleep(0.2)
    
    lock_path.touch()
    try:
        yield
    finally:
        lock_path.unlink()


def split_frontmatter(text: str) -> tuple[dict, str]:
    """Return (frontmatter_dict, body). Tolerates missing/invalid frontmatter."""
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            try:
                return yaml.safe_load(parts[1]) or {}, parts[2]
            except yaml.YAMLError:
                return {}, text
    return {}, text


class FileDraftStore(DraftStorePort):
    def __init__(self, ws: Workspace):
        self._ws = ws

    def _draft_file(self, idea_id: str):
        return self._ws.drafts / f"{idea_id}.md"

    def write_research_brief(self, idea_id: str, content: str) -> str:
        # Research briefs live OUTSIDE drafts/ — drafts/ holds only readable
        # articles. Briefs are working files (for production, not reading).
        self._ws.research.mkdir(parents=True, exist_ok=True)
        path = self._ws.research / f"{idea_id}.md"
        path.write_text(content)
        return str(path)

    def write_draft(self, idea_id: str, content: str) -> str:
        path = self._draft_file(idea_id)
        with file_lock(path):
            path.write_text(content)
        return str(path)

    def draft_path(self, idea_id: str) -> str:
        return str(self._draft_file(idea_id))

    def draft_exists(self, idea_id: str) -> bool:
        return self._draft_file(idea_id).exists()

    def load_draft(self, idea_id: str) -> Draft | None:
        path = self._draft_file(idea_id)
        if not path.exists():
            return None
        raw = path.read_text()
        fm, body = split_frontmatter(raw)
        return Draft(idea_id=idea_id, raw=raw, frontmatter=fm, body=body)

    def is_published(self, idea_id: str) -> bool:
        return any(self._ws.published.glob(f"{idea_id}.*"))

    def _post_file(self, idea_id: str):
        return self._ws.published / f"{idea_id}.json"

    def record_blogger_post(self, idea_id: str, info: dict) -> str:
        self._ws.published.mkdir(parents=True, exist_ok=True)
        path = self._post_file(idea_id)
        path.write_text(json.dumps(info, indent=2, ensure_ascii=False))
        return str(path)

    def blogger_post(self, idea_id: str) -> dict | None:
        path = self._post_file(idea_id)
        if not path.exists():
            return None
        try:
            return json.loads(path.read_text())
        except json.JSONDecodeError:
            return None

    def list_assets(self, idea_id: str) -> list[tuple[str, str]]:
        d = self._ws.assets / idea_id
        if not d.is_dir():
            return []
        exts = (".webp", ".png", ".jpg", ".jpeg")
        return [(p.name, str(p)) for p in sorted(d.iterdir())
                if p.suffix.lower() in exts]

    def update_body(self, idea_id: str, new_body: str, featured_image: str = "") -> str:
        path = self._draft_file(idea_id)
        with file_lock(path):
            fm, _ = split_frontmatter(path.read_text()) if path.exists() else ({}, "")
            fm = fm or {}
            if featured_image:
                fm.setdefault("seo", {})["featured_image"] = featured_image
            front = yaml.safe_dump(fm, allow_unicode=True, sort_keys=False)
            path.write_text(f"---\n{front}---\n{new_body}")
        return str(path)
