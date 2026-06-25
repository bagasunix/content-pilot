#!/usr/bin/env python3
"""
topic_ideas.py — Generate topic ideas based on blog niche + existing articles.

Usage:
    python3 scripts/topic_ideas.py                  # Suggest 5 new topics
    python3 scripts/topic_ideas.py --niche "DevOps" # Suggest topics in niche
    python3 scripts/topic_ideas.py --gap            # Find content gaps
"""

import json
import sys
import urllib.request
from html import unescape
from pathlib import Path

def _load_blog_id():
    """Load BLOG_ID from config.yaml."""
    cpath = Path(__file__).resolve().parent.parent / "config" / "config.yaml"
    if cpath.exists():
        import yaml
        cfg = yaml.safe_load(cpath.read_text())
        return cfg.get("blog_id", "")
    return ""

BLOG_ID = _load_blog_id()
FEED_URL = f"https://www.blogger.com/feeds/{BLOG_ID}/posts/default?max-results=100&alt=json"

# Blog niche categories + trending topic templates
NICHES = {
    "DevOps": {
        "keywords": ["docker", "kubernetes", "nginx", "redis", "postgresql", "mysql", "ci/cd", "jenkins", "github actions", "ansible", "terraform", "linux", "ubuntu", "server"],
        "templates": [
            "Cara Install {tool} di Ubuntu 24.04",
            "Cara Setup {tool} untuk Pemula",
            "Tutorial {tool} Lengkap dari Nol",
            "{tool} vs {tool2}: Mana yang Lebih Baik?",
            "Cara Konfigurasi {tool} di Linux",
            "Troubleshooting {tool}: Error Umum dan Solusinya",
            "Best Practices {tool} untuk Production",
        ]
    },
    "Android": {
        "keywords": ["android", "google play", "apk", "samsung", "xiaomi", "pixel", "launcher", "widget", "battery", "storage"],
        "templates": [
            "Cara Install Aplikasi di Android {version}",
            "Tips Productivity untuk Pengguna Android",
            "Aplikasi Productivity Terbaik untuk Android",
            "Cara Mengatasi Android Lambat di Android",
            "Cara Install Tanpa Root di Android",
        ]
    },
    "Web Dev": {
        "keywords": ["html", "css", "javascript", "react", "nodejs", "python", "api", "database", "frontend", "backend"],
        "templates": [
            "Tutorial {framework} untuk Pemula",
            "Cara Membuat {project} dengan {framework}",
            "{framework} vs {framework2}: Perbandingan 2026",
            "Tips Optimasi {tech} untuk Performa",
            "Cara Deploy {project} ke Production",
        ]
    },
    "Cybersecurity": {
        "keywords": ["security", "hacking", "pentest", "firewall", "ssl", "vpn", "password", "encryption", "malware", "phishing"],
        "templates": [
            "Cara Install VPN untuk Pemula",
            "Tips Keamanan Server yang Wajib Diketahui",
            "Server Security Checklist untuk Developer",
            "Cara Mendeteksi Malware di Linux",
        ]
    },
    "AI/Tech News": {
        "keywords": ["ai", "chatgpt", "machine learning", "deep learning", "automation", "gpt", "llm", "copilot", "gemini"],
        "templates": [
            "Cara Pakai {tool} untuk Productivity",
            "{tool} vs {tool2}: Mana yang Lebih Baik?",
            "Tutorial {tool} Lengkap untuk Pemula",
            "Tips Automasi dengan {tool}",
        ]
    }
}


def fetch_existing():
    """Fetch existing articles."""
    try:
        req = urllib.request.Request(FEED_URL, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
        posts = data.get("feed", {}).get("entry", [])
        return [unescape(p.get("title", {}).get("$t", "")) for p in posts]
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return []


def detect_niches(existing):
    """Detect which niches the blog covers based on existing articles."""
    scores = {}
    for niche, info in NICHES.items():
        score = 0
        for art in existing:
            art_lower = art.lower()
            for kw in info["keywords"]:
                if kw in art_lower:
                    score += 1
        scores[niche] = score
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)


