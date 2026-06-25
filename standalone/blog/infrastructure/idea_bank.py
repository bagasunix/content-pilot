"""Markdown idea-bank parser — turns '### [H|M|L] Title' blocks into Ideas."""
from __future__ import annotations

import re

from ..application.ports import IdeaBankPort
from ..domain.article import Idea
from .paths import Workspace

_HEAD_RE = re.compile(r"\[([HML])\]\s*(.+)")


def _field(body: str, name: str) -> str:
    # [ \t]* (not \s*) so an empty field doesn't greedily swallow the next line.
    m = re.search(rf"^-[ \t]*{re.escape(name)}:[ \t]*(.+)$", body, re.MULTILINE)
    return m.group(1).strip() if m else ""


class MarkdownIdeaBank(IdeaBankPort):
    def __init__(self, ws: Workspace):
        self._path = ws.idea_bank

    def list_ideas(self) -> list[Idea]:
        if not self._path.exists():
            return []
        ideas: list[Idea] = []
        # Split on the heading that starts each entry.
        for block in re.split(r"\n###\s+", self._path.read_text())[1:]:
            head, *rest = block.split("\n")
            body = "\n".join(rest)
            if "(CONTOH" in head or "(contoh" in head:
                continue
            m = _HEAD_RE.match(head.strip())
            priority = m.group(1) if m else "M"
            title = m.group(2).strip() if m else head.strip()
            idea_id = _field(body, "idea_id")
            if not idea_id:
                continue
            ideas.append(Idea(
                priority=priority,
                title=title,
                idea_id=idea_id,
                keyword=_field(body, "keyword target") or _field(body, "keyword"),
                category=_field(body, "kategori") or _field(body, "category"),
                source=_field(body, "sumber") or _field(body, "source"),
                angle=_field(body, "angle/pengalaman") or _field(body, "angle"),
                status=_field(body, "status") or "idea",
            ))
        return ideas
