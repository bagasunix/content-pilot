"""PipelineService — the use cases (the application core).

Orchestrates the domain rules over the ports. No I/O here: every side effect
goes through an injected port, which makes the whole thing unit-testable with
fakes (see tests/).
"""
from __future__ import annotations

from ..domain import gates, stages
from ..domain.article import Idea
from ..domain.images import embed_images, order_assets_for_placeholders
from .ports import (
    Clock,
    ConfigPort,
    DraftStorePort,
    IdeaBankPort,
    ImageHostPort,
    JournalPort,
    NotifierPort,
    PublisherPort,
)
from .results import (
    GateOutcome,
    NextResult,
    StageActionResult,
    StatusResult,
    StatusRow,
)


class PipelineService:
    def __init__(
        self,
        *,
        config: ConfigPort,
        clock: Clock,
        journal: JournalPort,
        drafts: DraftStorePort,
        idea_bank: IdeaBankPort,
        notifier: NotifierPort,
        publisher: PublisherPort,
        image_host: ImageHostPort,
    ):
        self._config = config
        self._clock = clock
        self._journal = journal
        self._drafts = drafts
        self._ideas = idea_bank
        self._notifier = notifier
        self._publisher = publisher
        self._image_host = image_host

    # ── helpers ───────────────────────────────────────────────────────────

    def _auto_fill_seo(self, idea_id: str, draft) -> None:
        """Self-heal: auto-populate missing SEO fields from draft content.
        
        Called before gate evaluation to prevent repeated 'seo.X kosong' failures.
        Only fills fields that are empty — never overwrites human/editor edits.
        """
        import re as _re
        seo = draft.seo or {}
        changed = False

        if not seo.get("title"):
            h1 = _re.search(r"^#\s+(.+)$", draft.body, _re.MULTILINE)
            if h1:
                seo["title"] = h1.group(1).strip()
                changed = True

        if not seo.get("slug"):
            seo["slug"] = idea_id
            changed = True

        if not seo.get("meta_description"):
            # First non-empty paragraph (skip headings, comments)
            for para in draft.body.split("\n\n"):
                text = _re.sub(r"<!--.*?-->", "", para).strip()
                text = _re.sub(r"^#+\s+", "", text).strip()
                if len(text) > 40 and not text.startswith("|"):
                    seo["meta_description"] = text[:155]
                    changed = True
                    break

        if not seo.get("keywords"):
            # Extract from title + H2s
            words = set()
            title = seo.get("title", "")
            for m in _re.finditer(r"^##\s+(.+)$", draft.body, _re.MULTILINE):
                words.update(m.group(1).lower().split())
            if title:
                words.update(title.lower().split())
            stop = {"dan", "di", "ke", "dari", "untuk", "yang", "ini", "itu",
                     "dengan", "pada", "adalah", "the", "a", "an", "of", "in",
                     "to", "for", "is", "on", "with", "how", "cara", "apa"}
            kw = sorted(words - stop)[:5]
            if kw:
                seo["keywords"] = kw
                changed = True

        if changed:
            draft.frontmatter["seo"] = seo
            self._drafts.update_body(idea_id, draft.body,
                                     featured_image=seo.get("featured_image", ""))

    @staticmethod
    def slug(topic: str) -> str:
        """Stable idea_id from a topic string."""
        s = topic.lower().strip().replace(" ", "-")
        s = "".join(c for c in s if c.isalnum() or c == "-")
        return s[:50]

    def _stages(self) -> dict:
        return self._journal.latest_stages()

    def _wip_limit(self) -> int:
        """Read WIP limit from config, fallback to domain default."""
        cfg = self._config.load()
        return int(cfg.get("wip_limit", stages.DEFAULT_WIP_LIMIT))

    def _current_stage(self, idea_id: str) -> str | None:
        info = self._stages().get(idea_id)
        return info["stage"] if info else None

    def _wip_in_flight(self, snapshot: dict | None = None) -> list[str]:
        snapshot = snapshot if snapshot is not None else self._stages()
        return [k for k, v in snapshot.items() if stages.counts_as_wip(v["stage"])]

    def _transition(self, idea_id, from_stage, to_stage, metadata=None, title=""):
        self._journal.append(idea_id, from_stage, to_stage, metadata)
        self._notifier.notify(idea_id, from_stage, to_stage, title)

    @staticmethod
    def _unresolved_markers(body: str) -> list[str]:
        """TODO/FIXME/[REDACTED]-style markers that must never reach Blogger."""
        from ..domain.gates import _COMMENT_RE, _UNRESOLVED_RE
        return _UNRESOLVED_RE.findall(_COMMENT_RE.sub("", body))

    @staticmethod
    def _first_h1(body: str) -> str:
        import re
        m = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
        return m.group(1).strip() if m else ""

    # ── status ────────────────────────────────────────────────────────────

    def status(self) -> StatusResult:
        snapshot = self._stages()
        rows = [
            StatusRow(idea_id, info["stage"], info["updated"],
                      stages.counts_as_wip(info["stage"]))
            for idea_id, info in sorted(
                snapshot.items(), key=lambda x: x[1]["updated"], reverse=True
            )
        ]
        wip = len(self._wip_in_flight(snapshot))
        return StatusResult(rows=rows, wip_count=wip, wip_limit=self._wip_limit())

    # ── next ──────────────────────────────────────────────────────────────

    def next_idea(self) -> NextResult:
        snapshot = self._stages()
        in_flight = self._wip_in_flight(snapshot)
        if len(in_flight) >= self._wip_limit():
            return NextResult("wip_full", wip_count=len(in_flight),
                              wip_limit=self._wip_limit(), in_flight=in_flight)

        ideas = self._ideas.list_ideas()
        if not ideas:
            return NextResult("empty")

        for idea in sorted(ideas, key=lambda i: i.priority_rank):
            cur = snapshot.get(idea.idea_id, {}).get("stage")
            if cur in (None, stages.IDEA):
                return NextResult("ok", idea=idea, angle_missing=not idea.has_angle)
        return NextResult("exhausted")

    # ── FASE 1: research ────────────────────────────────────────────────────

    def research(self, topic: str) -> StageActionResult:
        # Ad-hoc topic → idea_id derived by slugging the topic.
        return self._research(self.slug(topic), topic)

    def _research(self, idea_id: str, topic: str) -> StageActionResult:
        current = self._current_stage(idea_id)
        if current and current != stages.IDEA:
            # If we already started processing this idea, check if it's a failure
            # that should be retried.
            failures = self._journal.get_failures(idea_id)
            if failures:
                # If there were failures, we should re-evaluate the current stage
                # and potentially restart the pipeline.
                # For now, we simply prepend failure info to the research brief.
                pass # Logic to handle retry will be added here later.
            else:
                # If no failures, and we already started, just return existing stage.
                return StageActionResult("exists", idea_id=idea_id, from_stage=current)
        
        in_flight = self._wip_in_flight()
        if len(in_flight) >= self._wip_limit():
            return StageActionResult("wip_full", idea_id=idea_id,
                                     wip_count=len(in_flight), wip_limit=self._wip_limit())

        path = self._drafts.write_research_brief(idea_id, self._research_brief(idea_id, topic))
        self._transition(idea_id, stages.IDEA, stages.RESEARCHING,
                         metadata={"topic": topic}, title=topic)
        return StageActionResult("created", idea_id=idea_id,
                                 to_stage=stages.RESEARCHING, path=path)

    # ── FASE 2: draft ───────────────────────────────────────────────────────

    def draft(self, idea_id: str) -> StageActionResult:
        current = self._current_stage(idea_id)
        if not current:
            return StageActionResult("not_found", idea_id=idea_id)
        if current == stages.DRAFTED:
            return StageActionResult("already", idea_id=idea_id,
                                     path=self._drafts.draft_path(idea_id))
        if current not in (stages.RESEARCHING, stages.OUTLINED):
            return StageActionResult("wrong_stage", idea_id=idea_id, from_stage=current)

        path = self._drafts.write_draft(idea_id, self._draft_template(idea_id))
        self._transition(idea_id, current, stages.DRAFTED)
        return StageActionResult("created", idea_id=idea_id,
                                 to_stage=stages.DRAFTED, path=path)

    def review(self, idea_id: str) -> StageActionResult:
        current = self._current_stage(idea_id)
        if current != stages.DRAFTED:
            return StageActionResult("wrong_stage", idea_id=idea_id, from_stage=current)
        if not self._drafts.draft_exists(idea_id):
            return StageActionResult("missing_file", idea_id=idea_id,
                                     path=self._drafts.draft_path(idea_id))
        self._transition(idea_id, stages.DRAFTED, stages.REVIEWING)
        return StageActionResult("created", idea_id=idea_id, to_stage=stages.REVIEWING)

    # ── §6 gate ─────────────────────────────────────────────────────────────

    def gate(self, idea_id: str) -> GateOutcome:
        current = self._current_stage(idea_id)
        if current not in (stages.REVIEWING, stages.DRAFTED):
            return GateOutcome("wrong_stage", idea_id=idea_id, current_stage=current)

        draft = self._drafts.load_draft(idea_id)
        if draft is None:
            from ..domain.article import GateResult
            res = GateResult(failures=[f"draft file hilang: {self._drafts.draft_path(idea_id)}"])
            return GateOutcome("fail", idea_id=idea_id, current_stage=current, result=res)

        # Auto-fill missing SEO fields from draft content (self-heal pattern)
        self._auto_fill_seo(idea_id, draft)

        res = gates.evaluate(draft)
        if not res.passed:
            self._journal.append(idea_id, current, current,
                                 {"gate": "fail", "failures": res.failures})
            return GateOutcome("fail", idea_id=idea_id, current_stage=current, result=res)

        self._transition(idea_id, current, stages.GATED,
                         metadata={"gate": "pass", "warnings": res.warnings})
        return GateOutcome("pass", idea_id=idea_id, current_stage=current, result=res)

    # ── FASE 3: human gate + publish ────────────────────────────────────────

    def approve(self, idea_id: str) -> StageActionResult:
        """Human go-live gate. Manual only — never call from automation."""
        current = self._current_stage(idea_id)
        if current != stages.GATED:
            return StageActionResult("wrong_stage", idea_id=idea_id, from_stage=current)
        self._transition(idea_id, stages.GATED, stages.APPROVED, metadata={"by_human": True})
        return StageActionResult("created", idea_id=idea_id, to_stage=stages.APPROVED)

    def publish(self, idea_id: str) -> StageActionResult:
        current = self._current_stage(idea_id)
        if current != stages.APPROVED:
            return StageActionResult("wrong_stage", idea_id=idea_id, from_stage=current)
        if self._drafts.is_published(idea_id):           # idempotency (§7)
            return StageActionResult("already_published", idea_id=idea_id)
        if not self._publisher.token_available():
            return StageActionResult("no_token", idea_id=idea_id)
        # Safety net: re-validate draft right before publish. Gate should have
        # caught these, but a draft could have been edited post-gate.
        draft = self._drafts.load_draft(idea_id)
        if draft is not None:
            markers = self._unresolved_markers(draft.body)
            if markers:
                return StageActionResult(
                    "pre_publish_fail",
                    idea_id=idea_id,
                    failures=[f"marker unresolved di draft: {', '.join(markers)}"],
                )
        return StageActionResult("ready_to_publish", idea_id=idea_id)

    def push_draft(self, idea_id: str) -> StageActionResult:
        """Upload an approved article to Blogger as an UNPUBLISHED draft post.

        The body lands on blogger.com (so images can later be hosted natively
        on that post), but it never goes live here — that stays a manual gate.
        Idempotent via the published/<id>.json mapping.
        """
        current = self._current_stage(idea_id)
        if current != stages.APPROVED:
            return StageActionResult("wrong_stage", idea_id=idea_id, from_stage=current)
        if self._drafts.is_published(idea_id):
            return StageActionResult("already_pushed", idea_id=idea_id)
        if not self._publisher.token_available():
            return StageActionResult("no_token", idea_id=idea_id)
        draft = self._drafts.load_draft(idea_id)
        if draft is None:
            return StageActionResult("missing_file", idea_id=idea_id,
                                     path=self._drafts.draft_path(idea_id))
        markers = self._unresolved_markers(draft.body)
        if markers:
            return StageActionResult(
                "pre_publish_fail", idea_id=idea_id,
                failures=[f"marker unresolved di draft: {', '.join(markers)}"],
            )

        title = draft.seo.get("title") or self._first_h1(draft.body) or idea_id
        labels = draft.seo.get("keywords") or []
        info = self._publisher.upload_draft(title, draft.body, labels=labels)
        # Blogger API can't set permalink/search-description — stash the desired
        # values so the publisher can apply them in the editor at go-live.
        info = {
            **info,
            "slug": draft.seo.get("slug", ""),
            "search_description": draft.seo.get("meta_description", ""),
        }
        self._drafts.record_blogger_post(idea_id, info)
        self._transition(
            idea_id, current, stages.PUBLISHED,
            metadata={"blogger_post_id": info.get("id"), "url": info.get("url"),
                      "live": False},
            title=title,
        )
        return StageActionResult(
            "pushed", idea_id=idea_id, to_stage=stages.PUBLISHED,
            post_id=info.get("id", ""), url=info.get("url", ""),
        )

    def attach_images(self, idea_id: str) -> StageActionResult:
        """Host the article's assets, embed them into the draft body at its
        <!-- img --> slots (hero first → becomes the Blogger thumbnail), and
        update the already-pushed post. Runs after push_draft."""
        current = self._current_stage(idea_id)
        if current != stages.PUBLISHED:
            return StageActionResult("not_pushed", idea_id=idea_id, from_stage=current)
        post = self._drafts.blogger_post(idea_id)
        if not post or not post.get("id"):
            return StageActionResult("not_pushed", idea_id=idea_id)
        assets = self._drafts.list_assets(idea_id)
        if not assets:
            return StageActionResult("no_assets", idea_id=idea_id)
        draft = self._drafts.load_draft(idea_id)
        if draft is None:
            return StageActionResult("missing_file", idea_id=idea_id,
                                     path=self._drafts.draft_path(idea_id))

        path_by_name = dict(assets)
        ordered = order_assets_for_placeholders(draft.body, [n for n, _ in assets])
        urls = [self._image_host.upload_public(path_by_name[n]) for n in ordered]
        new_body = embed_images(draft.body, urls)
        self._drafts.update_body(idea_id, new_body, featured_image=urls[0])
        self._publisher.update_post(post["id"], new_body)
        return StageActionResult("attached", idea_id=idea_id,
                                 post_id=post["id"], detail=str(len(urls)))

    # ── FASE 1+2 combined ────────────────────────────────────────────────────

    def full(self, topic: str) -> list:
        """Ad-hoc topic → research + draft. idea_id derived from the topic."""
        return self._run(self.slug(topic), topic)

    def start(self, idea_id: str) -> list:
        """Start an idea-bank entry by its STABLE idea_id (keeps id == bank id).

        This is what automation should call — never slug a long title, which
        would create a draft whose id no longer matches the idea-bank entry.
        """
        idea = next((i for i in self._ideas.list_ideas() if i.idea_id == idea_id), None)
        if idea is None:
            return [("research", StageActionResult("idea_not_found", idea_id=idea_id))]
        return self._run(idea.idea_id, idea.title)

    def _run(self, idea_id: str, topic: str) -> list:
        """research → (outlined) → draft, keyed by an explicit idea_id."""
        steps = [("research", self._research(idea_id, topic))]
        if self._current_stage(idea_id) is None:
            return steps  # research blocked (WIP); stop
        if self._current_stage(idea_id) == stages.RESEARCHING:
            self._journal.append(idea_id, stages.RESEARCHING, stages.OUTLINED)
        steps.append(("draft", self.draft(idea_id)))
        return steps

    # ── job-isolated pipeline ────────────────────────────────────────────────

    def run_job(self, job_id: str, idea_id: str, topic: str) -> StageActionResult:
        """Run a single pipeline step in an isolated job workspace.

        Uses JobWorkspace for full file isolation. Returns the research result.
        The job state is tracked in workspace/jobs/<job_id>/state.json.
        """
        from ..infrastructure.job_workspace import JobWorkspace
        from ..infrastructure.paths import Workspace as _WS

        ws = _WS.default()
        jw = JobWorkspace(ws.root, job_id)

        # create or load job state
        state = jw.load_state()
        if state is None:
            state = jw.create_state(topic, idea_id)
        elif state.current_phase == "archive":
            return StageActionResult("already_archived", idea_id=idea_id)

        # write research brief to job-isolated directory
        brief = self._research_brief(idea_id, topic)
        jw.write_research(idea_id, brief)

        # also write to global workspace (backwards compat)
        self._drafts.write_research_brief(idea_id, brief)

        # transition state
        jw.transition(state, "research")

        # log to journal
        self._journal.append(idea_id, stages.IDEA, stages.RESEARCHING,
                             metadata={"topic": topic, "job_id": job_id})

        return StageActionResult("created", idea_id=idea_id,
                                 to_stage=stages.RESEARCHING,
                                 path=jw.research_dir / f"{idea_id}.md")

    # ── content templates (domain artifacts the use case produces) ───────────

    def _research_brief(self, idea_id: str, topic: str) -> str:
        failures = self._journal.get_failures(idea_id)
        failure_text = ""
        if failures:
            failure_text = "## Previous Failure Context\n"
            for f in failures:
                failure_text += f"- Stage: {f.get('from')} | Reason: {f.get('metadata', {}).get('failures')}\n"
        
        return f"""# Research Brief: {topic}

- idea_id: {idea_id}
- topic: {topic}
- created: {self._clock.now_iso()[:19]}
- stage: researching

{failure_text}
## Keyword Target
<!-- Diisi oleh blog-topic-research -->

## Search Intent
<!-- informational / transactional / navigational -->

## Competitor Analysis
<!-- Top 5 SERP results + gap -->

## Outline Proposal
<!-- H2/H3 structure setelah research -->

## Validasi Fakta & Versi Terbaru
<!-- WAJIB untuk tutorial teknologi (lihat blog-topic-research). -->
<!-- - Versi terbaru: <tool> <versi> (rilis <bln thn>) — sumber dok resmi -->
<!-- - Klaim terverifikasi ✓ (sumber + tanggal cek) -->
<!-- - Deprecation / perubahan vs versi lama -->
<!-- - PERLU VERIFIKASI editor: <klaim ragu> -->
<!-- Writer hanya boleh menulis dari info yang sudah tervalidasi di sini. -->

## Sources
<!-- Reference URLs — utamakan sumber primer (dok resmi, release notes, repo) -->
"""

    def _draft_template(self, idea_id: str) -> str:
        cfg = self._config.load()
        now = self._clock.now_iso()[:19]
        return f"""---
idea_id: {idea_id}
stage: drafted
domain: {cfg.get('domain', '')}
language: {cfg.get('language', 'id')}
created: {now}
updated: {now}
author: Hermes Agent
seo:
  title: ""
  meta_description: ""
  keywords: []
  slug: ""
---

# {gates.TITLE_PLACEHOLDER}

<!-- Draft ini diisi oleh Hermes agent via blog-writer skill -->
<!-- Voice guide WAJIB di-load sebelum menulis (/home/bagas/Project/blog-lifecycle/workspace/voice.md) -->
<!-- Setelah selesai: pipeline.py review {idea_id} -> gate {idea_id} -->

"""
