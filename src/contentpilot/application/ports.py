"""Ports — abstract interfaces the use cases require.

Infrastructure provides concrete implementations. The dependency rule: this
module imports only from the domain layer (via the service), never from
infrastructure.
"""
from __future__ import annotations

from abc import ABC, abstractmethod

from ..domain.article import Draft, Idea


class Clock(ABC):
    @abstractmethod
    def now_iso(self) -> str:
        """Current UTC time as an ISO-8601 string."""


class ConfigPort(ABC):
    @abstractmethod
    def load(self) -> dict:
        """Return the blog workspace config (domain, language, ...)."""


class JournalPort(ABC):
    @abstractmethod
    def append(self, idea_id: str, from_stage: str, to_stage: str,
               metadata: dict | None = None) -> None:
        """Append one stage-transition record."""

    @abstractmethod
    def latest_stages(self) -> dict:
        """Map idea_id -> {'stage': str, 'updated': iso} for the latest entry each."""

    @abstractmethod
    def mark_complete(self, idea_id: str, phase: str, result: dict | None = None) -> None:
        """Explicit completion signal for a phase."""

    @abstractmethod
    def is_phase_complete(self, idea_id: str, phase: str) -> bool:
        """Check if a phase has an explicit completion entry."""


class DraftStorePort(ABC):
    @abstractmethod
    def write_research_brief(self, idea_id: str, content: str) -> str:
        """Persist a research brief; return its path."""

    @abstractmethod
    def write_draft(self, idea_id: str, content: str) -> str:
        """Persist a draft template/body; return its path."""

    @abstractmethod
    def draft_path(self, idea_id: str) -> str:
        """Path where the draft would live (whether or not it exists)."""

    @abstractmethod
    def draft_exists(self, idea_id: str) -> bool:
        ...

    @abstractmethod
    def load_draft(self, idea_id: str) -> Draft | None:
        """Load + parse a draft into a domain entity, or None if missing."""

    @abstractmethod
    def is_published(self, idea_id: str) -> bool:
        """True if an artifact for this idea already exists in published/ (idempotency)."""

    @abstractmethod
    def record_blogger_post(self, idea_id: str, info: dict) -> str:
        """Persist the Blogger post mapping (id/url) to published/<id>.json; return its path."""

    @abstractmethod
    def blogger_post(self, idea_id: str) -> dict | None:
        """Return the recorded Blogger post info for this idea, or None."""

    @abstractmethod
    def list_assets(self, idea_id: str) -> list[tuple[str, str]]:
        """Return [(filename, abs_path)] of the article's image assets."""

    @abstractmethod
    def update_body(self, idea_id: str, new_body: str, featured_image: str = "") -> str:
        """Rewrite the draft's body (keep frontmatter; set seo.featured_image); return path."""


class IdeaBankPort(ABC):
    @abstractmethod
    def list_ideas(self) -> list[Idea]:
        """Parse the idea bank into domain entities (examples excluded)."""


class NotifierPort(ABC):
    @abstractmethod
    def notify(self, idea_id: str, from_stage: str, to_stage: str,
               title: str = "") -> None:
        """Fire a best-effort notification. Must never raise."""


class PublisherPort(ABC):
    @abstractmethod
    def token_available(self) -> bool:
        """True if Blogger OAuth (token.json) is set up."""

    @abstractmethod
    def upload_draft(self, title: str, content: str, labels: list | None = None) -> dict:
        """Create an UNPUBLISHED draft post on the CMS from a markdown body.

        Returns {'id', 'url', 'title'}. The post is NOT live — going live is a
        separate, human-gated step.
        """

    @abstractmethod
    def update_post(self, post_id: str, content: str) -> None:
        """Replace an existing post's content (markdown body; adapter renders HTML)."""


class ImageHostPort(ABC):
    @abstractmethod
    def upload_public(self, local_path: str) -> str:
        """Upload a local image, make it publicly reachable, return its URL."""
