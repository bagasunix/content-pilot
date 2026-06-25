"""Result objects returned by the use cases.

The service returns these structured results; the interface layer (presenter)
turns them into human-facing text. Keeps formatting out of the core.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from ..domain.article import GateResult, Idea


@dataclass
class StatusRow:
    idea_id: str
    stage: str
    updated: str
    is_wip: bool


@dataclass
class StatusResult:
    rows: list[StatusRow]
    wip_count: int
    wip_limit: int


@dataclass
class NextResult:
    # status: "wip_full" | "empty" | "ok" | "exhausted"
    status: str
    idea: Idea | None = None
    wip_count: int = 0
    wip_limit: int = 0
    in_flight: list[str] = field(default_factory=list)
    angle_missing: bool = False


@dataclass
class StageActionResult:
    """Generic outcome for research/draft/review/approve/publish."""
    # status codes are command-specific; the presenter maps them to text
    status: str
    idea_id: str = ""
    from_stage: str | None = None
    to_stage: str | None = None
    path: str = ""
    detail: str = ""
    wip_count: int = 0
    wip_limit: int = 0
    failures: list[str] = field(default_factory=list)
    post_id: str = ""
    url: str = ""


@dataclass
class GateOutcome:
    # status: "wrong_stage" | "fail" | "pass"
    status: str
    idea_id: str = ""
    current_stage: str | None = None
    result: GateResult | None = None
