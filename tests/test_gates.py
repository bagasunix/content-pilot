"""Domain gate rules — pure, no I/O."""
import unittest

from blog.domain import gates
from blog.domain.article import Draft

from .fakes import good_draft
from blog.infrastructure.draft_store import split_frontmatter


def _draft(raw, idea_id="x"):
    fm, body = split_frontmatter(raw)
    return Draft(idea_id=idea_id, raw=raw, frontmatter=fm, body=body)


class TestGates(unittest.TestCase):
    def test_complete_draft_passes(self):
        res = gates.evaluate(_draft(good_draft()))
        self.assertTrue(res.passed, res.failures)

    def test_empty_template_fails_with_reasons(self):
        raw = f"---\nseo:\n  title: \"\"\n---\n\n# {gates.TITLE_PLACEHOLDER}\n\nsingkat.\n"
        res = gates.evaluate(_draft(raw))
        self.assertFalse(res.passed)
        joined = " ".join(res.failures)
        self.assertIn("placeholder", joined)
        self.assertIn("seo.title", joined)
        self.assertIn("terlalu pendek", joined)

    def test_ai_tell_is_hard_fail(self):
        raw = good_draft().replace("Halo sobat,", "Di era digital saat ini,")
        res = gates.evaluate(_draft(raw))
        self.assertFalse(res.passed)
        self.assertTrue(any("di era digital" in f for f in res.failures))

    def test_ai_tell_inside_comment_is_ignored(self):
        raw = good_draft().replace("Halo sobat,", "<!-- di era digital --> Halo sobat,")
        res = gates.evaluate(_draft(raw))
        self.assertTrue(res.passed, res.failures)

    def test_anda_is_warning_not_failure(self):
        raw = good_draft().replace("Halo sobat", "Halo Anda")
        res = gates.evaluate(_draft(raw))
        self.assertTrue(res.passed, res.failures)
        self.assertTrue(any("Anda" in w for w in res.warnings))

    # ── §6 unresolved marker detection ────────────────────────────────────

    def test_todo_marker_is_hard_fail(self):
        raw = good_draft().replace("Halo sobat,", "Halo sobat, TODO(owner) ini harus diisi.")
        res = gates.evaluate(_draft(raw))
        self.assertFalse(res.passed)
        self.assertTrue(any("TODO(" in f for f in res.failures))

    def test_fixme_marker_is_hard_fail(self):
        raw = good_draft().replace("Halo sobat,", "FIXME(perlu dicek) lagi nih.")
        res = gates.evaluate(_draft(raw))
        self.assertFalse(res.passed)
        self.assertTrue(any("FIXME" in f for f in res.failures))

    def test_hack_marker_is_hard_fail(self):
        raw = good_draft().replace("Halo sobat,", "Halo sobat, HACK(biar cepet aja).")
        res = gates.evaluate(_draft(raw))
        self.assertFalse(res.passed)
        self.assertTrue(any("HACK(" in f for f in res.failures))

    def test_reducted_marker_is_hard_fail(self):
        raw = good_draft().replace("Halo sobat,", "Data sensitif: [REDACTED] jangan publish.")
        res = gates.evaluate(_draft(raw))
        self.assertFalse(res.passed)
        self.assertTrue(any("[REDACTED]" in f for f in res.failures))

    def test_marker_inside_comment_is_ignored(self):
        raw = good_draft().replace("Halo sobat,", "<!-- TODO(owner) --> Halo sobat,")
        res = gates.evaluate(_draft(raw))
        self.assertTrue(res.passed, res.failures)

    def test_clean_draft_still_passes(self):
        raw = good_draft()
        res = gates.evaluate(_draft(raw))
        self.assertTrue(res.passed, res.failures)

    # ── featured-image requirement ─────────────────────────────────────────

    def test_missing_image_is_hard_fail(self):
        raw = good_draft()
        # strip the image placeholder good_draft ships with
        raw = raw.replace('<!-- img: hero, alt: "gambar utama" -->', "")
        res = gates.evaluate(_draft(raw))
        self.assertFalse(res.passed)
        self.assertTrue(any("gambar" in f.lower() for f in res.failures))

    def test_image_placeholder_satisfies_requirement(self):
        raw = good_draft()  # ships with a <!-- img --> placeholder
        res = gates.evaluate(_draft(raw))
        self.assertTrue(res.passed, res.failures)

    def test_real_markdown_image_satisfies_requirement(self):
        raw = good_draft().replace(
            '<!-- img: hero, alt: "gambar utama" -->',
            "![hero](https://x/y.webp)",
        )
        res = gates.evaluate(_draft(raw), check_links=False)
        self.assertTrue(res.passed, res.failures)


if __name__ == "__main__":
    unittest.main()
