"""Domain entities."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Idea:
    """A topic queued in the idea bank."""
    priority: str            # "H" | "M" | "L"
    title: str
    idea_id: str
    keyword: str = ""
    category: str = ""
    source: str = ""
    angle: str = ""
    status: str = "idea"

    PRIORITY_ORDER = {"H": 0, "M": 1, "L": 2}

    @property
    def priority_rank(self) -> int:
        return self.PRIORITY_ORDER.get(self.priority, 1)

    @property
    def has_angle(self) -> bool:
        return bool(self.angle.strip())


@dataclass
class Draft:
    """A draft article, already parsed into frontmatter + body."""
    idea_id: str
    raw: str                 # full file text (incl. frontmatter)
    frontmatter: dict
    body: str

    @property
    def seo(self) -> dict:
        return self.frontmatter.get("seo", {}) or {}


@dataclass
class GateResult:
    """Outcome of the mechanical §6 quality gates."""
    failures: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not self.failures
