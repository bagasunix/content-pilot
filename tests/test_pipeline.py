"""Use-case tests for PipelineService, driven entirely by fake adapters."""
import unittest

from blog.application.service import PipelineService
from blog.domain import stages
from blog.domain.article import Idea

from .fakes import (
    FakeClock,
    FakeConfig,
    FakeDraftStore,
    FakeIdeaBank,
    FakeImageHost,
    FakeJournal,
    FakeNotifier,
    FakePublisher,
    good_draft,
)


def build(ideas=None, has_token=False):
    journal = FakeJournal()
    drafts = FakeDraftStore()
    svc = PipelineService(
        config=FakeConfig(),
        clock=FakeClock(),
        journal=journal,
        drafts=drafts,
        idea_bank=FakeIdeaBank(ideas or []),
        notifier=FakeNotifier(),
        publisher=FakePublisher(has_token=has_token),
        image_host=FakeImageHost(),
    )
    return svc, journal, drafts


class TestResearchDraftFlow(unittest.TestCase):
    def test_research_creates_and_transitions(self):
        svc, journal, drafts = build()
        r = svc.research("Cara Install Docker")
        self.assertEqual(r.status, "created")
        self.assertEqual(svc._current_stage(r.idea_id), stages.RESEARCHING)
        self.assertIn(r.idea_id, drafts.research)

    def test_research_idempotent(self):
        svc, *_ = build()
        svc.research("Cara Install Docker")
        again = svc.research("Cara Install Docker")
        self.assertEqual(again.status, "exists")

    def test_draft_requires_research(self):
        svc, *_ = build()
        self.assertEqual(svc.draft("ghost").status, "not_found")

    def test_full_pipeline_reaches_drafted(self):
        svc, journal, drafts = build()
        steps = dict(svc.full("Cara Install Docker"))
        self.assertEqual(steps["draft"].status, "created")
        idea_id = svc.slug("Cara Install Docker")
        self.assertEqual(svc._current_stage(idea_id), stages.DRAFTED)


class TestWIPLimit(unittest.TestCase):
    def _fill(self, journal):
        for i in range(stages.WIP_LIMIT):
            journal.seed(f"busy-{i}", stages.DRAFTED)

    def test_research_blocked_when_wip_full(self):
        svc, journal, _ = build()
        self._fill(journal)
        self.assertEqual(svc.research("Topik Baru").status, "wip_full")

    def test_next_blocked_when_wip_full(self):
        ideas = [Idea("H", "Topik", "topik", angle="ada")]
        svc, journal, _ = build(ideas=ideas)
        self._fill(journal)
        self.assertEqual(svc.next_idea().status, "wip_full")


class TestNext(unittest.TestCase):
    def test_picks_highest_priority_not_in_pipeline(self):
        ideas = [
            Idea("L", "Low one", "low-one", angle="x"),
            Idea("H", "High one", "high-one", angle="x"),
            Idea("M", "Med one", "med-one", angle="x"),
        ]
        svc, *_ = build(ideas=ideas)
        r = svc.next_idea()
        self.assertEqual(r.status, "ok")
        self.assertEqual(r.idea.idea_id, "high-one")

    def test_flags_missing_angle(self):
        svc, *_ = build(ideas=[Idea("H", "No angle", "no-angle")])
        r = svc.next_idea()
        self.assertTrue(r.angle_missing)

    def test_skips_ideas_already_in_pipeline(self):
        ideas = [Idea("H", "High one", "high-one", angle="x"),
                 Idea("M", "Med one", "med-one", angle="x")]
        svc, journal, _ = build(ideas=ideas)
        journal.seed("high-one", stages.DRAFTED)
        r = svc.next_idea()
        self.assertEqual(r.idea.idea_id, "med-one")


class TestStart(unittest.TestCase):
    def test_start_keys_off_idea_bank_id_not_title_slug(self):
        # Long title would slug to something else; start must keep the bank id.
        ideas = [Idea("H", "Docker Compose untuk Pemula: dari nol sampai jalan",
                      "docker-compose-untuk-pemula", angle="x")]
        svc, journal, drafts = build(ideas=ideas)
        steps = dict(svc.start("docker-compose-untuk-pemula"))
        self.assertEqual(steps["draft"].status, "created")
        # draft stored under the STABLE id, not the slugged title
        self.assertIn("docker-compose-untuk-pemula", drafts.drafts)
        self.assertNotIn("docker-compose-untuk-pemula-dari-nol-sampai-jalan", drafts.drafts)
        self.assertEqual(svc._current_stage("docker-compose-untuk-pemula"), stages.DRAFTED)

    def test_start_unknown_idea(self):
        svc, *_ = build(ideas=[])
        steps = dict(svc.start("ghost"))
        self.assertEqual(steps["research"].status, "idea_not_found")


