"""ContentPilot — Blogger API Client

Read existing posts from user's Blogger blog.
Analyze content for topic suggestions.
"""
import json
import re
from collections import Counter
from pathlib import Path
from typing import List, Dict, Optional


class BloggerClient:
    """Read posts from Blogger blog via RSS feed."""
    
    def __init__(self, blog_id: str = None, domain: str = None):
        self.blog_id = blog_id
        self.domain = domain
        self.feed_url = f"https://www.blogger.com/feeds/{blog_id}/posts/default?max-results=100&alt=json"
    
    def fetch_posts(self, max_results: int = 50) -> List[Dict]:
        """Fetch existing posts from blog."""
        import urllib.request
        import xml.etree.ElementTree as ET
        
        posts = []
        try:
            url = self.feed_url + f"&max-results={max_results}"
            req = urllib.request.Request(url, headers={"User-Agent": "ContentPilot/1.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                xml_data = resp.read().decode("utf-8")
                root = ET.fromstring(xml_data)
                
                ns = {"atom": "http://www.w3.org/2005/Atom"}
                for entry in root.findall(".//atom:entry", ns):
                    title = entry.find("atom:title", ns)
                    content = entry.find("atom:content", ns)
                    published = entry.find("atom:published", ns)
                    
                    if title is not None:
                        posts.append({
                            "title": title.text or "",
                            "content": content.text if content is not None else "",
                            "published": published.text if published is not None else "",
                        })
        except Exception as e:
            print(f"Error fetching posts: {e}")
        
        return posts
    
    def extract_topics(self, posts: List[Dict]) -> List[str]:
        """Extract main topics/keywords from posts."""
        topics = []
        for post in posts:
            title = post.get("title", "")
            if title:
                # Clean and extract meaningful words
                words = re.findall(r'\b\w+\b', title.lower())
                # Filter out common words
                stop_words = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'in', 'on', 'at',
                             'to', 'for', 'of', 'with', 'by', 'from', 'and', 'or', 'but',
                             'cara', 'untuk', 'dengan', 'yang', 'di', 'dari', 'ke', 'ini',
                             'itu', 'ada', 'tidak', 'bisa', 'akan', 'sudah', 'lebih'}
                meaningful = [w for w in words if w not in stop_words and len(w) > 2]
                topics.extend(meaningful)
        
        return topics
    
    def extract_categories(self, posts: List[Dict]) -> Dict[str, int]:
        """Extract categories from posts."""
        categories = Counter()
        
        # Common category patterns in Indonesian tech blogs
        category_keywords = {
            "DevOps": ["docker", "kubernetes", "linux", "ubuntu", "server", "nginx", "deploy", "ci/cd", "git"],
            "AI/Tech": ["ai", "gpt", "machine learning", "python", "api", "openai", "chatgpt"],
            "Web Dev": ["react", "vue", "angular", "javascript", "html", "css", "web", "frontend", "backend"],
            "Security": ["security", "hack", "vulnerability", "password", "encryption", "firewall"],
            "Tutorial": ["tutorial", "cara", "panduan", "step", "guide", "belajar"],
            "Review": ["review", "versus", "vs", "comparison", "perbandingan"],
        }
        
        for post in posts:
            title_lower = post.get("title", "").lower()
            content_lower = post.get("content", "").lower()[:500]  # First 500 chars
            
            for category, keywords in category_keywords.items():
                for kw in keywords:
                    if kw in title_lower or kw in content_lower:
                        categories[category] += 1
                        break
        
        return dict(categories.most_common())
    
    def get_content_gaps(self, posts: List[Dict], trending_topics: List[Dict]) -> List[Dict]:
        """Find content gaps — topics trending but not yet written."""
        existing_titles = {post["title"].lower() for post in posts}
        existing_topics = set(self.extract_topics(posts))
        
        gaps = []
        for topic in trending_topics:
            title = topic.get("title", "")
            title_lower = title.lower()
            
            # Check if similar topic already exists
            already_exists = False
            for existing in existing_titles:
                # Simple similarity check
                existing_words = set(existing.split())
                topic_words = set(title_lower.split())
                overlap = len(existing_words & topic_words)
                if overlap >= 2:  # At least 2 words overlap
                    already_exists = True
                    break
            
            if not already_exists:
                gaps.append({
                    "title": title,
                    "source": topic.get("source", "Unknown"),
                    "category": topic.get("category", "general"),
                    "relevance": "high" if any(kw in title_lower for kw in existing_topics) else "medium",
                    "url": topic.get("url", ""),
                })
        
        return gaps


class ContentAnalyzer:
    """Analyze blog content for insights."""
    
    def analyze_writing_style(self, posts: List[Dict]) -> Dict:
        """Analyze writing style of existing posts."""
        if not posts:
            return {"avg_length": 0, "common_words": [], "tone": "unknown"}
        
        lengths = []
        all_words = []
        
        for post in posts:
            content = post.get("content", "")
            # Strip HTML
            content = re.sub(r'<[^>]+>', '', content)
            words = content.split()
            lengths.append(len(words))
            all_words.extend([w.lower() for w in words if len(w) > 3])
        
        word_freq = Counter(all_words).most_common(20)
        
        return {
            "avg_length": sum(lengths) // len(lengths) if lengths else 0,
            "total_posts": len(posts),
            "common_words": [w for w, c in word_freq[:10]],
            "tone": "technical" if any(w in [w for w, _ in word_freq[:5]] for w in ["install", "setup", "config", "run"]) else "general",
        }
    
    def suggest_topics(self, posts: List[Dict], trending: List[Dict]) -> List[Dict]:
        """Suggest topics based on blog analysis + trending."""
        analyzer = ContentAnalyzer()
        style = analyzer.analyze_writing_style(posts)
        
        # Get existing topics
        existing_topics = set()
        for post in posts:
            words = re.findall(r'\b\w+\b', post.get("title", "").lower())
            existing_topics.update(words)
        
        suggestions = []
        
        # 1. Content gaps (trending but not written)
        blogger = BloggerClient()
        gaps = blogger.get_content_gaps(posts, trending)
        for gap in gaps[:5]:
            suggestions.append({
                "title": gap["title"],
                "type": "content_gap",
                "reason": "Trending topic not yet covered",
                "priority": "high",
                "category": gap["category"],
            })
        
        # 2. Expand existing popular topics
        popular_words = style.get("common_words", [])[:5]
        for word in popular_words:
            if len(word) > 4:  # Only meaningful words
                suggestions.append({
                    "title": f"Advanced {word} Guide",
                    "type": "expand",
                    "reason": f"Expand on popular topic: {word}",
                    "priority": "medium",
                    "category": "tutorial",
                })
        
        # 3. Related topics based on existing content
        for post in posts[:3]:
            title = post.get("title", "")
            if "cara" in title.lower() or "tutorial" in title.lower():
                suggestions.append({
                    "title": f"{title} — Tips & Tricks",
                    "type": "related",
                    "reason": "Companion article to existing popular post",
                    "priority": "medium",
                    "category": "tutorial",
                })
        
        return suggestions[:10]
