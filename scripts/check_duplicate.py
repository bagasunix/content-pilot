#!/usr/bin/env python3
"""
check_duplicate.py — Check if topic already exists on the blog.

Usage:
    python3 scripts/check_duplicate.py "Cara Install Redis di Ubuntu"
    python3 scripts/check_duplicate.py --list  # list all existing articles
"""

import json
import sys
import urllib.request
from html import unescape
import re
from pathlib import Path

def _load_blog_id():
    """Load BLOG_ID from workspace/variables.json or config.yaml."""
    # Try variables.json first (single source of truth)
    vpath = Path(__file__).resolve().parent.parent / "workspace" / "variables.json"
    if vpath.exists():
        data = json.loads(vpath.read_text())
        return data.get("BLOG_ID", "")
    # Fallback: workspace/config.yaml
    cpath = Path(__file__).resolve().parent.parent / "workspace" / "config.yaml"
    if cpath.exists():
        import yaml
        cfg = yaml.safe_load(cpath.read_text())
        return cfg.get("blog_id", "")
    return ""

BLOG_ID = _load_blog_id()
FEED_URL = f"https://www.blogger.com/feeds/{BLOG_ID}/posts/default?max-results=50&alt=json"


def fetch_existing(max_results=50):
    """Fetch existing articles from Blogger feed."""
    url = f"{FEED_URL}&max-results={max_results}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
        posts = data.get("feed", {}).get("entry", [])
        articles = []
        for p in posts:
            title = unescape(p.get("title", {}).get("$t", ""))
            slug = ""
            for link in p.get("link", []):
                if link.get("rel") == "alternate":
                    href = link.get("href", "")
                    slug = href.split("/")[-1].replace(".html", "")
                    break
            articles.append({"title": title, "slug": slug})
        return articles
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return []


def check_overlap(topic, articles):
    """Check if topic overlaps with existing articles."""
    topic_lower = topic.lower()
    # Extract key words (remove common stop words)
    stop_words = {"cara", "di", "untuk", "yang", "dan", "ini", "itu", "dengan", "pada", "dari"}
    topic_words = set(w for w in re.split(r"\s+", topic_lower) if w not in stop_words and len(w) > 2)

    matches = []
    for art in articles:
        title_lower = art["title"].lower()
        title_words = set(re.split(r"\s+", title_lower))
        overlap = topic_words & title_words
        if len(overlap) >= 2:  # at least 2 words in common
            matches.append({"title": art["title"], "slug": art["slug"], "overlap": list(overlap)})

    return matches


def main():
    if len(sys.argv) < 2:
        print("Usage: check_duplicate.py <topic> or check_duplicate.py --list")
        sys.exit(1)

    if sys.argv[1] == "--list":
        articles = fetch_existing()
        print(f"Existing articles: {len(articles)}")
        for a in articles:
            print(f"  - {a['title']} ({a['slug']})")
        return

    topic = sys.argv[1]
    articles = fetch_existing()

    if not articles:
        print(f"OK: No existing articles found. Topic '{topic}' is safe to write.")
        return

    matches = check_overlap(topic, articles)

    if matches:
        print(f"⚠️  POTENTIAL DUPLICATE — {len(matches)} similar article(s) found:")
        for m in matches:
            print(f"  - {m['title']} (overlap: {', '.join(m['overlap'])})")
        print(f"\nSuggestion: Write a different angle or update the existing article.")
    else:
        print(f"OK: No duplicate found for '{topic}'. Safe to write.")


if __name__ == "__main__":
    main()
