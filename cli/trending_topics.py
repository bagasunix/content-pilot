#!/usr/bin/env python3
"""
trending_topics.py — Find trending topics relevant to blog niche.

Usage:
    python3 scripts/trending_topics.py                  # All trending in blog niche
    python3 scripts/trending_topics.py --region ID       # Indonesia trending
    python3 scripts/trending_topics.py --source google   # Google Trends only
    python3 scripts/trending_topics.py --source hackernews  # Hacker News only
"""

import json
import sys
import urllib.request
from html import unescape
import re

# Blog niche keywords (from topic_ideas.py)
NICHES = {
    "DevOps": ["docker", "kubernetes", "nginx", "redis", "postgresql", "linux", "ubuntu", "server", "ci/cd", "terraform", "ansible", "jenkins", "grafana", "prometheus", "ssh", "bash", "devops", "cloud", "aws", "gcp", "azure"],
    "Android": ["android", "samsung", "xiaomi", "pixel", "google play", "apk", "launcher", "widget", "battery", "android 15", "android 16"],
    "Web Dev": ["javascript", "react", "nodejs", "python", "html", "css", "api", "database", "frontend", "backend", "nextjs", "typescript", "tailwind", "fastapi", "django"],
    "Cybersecurity": ["security", "hacking", "pentest", "firewall", "ssl", "vpn", "malware", "phishing", "encryption", "vulnerability", "cve", "zero-day"],
    "AI/Tech News": ["ai", "chatgpt", "openai", "google gemini", "claude", "machine learning", "deep learning", "llm", "gpt", "copilot", "stable diffusion", "midjourney", "automation", "robot"]
}


def fetch_google_trending():
    """Fetch Google trending searches (Indonesia)."""
    url = "https://trends.google.com/trending?geo=ID&hours=24"
    # Google Trends doesn't have a public API, so we scrape trending topics
    # from alternative sources
    try:
        # Use RSS feed from Google News
        rss_url = "https://news.google.com/rss?hl=id&gl=ID&ceid=ID:id"
        req = urllib.request.Request(rss_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read().decode("utf-8")
        
        # Parse RSS items
        titles = re.findall(r"<title>(.*?)</title>", content)
        # Skip first item (feed title)
        return [unescape(t) for t in titles[1:20] if t.strip()]
    except Exception as e:
        print(f"Warning: Could not fetch Google trending: {e}", file=sys.stderr)
        return []


def fetch_hackernews():
    """Fetch top stories from Hacker News."""
    try:
        # Get top story IDs
        req = urllib.request.Request(
            "https://hacker-news.firebaseio.com/v0/topstories.json",
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            story_ids = json.loads(resp.read())[:20]
        
        # Get story details
        stories = []
        for sid in story_ids[:15]:
            try:
                req = urllib.request.Request(
                    f"https://hacker-news.firebaseio.com/v0/item/{sid}.json",
                    headers={"User-Agent": "Mozilla/5.0"}
                )
                with urllib.request.urlopen(req, timeout=5) as resp:
                    story = json.loads(resp.read())
                title = story.get("title", "")
                url = story.get("url", "")
                score = story.get("score", 0)
                stories.append({"title": title, "url": url, "score": score})
            except:
                continue
        return stories
    except Exception as e:
        print(f"Warning: Could not fetch Hacker News: {e}", file=sys.stderr)
        return []


def fetch_producthunt():
    """Fetch top products from Product Hunt (via RSS)."""
    try:
        rss_url = "https://www.producthunt.com/feed"
        req = urllib.request.Request(rss_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read().decode("utf-8")
        titles = re.findall(r"<title><!\[CDATA\[(.*?)\]\]></title>", content)
        if not titles:
            titles = re.findall(r"<title>(.*?)</title>", content)
        return [unescape(t) for t in titles[:10] if t.strip()]
    except Exception as e:
        print(f"Warning: Could not fetch Product Hunt: {e}", file=sys.stderr)
        return []


def match_niche(text, niches):
    """Check which niches a text matches."""
    text_lower = text.lower()
    matches = []
    for niche, keywords in niches.items():
        for kw in keywords:
            if kw in text_lower:
                matches.append(niche)
                break
    return matches


def suggest_from_trending(trending_items, niches, source_name):
    """Filter trending items that match blog niches."""
    suggestions = []
    for item in trending_items:
        title = item["title"] if isinstance(item, dict) else item
        matched_niches = match_niche(title, niches)
        if matched_niches:
            suggestions.append({
                "title": title,
                "niches": matched_niches,
                "source": source_name,
                "url": item.get("url", "") if isinstance(item, dict) else "",
                "score": item.get("score", 0) if isinstance(item, dict) else 0
            })
    return suggestions


def main():
    source = "all"
    if len(sys.argv) > 2 and sys.argv[1] == "--source":
        source = sys.argv[2]

    print("=== Trending Topics (Blog Niche Filtered) ===\n")

    all_suggestions = []

    # Google News trending
    if source in ("all", "google", "news"):
        print("Fetching Google News trending...")
        trending = fetch_google_trending()
        suggestions = suggest_from_trending(trending, NICHES, "Google News")
        all_suggestions.extend(suggestions)
        print(f"  Found {len(trending)} trending, {len(suggestions)} match blog niche\n")

    # Hacker News
    if source in ("all", "hackernews", "hn"):
        print("Fetching Hacker News top stories...")
        stories = fetch_hackernews()
        suggestions = suggest_from_trending(stories, NICHES, "Hacker News")
        all_suggestions.extend(suggestions)
        print(f"  Found {len(stories)} stories, {len(suggestions)} match blog niche\n")

    # Product Hunt
    if source in ("all", "producthunt", "ph"):
        print("Fetching Product Hunt trending...")
        products = fetch_producthunt()
        suggestions = suggest_from_trending(products, NICHES, "Product Hunt")
        all_suggestions.extend(suggestions)
        print(f"  Found {len(products)} products, {len(suggestions)} match blog niche\n")

    if not all_suggestions:
        print("No trending topics match blog niches.")
        print("\nTip: Run 'topic_ideas.py --gap' for content gap analysis instead.")
        return

    # Sort by relevance (more niche matches = more relevant)
    all_suggestions.sort(key=lambda x: len(x["niches"]), reverse=True)

    print(f"=== {len(all_suggestions)} Trending Topics Match Blog Niche ===\n")
    for i, s in enumerate(all_suggestions, 1):
        niches_str = ", ".join(s["niches"])
        score_str = f" (score: {s['score']})" if s["score"] else ""
        print(f"  {i}. [{niches_str}] {s['title']}{score_str}")
        if s["url"]:
            print(f"     {s['url']}")
        print()


if __name__ == "__main__":
    main()
