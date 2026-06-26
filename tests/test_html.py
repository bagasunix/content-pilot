"""Tests for the stdlib markdown→HTML converter (no external deps)."""
import unittest

from blog.infrastructure.html import markdown_to_html


class TestMarkdownToHtml(unittest.TestCase):
    def test_paragraph(self):
        self.assertIn("<p>Halo sobat.</p>", markdown_to_html("Halo sobat."))

    def test_headings(self):
        html = markdown_to_html("# Judul\n\n## Sub")
        self.assertIn("<h1>Judul</h1>", html)
        self.assertIn("<h2>Sub</h2>", html)

    def test_bold_and_inline_code(self):
        html = markdown_to_html("Ini **tebal** dan `kode`.")
        self.assertIn("<strong>tebal</strong>", html)
        self.assertIn("<code>kode</code>", html)

    def test_link(self):
        html = markdown_to_html("Lihat [docs](https://docs.docker.com).")
        self.assertIn('<a href="https://docs.docker.com">docs</a>', html)

    def test_image(self):
        html = markdown_to_html("![Diagram arsitektur](https://x/y.webp)")
        self.assertIn('<img src="https://x/y.webp" alt="Diagram arsitektur"', html)

    def test_fenced_code_block(self):
        html = markdown_to_html("```bash\necho halo\n```")
        self.assertIn("<pre><code", html)
        self.assertIn("echo halo", html)
        # content inside a code fence must NOT be treated as markdown
        self.assertNotIn("<strong>", markdown_to_html("```\n**x**\n```"))

    def test_unordered_list(self):
        html = markdown_to_html("- satu\n- dua")
        self.assertIn("<ul>", html)
        self.assertEqual(html.count("<li>"), 2)

    def test_html_escape_in_text(self):
        html = markdown_to_html("a < b & c")
        self.assertIn("a &lt; b &amp; c", html)

    def test_strips_html_comments(self):
        # Imagery leaves <!-- img: ... --> placeholders; they must never render
        # as visible escaped text on Blogger.
        html = markdown_to_html("<!-- img: hero, alt: x -->\n\nHalo sobat.")
        self.assertNotIn("img:", html)
        self.assertNotIn("&lt;!--", html)
        self.assertIn("<p>Halo sobat.</p>", html)


if __name__ == "__main__":
    unittest.main()