class TestGateAndPublish(unittest.TestCase):
    def test_gate_pass_moves_to_gated(self):
        svc, journal, drafts = build()
        svc.full("Cara Pasang Sesuatu")
        idea_id = svc.slug("Cara Pasang Sesuatu")
        drafts.drafts[idea_id] = good_draft(idea_id=idea_id)   # agent "writes" it
        svc.review(idea_id)
        out = svc.gate(idea_id)
        self.assertEqual(out.status, "pass")
        self.assertEqual(svc._current_stage(idea_id), stages.GATED)

    def test_gate_fail_stays_put(self):
        svc, journal, drafts = build()
        svc.full("Topik Kosong")
        idea_id = svc.slug("Topik Kosong")
        svc.review(idea_id)                                     # draft still a template
        out = svc.gate(idea_id)
        self.assertEqual(out.status, "fail")
        self.assertNotEqual(svc._current_stage(idea_id), stages.GATED)

    def test_publish_idempotency(self):
        svc, journal, drafts = build(has_token=True)
        journal.seed("done", stages.APPROVED)
        drafts.published.add("done")
        self.assertEqual(svc.publish("done").status, "already_published")

    def test_publish_blocked_without_token(self):
        svc, journal, _ = build(has_token=False)
        journal.seed("ready", stages.APPROVED)
        self.assertEqual(svc.publish("ready").status, "no_token")

    def test_approve_only_from_gated(self):
        svc, journal, _ = build()
        journal.seed("x", stages.DRAFTED)
        self.assertEqual(svc.approve("x").status, "wrong_stage")

    def test_publish_blocks_on_todo_marker(self):
        svc, journal, drafts = build(has_token=True)
        journal.seed("todo-draft", stages.APPROVED)
        # Inject a draft with TODO marker
        bad = good_draft(idea_id="todo-draft").replace(
            "Halo sobat,", "Halo sobat, TODO(owner) pengalaman pribadi."
        )
        drafts.drafts["todo-draft"] = bad
        out = svc.publish("todo-draft")
        self.assertEqual(out.status, "pre_publish_fail")
        self.assertTrue(any("TODO(" in f for f in out.failures))

    def test_publish_blocks_on_reducted_marker(self):
        svc, journal, drafts = build(has_token=True)
        journal.seed("redacted", stages.APPROVED)
        bad = good_draft(idea_id="redacted").replace(
            "Halo sobat,", "Data: [REDACTED] jangan publish."
        )
        drafts.drafts["redacted"] = bad
        out = svc.publish("redacted")
        self.assertEqual(out.status, "pre_publish_fail")

    def test_publish_passes_clean_draft(self):
        svc, journal, drafts = build(has_token=True)
        journal.seed("clean", stages.APPROVED)
        drafts.drafts["clean"] = good_draft(idea_id="clean")
        out = svc.publish("clean")
        self.assertEqual(out.status, "ready_to_publish")


