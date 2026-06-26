"""Embed hosted image URLs into a draft body at its <!-- img: ... --> markers.

The writer/imagery handoff leaves placeholders like
    <!-- img: hero image, alt: "Teks alt" -->
in the body. This replaces each one (in order) with real markdown
`![alt](url)`, pulling the alt text from the placeholder so the writer's intent
is preserved. Extra placeholders with no URL are left untouched.
"""
from __future__ import annotations

import re

_PLACEHOLDER_RE = re.compile(r"<!--\s*img:(.*?)-->", re.DOTALL)
_ALT_RE = re.compile(r'alt:\s*"([^"]*)"')
_TOKEN_RE = re.compile(r"[a-z]+")

# Canonicalise ID/EN synonyms so a placeholder's words match a filename's.
_SYNONYMS = {
    "featured": "hero",
    "tabel": "table",
    "perbandingan": "comparison",
    "arsitektur": "architecture",
    "foto": "image",
    "gambar": "image",
    "layar": "screenshot",
    "tangkapan": "screenshot",
}


def _tokens(text: str) -> set[str]:
    return {_SYNONYMS.get(t, t) for t in _TOKEN_RE.findall(text.lower())}


def order_assets_for_placeholders(body: str, asset_names: list[str]) -> list[str]:
    """Order asset filenames to align with the body's <!-- img --> placeholders.

    Each placeholder is matched to the asset whose filename shares the most
    keywords (ID/EN synonyms folded), greedily. Assets matching no placeholder
    are appended in their original order. Avoids the alphabetical-zip bug where
    a 'comparison table' slot wrongly got the 'architecture diagram' image.
    """
    placeholders = [m.group(1) for m in _PLACEHOLDER_RE.finditer(body)]
    if not placeholders:
        return list(asset_names)

    remaining = list(asset_names)
    ordered: list[str] = []
    for ph in placeholders:
        ph_tokens = _tokens(ph)
        best, best_score = None, 0
        for name in remaining:
            score = len(ph_tokens & _tokens(name.rsplit(".", 1)[0]))
            if score > best_score:
                best, best_score = name, score
        if best is not None:
            ordered.append(best)
            remaining.remove(best)
    ordered.extend(remaining)  # leftovers (no matching placeholder)
    return ordered


def embed_images(body: str, urls: list[str]) -> str:
    it = iter(urls)

    def _repl(m: re.Match) -> str:
        url = next(it, None)
        if url is None:
            return m.group(0)  # ran out of URLs — leave the placeholder as-is
        inner = m.group(1)
        am = _ALT_RE.search(inner)
        alt = am.group(1) if am else inner.strip()
        return f"![{alt}]({url})"

    return _PLACEHOLDER_RE.sub(_repl, body)