def suggest_topics(niche, existing, count=5):
    """Suggest topics in a specific niche."""
    import random
    info = NICHES.get(niche, list(NICHES.values())[0])
    
    # Find gaps — tools/topics not yet covered
    existing_lower = " ".join(existing).lower()
    uncovered_tools = [kw for kw in info["keywords"] if kw not in existing_lower]
    
    suggestions = []
    for template in info["templates"]:
        if "{tool}" in template and uncovered_tools:
            tool = random.choice(uncovered_tools)
            if "{tool2}" in template:
                tool2 = random.choice([t for t in info["keywords"] if t != tool][:5])
                topic = template.format(tool=tool.title(), tool2=tool2.title())
            else:
                topic = template.format(tool=tool.title())
            suggestions.append(topic)
        elif "{framework}" in template:
            suggestions.append(template.format(framework="Docker", framework2="Podman", tech="API", project="REST API"))
        elif "{action}" in template:
            suggestions.append(template.format(action="Install", topic="Productivity", problem="Lambat", version="24.04"))
        elif "{tool}" not in template and "{framework}" not in template:
            suggestions.append(template)
    
    # Remove duplicates and existing
    seen = set()
    unique = []
    for s in suggestions:
        s_lower = s.lower()
        if s_lower not in seen and not any(s_lower in e.lower() for e in existing):
            seen.add(s_lower)
            unique.append(s)
    
    return unique[:count]


def find_gaps(existing):
    """Find content gaps — niches with few articles."""
    niche_counts = {niche: 0 for niche in NICHES}
    for art in existing:
        art_lower = art.lower()
        for niche, info in NICHES.items():
            for kw in info["keywords"]:
                if kw in art_lower:
                    niche_counts[niche] += 1
                    break
    
    # Find underrepresented niches
    gaps = []
    for niche, count in sorted(niche_counts.items(), key=lambda x: x[1]):
        if count < 5:
            gaps.append(f"{niche} ({count} articles) — banyak topik belum tercakup")
    
    return gaps, niche_counts


def main():
    existing = fetch_existing()
    if not existing:
        print("ERROR: Could not fetch existing articles")
        sys.exit(1)

    print(f"Blog memiliki {len(existing)} artikel existing.\n")

    if len(sys.argv) > 1 and sys.argv[1] == "--niche" and len(sys.argv) > 2:
        niche = sys.argv[2]
        print(f"=== Topik di niche: {niche} ===")
        topics = suggest_topics(niche, existing)
        for i, t in enumerate(topics, 1):
            print(f"  {i}. {t}")

    elif len(sys.argv) > 1 and sys.argv[1] == "--gap":
        print("=== Content Gaps ===")
        gaps, counts = find_gaps(existing)
        print("Niche coverage:")
        for niche, count in counts.items():
            bar = "█" * count + "░" * (10 - count)
            print(f"  {niche:15s} {bar} {count}")
        print("\nGaps:")
        for g in gaps:
            print(f"  - {g}")
        print("\n=== Topik yang disarankan ===")
        for niche, count in counts.items():
            if count < 5:
                topics = suggest_topics(niche, existing, count=3)
                for t in topics:
                    print(f"  [{niche}] {t}")

    else:
        # Default: suggest from top niche
        niches = detect_niches(existing)
        print("=== Blog Niche Analysis ===")
        for niche, score in niches:
            bar = "█" * score + "░" * (20 - score)
            print(f"  {niche:15s} {bar} {score} articles")
        
        print("\n=== Topik yang Disarankan ===")
        top_niche = niches[0][0]
        print(f"(Based on dominant niche: {top_niche})\n")
        topics = suggest_topics(top_niche, existing)
        for i, t in enumerate(topics, 1):
            print(f"  {i}. {t}")


if __name__ == "__main__":
    main()