class TestPushDraft(unittest.TestCase):
    """push_draft uploads an approved article to Blogger as an UNPUBLISHED
    draft post and records the post_id — the article's body lands on Blogger,
    but never goes live without a further manual step."""

    def _approved(self, idea_id="post", title="Judul Keren", token=True):
        svc, journal, drafts = build(has_token=token)
        journal.seed(idea_id, stages.APPROVED)
        drafts.drafts[idea_id] = good_draft(idea_id=idea_id, title=title)
        return svc, journal, drafts

    def test_push_requires_approved(self):
        svc, journal, drafts = build(has_token=True)
        journal.seed("g", stages.GATED)
        drafts.drafts["g"] = good_draft(idea_id="g")
        self.assertEqual(svc.push_draft("g").status, "wrong_stage")

    def test_push_blocked_without_token(self):
        svc, journal, drafts = self._approved(token=False)
        self.assertEqual(svc.push_draft("post").status, "no_token")

    def test_push_idempotent(self):
        svc, journal, drafts = self._approved()
        drafts.published.add("post")
        self.assertEqual(svc.push_draft("post").status, "already_pushed")

    def test_push_blocks_on_marker(self):
        svc, journal, drafts = self._approved()
        drafts.drafts["post"] = good_draft(idea_id="post").replace(
            "Halo sobat,", "Halo sobat, TODO(owner) isi nanti."
        )
        out = svc.push_draft("post")
        self.assertEqual(out.status, "pre_publish_fail")

    def test_push_uploads_records_and_transitions(self):
        svc, journal, drafts = self._approved(title="Docker Buat Pemula")
        out = svc.push_draft("post")
        self.assertEqual(out.status, "pushed")
        # uploaded once, as a draft, with the seo title + markdown body
        self.assertEqual(len(svc._publisher.uploaded), 1)
        call = svc._publisher.uploaded[0]
        self.assertEqual(call["title"], "Docker Buat Pemula")
        self.assertIn("Halo sobat", call["content"])
        # mapping recorded → idempotent next time
        self.assertEqual(drafts.blogger_post("post")["id"], "FAKE-POST-1")
        self.assertTrue(drafts.is_published("post"))
        # stage advanced to published, post_id journalled
        self.assertEqual(svc._current_stage("post"), stages.PUBLISHED)
        meta = journal.entries[-1]["metadata"]
        self.assertEqual(meta["blogger_post_id"], "FAKE-POST-1")
        self.assertIs(meta["live"], False)

    def test_push_returns_url_and_post_id(self):
        svc, journal, drafts = self._approved()
        out = svc.push_draft("post")
        self.assertEqual(out.post_id, "FAKE-POST-1")
        self.assertTrue(out.url.startswith("http"))

    def test_push_records_slug_and_search_description(self):
        # Blogger API can't set permalink/search-description; record them in the
        # mapping so the publisher can apply them in the editor at go-live.
        svc, journal, drafts = self._approved()
        svc.push_draft("post")
        rec = drafts.blogger_post("post")
        self.assertEqual(rec["slug"], "cara-pasang-sesuatu")
        self.assertEqual(rec["search_description"],
                         "deskripsi singkat yang bikin penasaran")


class TestAttachImages(unittest.TestCase):
    """attach_images hosts the article's assets, embeds them into the draft body
    at its <!-- img --> slots (hero first → thumbnail), and updates the post."""

    def _pushed(self, idea_id="post"):
        svc, journal, drafts = build(has_token=True)
        journal.seed(idea_id, stages.PUBLISHED)
        drafts.drafts[idea_id] = good_draft(idea_id=idea_id)  # 1 hero placeholder
        drafts.record_blogger_post(idea_id, {"id": "P1", "url": "http://b/x"})
        return svc, journal, drafts

    def test_attach_requires_published(self):
        svc, journal, drafts = build(has_token=True)
        journal.seed("g", stages.GATED)
        self.assertEqual(svc.attach_images("g").status, "not_pushed")

    def test_attach_no_assets(self):
        svc, journal, drafts = self._pushed()
        self.assertEqual(svc.attach_images("post").status, "no_assets")

    def test_attach_uploads_embeds_and_updates_post(self):
        svc, journal, drafts = self._pushed()
        drafts.seed_assets("post", [("featured-image.webp", "/a/featured-image.webp")])
        out = svc.attach_images("post")
        self.assertEqual(out.status, "attached")
        self.assertEqual(len(svc._image_host.uploaded), 1)
        pid, content = svc._publisher.updated[-1]
        self.assertEqual(pid, "P1")
        self.assertIn("http://img/featured-image.webp", content)
        body, feat = drafts.bodies["post"]
        self.assertIn("http://img/featured-image.webp", body)
        self.assertEqual(feat, "http://img/featured-image.webp")

    def test_attach_orders_assets_by_placeholder(self):
        svc, journal, drafts = self._pushed()
        drafts.drafts["post"] = good_draft(idea_id="post").replace(
            '<!-- img: hero, alt: "gambar utama" -->',
            '<!-- img: hero, alt: "Hero" -->\n<!-- img: tabel perbandingan, alt: "Tabel" -->',
        )
        drafts.seed_assets("post", [
            ("architecture-diagram.webp", "/a/architecture-diagram.webp"),
            ("featured-image.webp", "/a/featured-image.webp"),
            ("comparison-table.webp", "/a/comparison-table.webp"),
        ])
        svc.attach_images("post")
        _, content = svc._publisher.updated[-1]
        self.assertIn("![Hero](http://img/featured-image.webp)", content)
        self.assertIn("![Tabel](http://img/comparison-table.webp)", content)


if __name__ == "__main__":
    unittest.main()
