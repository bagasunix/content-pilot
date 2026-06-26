"""Tests for link_validator module."""
import pytest
from blog.domain.link_validator import (
    extract_links,
    get_domain,
    classify_domain,
    validate_links,
    format_report,
    HOAX_DOMAINS,
    TRUSTED_DOMAINS,
    TRUSTED_TLDS,
)


class TestExtractLinks:
    def test_markdown_links(self):
        content = "Check [this source](https://arxiv.org/abs/1234) and [that](https://github.com/repo)"
        urls = extract_links(content)
        assert "https://arxiv.org/abs/1234" in urls
        assert "https://github.com/repo" in urls

    def test_html_href(self):
        content = '<a href="https://docs.python.org/3/library/">docs</a>'
        urls = extract_links(content)
        assert "https://docs.python.org/3/library/" in urls

    def test_bare_urls(self):
        content = "Visit https://example.com/page for more info."
        urls = extract_links(content)
        assert "https://example.com/page" in urls

    def test_no_duplicates(self):
        content = "[link](https://example.com) and https://example.com again"
        urls = extract_links(content)
        assert urls.count("https://example.com") == 1

    def test_no_links(self):
        content = "This article has no links at all."
        urls = extract_links(content)
        assert urls == []

    def test_ignores_internal_anchors(self):
        content = "See [section](#heading) for details."
        urls = extract_links(content)
        assert urls == []

    def test_strips_trailing_backtick(self):
        # Inline code: `https://example.com/page` — the closing backtick and
        # following punctuation must NOT be swallowed into the URL.
        content = "Buka `https://example.com/page`. lalu lanjut."
        urls = extract_links(content)
        assert "https://example.com/page" in urls
        assert all("`" not in u for u in urls)

    def test_strips_trailing_punctuation(self):
        content = "Kunjungi https://example.com/page, terus https://example.org/x."
        urls = extract_links(content)
        assert "https://example.com/page" in urls
        assert "https://example.org/x" in urls


class TestLocalHostsSkipped:
    """Local / non-routable hosts are legit in tutorials and must never be
    HTTP-checked or counted as dead links (offline, no network needed)."""

    def test_localhost_inline_code_not_failed(self):
        content = (
            "Buka browser: `http://localhost:8080`\n\n"
            "Test: `http://localhost:3000`. Kalau muncul pesan berarti sukses."
        )
        result = validate_links(content, check_http=True)
        assert result.passed
        assert result.failures == []

    def test_loopback_ip_skipped(self):
        content = "Server jalan di http://127.0.0.1:5000/health untuk dicek."
        result = validate_links(content, check_http=True)
        assert result.passed
        assert result.failures == []


class TestGetDomain:
    def test_basic(self):
        assert get_domain("https://www.example.com/path") == "example.com"

    def test_subdomain(self):
        assert get_domain("https://docs.python.org/3/") == "docs.python.org"

    def test_no_www(self):
        assert get_domain("https://github.com/repo") == "github.com"


class TestClassifyDomain:
    def test_hoax_domain(self):
        assert classify_domain("infowars.com") == "hoax"
        assert classify_domain("naturalnews.com") == "hoax"

    def test_hoax_subdomain(self):
        assert classify_domain("news.infowars.com") == "hoax"

    def test_trusted_domain(self):
        assert classify_domain("github.com") == "high"
        assert classify_domain("arxiv.org") == "high"
        assert classify_domain("scholar.google.com") == "high"

    def test_trusted_tld(self):
        assert classify_domain("mit.edu") == "high"
        assert classify_domain("ui.ac.id") == "high"
        assert classify_domain("kemkes.go.id") == "high"

    def test_unknown_domain(self):
        assert classify_domain("randomsite123.com") == "medium"

    def test_trusted_subdomain(self):
        assert classify_domain("en.wikipedia.org") == "high"


class TestValidateLinksOffline:
    """Test validate_links with check_http=False (domain-only checks)."""

    def test_hoax_link_fails(self):
        content = "Menurut [sumber](https://infowars.com/article/123) ini benar."
        result = validate_links(content, check_http=False)
        assert not result.passed
        assert any("HOAX" in f for f in result.failures)

    def test_clean_links_pass(self):
        content = (
            "Referensi dari [GitHub](https://github.com/project) "
            "dan [Wikipedia](https://en.wikipedia.org/wiki/Topic)."
        )
        result = validate_links(content, check_http=False)
        assert result.passed

    def test_no_links_warning(self):
        content = "Artikel tanpa referensi external apapun."
        result = validate_links(content, check_http=False)
        assert result.passed  # warning, not failure
        assert any("Tidak ada external link" in w for w in result.warnings)

    def test_multiple_hoax_links(self):
        content = (
            "Source [1](https://naturalnews.com/x) "
            "dan [2](https://beforeitsnews.com/y)."
        )
        result = validate_links(content, check_http=False)
        assert not result.passed
        assert len(result.failures) == 2


class TestFormatReport:
    def test_clean_report(self):
        content = "See [docs](https://docs.python.org/3/) for reference."
        result = validate_links(content, check_http=False)
        report = format_report(result)
        assert "1 links ditemukan" in report

    def test_failure_report(self):
        content = "Bad source [here](https://infowars.com/fake)."
        result = validate_links(content, check_http=False)
        report = format_report(result)
        assert "FAILURES" in report
        assert "HOAX" in report


class TestGatesIntegration:
    """Test that link validation is integrated into gates.evaluate()."""

    def test_gate_catches_hoax_link(self):
        from blog.domain.article import Draft
        from blog.domain.gates import evaluate

        raw = """---
seo:
  title: "Test Article"
  meta_description: "Test desc"
  slug: "test-article"
  keywords: ["test"]
---
# Test Article

Ini artikel test dengan sumber dari [sini](https://infowars.com/article).
Perlu ditambah banyak kata supaya memenuhi syarat minimum kata yang diperlukan.
""" + ("Lorem ipsum dolor sit amet. " * 50)

        draft = Draft(
            idea_id="test-001",
            raw=raw,
            frontmatter={
                "seo": {
                    "title": "Test Article",
                    "meta_description": "Test desc",
                    "slug": "test-article",
                    "keywords": ["test"],
                }
            },
            body=raw.split("---", 2)[2].strip(),
        )
        result = evaluate(draft, check_links=False)
        # Should fail because of hoax link
        hoax_failures = [f for f in result.failures if "HOAX" in f]
        assert len(hoax_failures) > 0

    def test_gate_passes_clean_links(self):
        from blog.domain.article import Draft
        from blog.domain.gates import evaluate

        raw = """---
seo:
  title: "Clean Article"
  meta_description: "Good desc"
  slug: "clean-article"
  keywords: ["clean"]
---
# Clean Article

Referensi dari [GitHub](https://github.com/project) dan
[Python docs](https://docs.python.org/3/library/). Artikel ini cukup panjang
supaya lewat gate minimum kata yang diperlukan oleh sistem editorial.
""" + ("Konten tambahan yang relevan dan informatif. " * 50)

        draft = Draft(
            idea_id="clean-001",
            raw=raw,
            frontmatter={
                "seo": {
                    "title": "Clean Article",
                    "meta_description": "Good desc",
                    "slug": "clean-article",
                    "keywords": ["clean"],
                }
            },
            body=raw.split("---", 2)[2].strip(),
        )
        result = evaluate(draft, check_links=False)
        # No hoax failures
        hoax_failures = [f for f in result.failures if "HOAX" in f]
        assert len(hoax_failures) == 0
