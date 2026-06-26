"""ContentPilot — SEO Analyzer

Analyzes blog drafts for SEO readiness, readability, and structure.
Generates analysis-report.md with scoring and actionable recommendations.

Based on the Analyst role from blog-lifecycle (SEO scoring 0-100, readability A-F).
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path


# ============================================================
# SEO CHECKS
# ============================================================

@dataclass
class SEOCheck:
    name: str
    status: str  # OK, FAIL, WARN
    detail: str
    weight: int = 0  # for scoring


@dataclass
class ReadabilityResult:
    grade: str  # A-F
    avg_words_per_sentence: float
    long_paragraphs: int  # >3 sentences
    long_sentences: int  # >25 words


@dataclass
class AnalysisResult:
    seo_score: int  # 0-100
    readability: ReadabilityResult
    checks: list[SEOCheck] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    verdict: str = ""  # PASS / PASS WITH WARNINGS / NEEDS REVISION


def analyze_draft(draft_path: str, domain: str = "") -> AnalysisResult:
    """Analyze a draft.md file for SEO and readability."""
    path = Path(draft_path)
    if not path.exists():
        raise FileNotFoundError(f"Draft not found: {draft_path}")

    content = path.read_text()
    seo = _extract_seo_frontmatter(content)
    body = _extract_body(content)

    checks = []
    recommendations = []

    # --- SEO Checks ---

    # 1. Title tag length
    title = seo.get("title", "")
    title_len = len(title)
    if not title:
        checks.append(SEOCheck("Title tag", "FAIL", "Kosong", 15))
        recommendations.append("[HIGH] Title tag kosong → tambahkan judul 50-60 karakter dengan keyword utama")
    elif title_len < 50:
        checks.append(SEOCheck("Title tag", "WARN", f"{title_len} char (min 50)", 15))
        recommendations.append(f"[MED] Title terlalu pendek ({title_len} char) → tambahkan keyword atau detail")
    elif title_len > 60:
        checks.append(SEOCheck("Title tag", "WARN", f"{title_len} char (max 60)", 15))
        recommendations.append(f"[MED] Title terlalu panjang ({title_len} char) → potong agar tidak terpotong di SERP")
    else:
        checks.append(SEOCheck("Title tag", "OK", f"{title_len} char", 15))

    # 2. Meta description length
    meta = seo.get("meta_description", "")
    meta_len = len(meta)
    if not meta:
        checks.append(SEOCheck("Meta description", "FAIL", "Kosong", 15))
        recommendations.append("[HIGH] Meta description kosong → tulis 150-160 karakter dengan keyword + hook")
    elif meta_len < 150:
        checks.append(SEOCheck("Meta description", "WARN", f"{meta_len} char (min 150)", 15))
        recommendations.append(f"[MED] Meta desc terlalu pendek ({meta_len} char) → tambahkan detail")
    elif meta_len > 160:
        checks.append(SEOCheck("Meta description", "WARN", f"{meta_len} char (max 160)", 15))
        recommendations.append(f"[MED] Meta desc terlalu panjang ({meta_len} char) → potong")
    else:
        checks.append(SEOCheck("Meta description", "OK", f"{meta_len} char", 15))

    # 3. Slug
    slug = seo.get("slug", "")
    if not slug:
        checks.append(SEOCheck("Slug", "FAIL", "Kosong", 5))
        recommendations.append("[HIGH] Slug kosong → buat slug lowercase, hyphen-separated, max 5 kata")
    elif len(slug.split("-")) > 5:
        checks.append(SEOCheck("Slug", "WARN", f"{len(slug.split('-'))} kata", 5))
        recommendations.append(f"[LOW] Slug terlalu panjang → maksimal 5 kata")
    else:
        checks.append(SEOCheck("Slug", "OK", f"/{slug}", 5))

    # 4. Keyword placement
    keywords = seo.get("keywords", "")
    keyword = keywords.split(",")[0].strip() if keywords else ""
    if not keyword:
        checks.append(SEOCheck("Keyword placement", "FAIL", "Tidak ada keyword", 20))
        recommendations.append("[HIGH] Keyword kosong → tentukan keyword utama")
    else:
        kw_lower = keyword.lower()
        in_title = kw_lower in title.lower() if title else False
        in_h1 = kw_lower in _get_h1(body).lower() if _get_h1(body) else False
        in_intro = kw_lower in _get_first_paragraph(body).lower() if _get_first_paragraph(body) else False
        body_count = body.lower().count(kw_lower)

        issues = []
        if not in_title:
            issues.append("title")
        if not in_h1:
            issues.append("H1")
        if not in_intro:
            issues.append("paragraf pertama")
        if body_count < 2:
            issues.append(f"body ({body_count}x, min 2x)")

        if issues:
            checks.append(SEOCheck("Keyword placement", "WARN", f"Missing di: {', '.join(issues)}", 20))
            recommendations.append(f"[HIGH] Keyword '{keyword}' tidak ditemukan di: {', '.join(issues)}")
        else:
            checks.append(SEOCheck("Keyword placement", "OK", f"'{keyword}' ditemukan di title, H1, intro, body ({body_count}x)", 20))

    # 5. H1 check
    h1_count = len(re.findall(r"^# \S", body, re.MULTILINE))
    if h1_count == 0:
        checks.append(SEOCheck("H1", "FAIL", "Tidak ada H1", 5))
        recommendations.append("[HIGH] Tidak ada H1 → tambahkan heading # di awal artikel")
    elif h1_count > 1:
        checks.append(SEOCheck("H1", "WARN", f"{h1_count} H1 (seharusnya 1)", 5))
        recommendations.append(f"[MED] {h1_count} H1 ditemukan → harus tepat 1")
    else:
        checks.append(SEOCheck("H1", "OK", "1 H1", 5))

    # 6. H2/H3 structure
    word_count = len(re.findall(r"\w+", body))
    h2_count = len(re.findall(r"^## \S", body, re.MULTILINE))
    if word_count > 1000 and h2_count < 3:
        checks.append(SEOCheck("H2 structure", "WARN", f"{h2_count} H2 untuk {word_count} kata", 15))
        recommendations.append(f"[MED] {h2_count} H2 untuk {word_count} kata → minimal 3 H2 untuk artikel >1000 kata")
    else:
        checks.append(SEOCheck("H2 structure", "OK", f"{h2_count} H2", 15))

    # 7. Internal links
    internal_links = len(re.findall(r"\[.*?\]\((?!http).*?\)", body))
    if internal_links < 2:
        checks.append(SEOCheck("Internal links", "WARN", f"{internal_links} link (min 2)", 10))
        recommendations.append(f"[MED] Internal link hanya {internal_links} → tambahkan minimal 2 link ke artikel lain")
    else:
        checks.append(SEOCheck("Internal links", "OK", f"{internal_links} link", 10))

    # 8. External links
    external_links = len(re.findall(r"\[.*?\]\(https?://.*?\)", body))
    if external_links < 1:
        checks.append(SEOCheck("External links", "WARN", f"{external_links} link", 5))
        recommendations.append(f"[LOW] External link 0 → tambahkan minimal 1 ke sumber otoritatif")
    else:
        checks.append(SEOCheck("External links", "OK", f"{external_links} link", 5))

    # 9. Image alt text
    images = re.findall(r"!\[([^\]]*)\]\([^)]+\)", body)
    images_no_alt = [i for i, alt in enumerate(images) if not alt.strip()]
    if images and images_no_alt:
        checks.append(SEOCheck("Image alt text", "WARN", f"{len(images_no_alt)}/{len(images)} tanpa alt", 10))
        recommendations.append(f"[MED] {len(images_no_alt)} gambar tanpa alt text → tambahkan alt text deskriptif")
    else:
        checks.append(SEOCheck("Image alt text", "OK", f"{len(images)} gambar", 10))

    # 10. Keyword density
    if keyword and word_count > 0:
        kw_count = body.lower().count(keyword.lower())
        density = (kw_count / word_count) * 100
        if density < 1:
            checks.append(SEOCheck("Keyword density", "WARN", f"{density:.1f}% (min 1%)", 5))
            recommendations.append(f"[LOW] Keyword density {density:.1f}% → tambahkan自然地 dalam konteks")
        elif density > 3:
            checks.append(SEOCheck("Keyword density", "WARN", f"{density:.1f}% (max 3%)", 5))
            recommendations.append(f"[LOW] Keyword density {density:.1f}% → terlalu banyak, terlihat spam")
        else:
            checks.append(SEOCheck("Keyword density", "OK", f"{density:.1f}%", 5))

    # --- Readability ---

    readability = _analyze_readability(body)

    if readability.grade in ("D", "F"):
        recommendations.append(f"[HIGH] Readability {readability.grade} → perbaiki struktur paragraf dan kalimat")

    # --- Calculate Score ---

    seo_score = 0
    for check in checks:
        if check.status == "OK":
            seo_score += check.weight
        elif check.status == "WARN":
            seo_score += check.weight // 2

    # --- Verdict ---

    if seo_score >= 80 and readability.grade in ("A", "B"):
        verdict = "PASS"
    elif seo_score >= 60 or readability.grade == "C":
        verdict = "PASS WITH WARNINGS"
    else:
        verdict = "NEEDS REVISION"

    return AnalysisResult(
        seo_score=seo_score,
        readability=readability,
        checks=checks,
        recommendations=recommendations,
        verdict=verdict,
    )


def _extract_seo_frontmatter(content: str) -> dict:
    """Extract SEO fields from YAML frontmatter."""
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}

    frontmatter = match.group(1)
    result = {}
    for line in frontmatter.split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip().strip('"').strip("'")
    return result


def _extract_body(content: str) -> str:
    """Extract body content after frontmatter."""
    return re.sub(r"^---.*?---\s*", "", content, count=1, flags=re.DOTALL)


def _get_h1(body: str) -> str:
    match = re.search(r"^# (.+)$", body, re.MULTILINE)
    return match.group(1) if match else ""


def _get_first_paragraph(body: str) -> str:
    """Get first non-heading, non-empty paragraph."""
    for line in body.split("\n"):
        line = line.strip()
        if line and not line.startswith("#") and not line.startswith("!") and not line.startswith("["):
            return line
    return ""


def _analyze_readability(body: str) -> ReadabilityResult:
    """Analyze readability of body text."""
    sentences = re.split(r"[.!?]+", body)
    sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 5]

    words_per_sentence = []
    for sent in sentences:
        words = len(re.findall(r"\w+", sent))
        words_per_sentence.append(words)

    avg_wps = sum(words_per_sentence) / len(words_per_sentence) if words_per_sentence else 0
    long_sentences = sum(1 for w in words_per_sentence if w > 25)

    # Count paragraphs (separated by blank lines)
    paragraphs = re.split(r"\n\s*\n", body)
    paragraphs = [p.strip() for p in paragraphs if p.strip() and not p.strip().startswith("#")]
    long_paragraphs = sum(1 for p in paragraphs if len(re.split(r"[.!?]+", p)) > 3)

    # Grade
    if avg_wps < 20 and long_paragraphs == 0:
        grade = "A"
    elif avg_wps < 25 and long_paragraphs <= 1:
        grade = "B"
    elif avg_wps < 30:
        grade = "C"
    elif avg_wps < 35:
        grade = "D"
    else:
        grade = "F"

    return ReadabilityResult(
        grade=grade,
        avg_words_per_sentence=round(avg_wps, 1),
        long_paragraphs=long_paragraphs,
        long_sentences=long_sentences,
    )


def format_report(task_id: str, result: AnalysisResult) -> str:
    """Format analysis result as markdown report."""
    lines = [
        f"# Analysis Report — {task_id}",
        "",
        "## Summary",
        f"- **SEO Score**: {result.seo_score}/100",
        f"- **Readability**: {result.readability.grade}",
        f"- **Verdict**: {result.verdict}",
        "",
        "## SEO Detail",
        "| Check | Status | Detail |",
        "|-------|--------|--------|",
    ]

    for check in result.checks:
        icon = {"OK": "✅", "WARN": "⚠️", "FAIL": "❌"}.get(check.status, "")
        lines.append(f"| {check.name} | {icon} {check.status} | {check.detail} |")

    lines.extend([
        "",
        "## Readability Detail",
        f"- Rata-rata kata per kalimat: {result.readability.avg_words_per_sentence}",
        f"- Paragraf >3 kalimat: {result.readability.long_paragraphs} buah",
        f"- Kalimat >25 kata: {result.readability.long_sentences} buah",
        "",
        "## Rekomendasi",
    ])

    if result.recommendations:
        for i, rec in enumerate(result.recommendations, 1):
            lines.append(f"{i}. {rec}")
    else:
        lines.append("- Tidak ada rekomendasi. Artikel sudah siap!")

    return "\n".join(lines)
