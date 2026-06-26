"""Tests for embedding image URLs into a draft body at <!-- img --> placeholders."""
import unittest

from blog.domain.images import embed_images, order_assets_for_placeholders


class TestEmbedImages(unittest.TestCase):
    def test_replaces_placeholder_with_image_using_its_alt(self):
        body = 'Intro.\n\n<!-- img: hero, alt: "Foto keren" -->\n\nLanjut.'
        out = embed_images(body, ["https://x/y.webp"])
        self.assertIn("![Foto keren](https://x/y.webp)", out)
        self.assertNotIn("<!-- img", out)

    def test_replaces_in_order(self):
        body = '<!-- img: a, alt: "satu" -->\nteks\n<!-- img: b, alt: "dua" -->'
        out = embed_images(body, ["http://u/1", "http://u/2"])
        self.assertIn("![satu](http://u/1)", out)
        self.assertIn("![dua](http://u/2)", out)

    def test_leaves_extra_placeholder_when_fewer_urls(self):
        body = '<!-- img: a, alt: "satu" -->\n<!-- img: b, alt: "dua" -->'
        out = embed_images(body, ["http://u/1"])
        self.assertIn("![satu](http://u/1)", out)
        self.assertIn("<!-- img: b", out)  # second placeholder untouched

    def test_falls_back_to_raw_text_when_no_alt_field(self):
        body = "<!-- img: diagram arsitektur -->"
        out = embed_images(body, ["http://u/d"])
        self.assertIn("![diagram arsitektur](http://u/d)", out)

    def test_no_placeholder_returns_body_unchanged(self):
        body = "Tidak ada gambar di sini."
        self.assertEqual(embed_images(body, ["http://u/1"]), body)


class TestOrderAssetsForPlaceholders(unittest.TestCase):
    def test_matches_by_keyword_not_alphabetical(self):
        body = (
            '<!-- img: hero image, alt: "Foto hero" -->\n'
            '<!-- img: screenshot tabel perbandingan, alt: "Tabel perbandingan" -->'
        )
        assets = ["featured-image.webp", "architecture-diagram.webp", "comparison-table.webp"]
        out = order_assets_for_placeholders(body, assets)
        # placeholder order: hero→featured, tabel→comparison; leftover appended
        self.assertEqual(out[0], "featured-image.webp")
        self.assertEqual(out[1], "comparison-table.webp")
        self.assertIn("architecture-diagram.webp", out)

    def test_indonesian_synonyms(self):
        body = '<!-- img: diagram arsitektur sistem -->'
        assets = ["comparison-table.webp", "architecture-diagram.webp"]
        out = order_assets_for_placeholders(body, assets)
        self.assertEqual(out[0], "architecture-diagram.webp")

    def test_no_placeholders_returns_assets_as_is(self):
        out = order_assets_for_placeholders("teks biasa", ["a.webp", "b.webp"])
        self.assertEqual(out, ["a.webp", "b.webp"])


if __name__ == "__main__":
    unittest.main()
