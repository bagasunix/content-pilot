"""In-memory fake adapters — let the use cases be tested with zero I/O."""
from __future__ import annotations

from blog.application.ports import (
    Clock,
    ConfigPort,
    DraftStorePort,
    IdeaBankPort,
    ImageHostPort,
    JournalPort,
    PublisherPort,
)
from blog.domain.article import Draft
from blog.infrastructure.draft_store import split_frontmatter


class FakeClock(Clock):
    def now_iso(self) -> str:
        return "2026-06-14T00:00:00+00:00"


class FakeConfig(ConfigPort):
    def __init__(self, data=None):
        self.data = data or {"domain": "{{DOMAIN}}", "language": "id"}

    def load(self):
        return self.data


class FakeJournal(JournalPort):
    def __init__(self):
        self.entries = []

    def append(self, idea_id, from_stage, to_stage, metadata=None):
        self.entries.append({
            "idea_id": idea_id, "from": from_stage, "to": to_stage,
            "metadata": metadata,
        })

    def latest_stages(self):
        out = {}
        for i, e in enumerate(self.entries):
            out[e["idea_id"]] = {"stage": e["to"], "updated": f"2026-06-14T00:00:{i:02d}"}
        return out

    def seed(self, idea_id, stage):
        self.append(idea_id, "idea", stage)

    def get_failures(self, idea_id):
        return [e for e in self.entries
                if e["idea_id"] == idea_id and e.get("metadata", {}).get("gate") == "fail"]

    def mark_complete(self, idea_id, phase, result=None):
        self.entries.append({
            "idea_id": idea_id, "from": phase, "to": phase,
            "metadata": {"complete": True, **(result or {})},
        })

    def is_phase_complete(self, idea_id, phase):
        return any(
            e["idea_id"] == idea_id and e["from"] == phase
            and e.get("metadata", {}).get("complete") is True
            for e in self.entries
        )


class FakeDraftStore(DraftStorePort):
    def __init__(self):
        self.research = {}
        self.drafts = {}
        self.published = set()
        self.posts = {}
        self._assets = {}
        self.bodies = {}

    def write_research_brief(self, idea_id, content):
        self.research[idea_id] = content
        return f"/ws/drafts/{idea_id}.research.md"

    def write_draft(self, idea_id, content):
        self.drafts[idea_id] = content
        return f"/ws/drafts/{idea_id}.md"

    def draft_path(self, idea_id):
        return f"/ws/drafts/{idea_id}.md"

    def draft_exists(self, idea_id):
        return idea_id in self.drafts

    def load_draft(self, idea_id):
        if idea_id not in self.drafts:
            return None
        raw = self.drafts[idea_id]
        fm, body = split_frontmatter(raw)
        return Draft(idea_id=idea_id, raw=raw, frontmatter=fm, body=body)

    def is_published(self, idea_id):
        return idea_id in self.published

    def record_blogger_post(self, idea_id, info):
        self.posts[idea_id] = info
        self.published.add(idea_id)
        return f"/ws/published/{idea_id}.json"

    def blogger_post(self, idea_id):
        return self.posts.get(idea_id)

    def seed_assets(self, idea_id, assets):
        self._assets[idea_id] = assets

    def list_assets(self, idea_id):
        return list(self._assets.get(idea_id, []))

    def update_body(self, idea_id, new_body, featured_image=""):
        self.bodies[idea_id] = (new_body, featured_image)
        return f"/ws/drafts/{idea_id}.md"


class FakeIdeaBank(IdeaBankPort):
    def __init__(self, ideas=None):
        self.ideas = ideas or []

    def list_ideas(self):
        return list(self.ideas)


class FakePublisher(PublisherPort):
    def __init__(self, has_token=False):
        self._has_token = has_token
        self.uploaded = []
        self.updated = []

    def token_available(self):
        return self._has_token

    def upload_draft(self, title, content, labels=None):
        self.uploaded.append({"title": title, "content": content, "labels": labels or []})
        n = len(self.uploaded)
        return {"id": f"FAKE-POST-{n}", "url": f"http://blog.test/p/{n}.html", "title": title}

    def update_post(self, post_id, content):
        self.updated.append((post_id, content))


class FakeImageHost(ImageHostPort):
    def __init__(self):
        self.uploaded = []

    def upload_public(self, local_path):
        self.uploaded.append(local_path)
        import os
        return f"http://img/{os.path.basename(local_path)}"


class FakeNotifier:
    def __init__(self):
        self.sent = []

    def notify(self, idea_id, from_stage, to_stage, title=""):
        self.sent.append((idea_id, from_stage, to_stage))


def good_draft(idea_id="x", title="Cara Pasang Sesuatu"):
    """A draft that passes every mechanical gate."""
    body = "Halo sobat, ini paragraf pembuka yang santai. " + ("kata " * 700)
    return f"""---
idea_id: {idea_id}
seo:
  title: "{title}"
  meta_description: "deskripsi singkat yang bikin penasaran"
  keywords: [pasang, sesuatu]
  slug: cara-pasang-sesuatu
---

# {title}

<!-- img: hero, alt: "gambar utama" -->

{body}

```bash
echo halo
```
"""
