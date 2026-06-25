"""
ContentPilot — Web Dashboard

User-friendly web interface untuk ContentPilot.

Usage:
    python3 app.py

Then open: http://localhost:8080
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import json
import os
import sys
from pathlib import Path

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# ============================================================
# CONFIGURATION
# ============================================================

WORKSPACE = Path("workspace")
LICENSE_FILE = WORKSPACE / ".license"
CONFIG_FILE = Path("workspace/config.yaml")

# ============================================================
# ROUTES
# ============================================================

@app.route('/')
def index():
    """Main dashboard."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    license_data = load_license()
    
    # Get pipeline status
    status = get_pipeline_status()
    
    return render_template('dashboard.html', 
                         license=license_data,
                         status=status)

@app.route('/activate', methods=['GET', 'POST'])
@app.route('/activate/<key>')
def activate(key=None):
    """License activation page."""
    # Direct activation via URL
    if key:
        result = validate_license_key(key)
        if result.get('valid'):
            save_license(key, result.get('tier', 'free'))
            session['logged_in'] = True
            session['license_key'] = key
            session['license_tier'] = result.get('tier', 'free')
            return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        key = request.form.get('key', '').strip()
        
        if not key:
            return render_template('activate.html', error="Please enter a license key")
        
        # Validate key
        result = validate_license_key(key)
        
        if result.get('valid'):
            # Save license
            save_license(key, result.get('tier', 'free'))
            # Set session
            session['logged_in'] = True
            session['license_key'] = key
            session['license_tier'] = result.get('tier', 'free')
            return redirect(url_for('dashboard'))
        else:
            return render_template('activate.html', error=result.get('error', 'Invalid key'))
    
    return render_template('activate.html')

@app.route('/dashboard')
def dashboard():
    """Dashboard page."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    license_data = load_license()
    
    status = get_pipeline_status()
    articles_list = get_articles()
    
    # Build stats from status
    stats = {
        'ideas': status.get('stages', {}).get('idea', 0),
        'in_progress': status.get('wip', 0),
        'published': status.get('stages', {}).get('published', 0),
        'avg_seo': 0,
    }
    
    # Build pipeline from status
    pipeline = {
        'researching': status.get('stages', {}).get('researching', 0),
        'drafted': status.get('stages', {}).get('drafted', 0),
        'gated': status.get('stages', {}).get('gated', 0),
        'reviewing': status.get('stages', {}).get('reviewing', 0),
        'published': status.get('stages', {}).get('published', 0),
    }
    
    return render_template('dashboard.html', license=license_data, stats=stats, pipeline=pipeline, articles=articles_list)

@app.route('/articles')
def articles():
    """Articles management page."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    license_data = load_license()
    
    articles_list = get_articles()
    return render_template('articles.html', license=license_data, articles=articles_list)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    """Settings page."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    license_data = load_license()
    
    if request.method == 'POST':
        # Save settings
        save_settings(request.form)
        return redirect(url_for('settings'))
    
    config = load_config()
    return render_template('settings.html', license=license_data, config=config)

@app.route('/research', methods=['GET', 'POST'])
def research():
    """Start research for a topic."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    # Get topic from GET or POST
    topic = request.args.get('topic', '') or request.form.get('topic', '')
    topic = topic.strip()
    
    if not topic:
        return jsonify({"error": "Please enter a topic"}), 400
    
    # Run research (simplified)
    idea_id = slugify(topic)
    
    # Add to idea bank
    idea_bank = WORKSPACE / 'idea-bank.md'
    with open(idea_bank, 'a') as f:
        entry = f"\n### [H] {topic}\n- idea_id: {idea_id}\n- category: general\n- source: smart-suggestion\n- status: idea\n"
        f.write(entry)
    
    return jsonify({
        "success": True,
        "idea_id": idea_id,
        "message": f"Research started for: {topic}"
    })


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page."""
    # Check if already logged in
    if session.get('logged_in'):
        return redirect(url_for('dashboard'))
    
    # Check if license exists — show login form (not auto-login)
    license_data = load_license()
    if license_data and license_data.get('key'):
        # User has license but not logged in — show login form
        pass
    
    if request.method == 'POST':
        key = request.form.get('key', '').strip()
        
        if not key:
            return render_template('login.html', error="Please enter a license key")
        
        # Validate key
        result = validate_license_key(key)
        
        if result.get('valid'):
            # Save license
            save_license(key, result.get('tier', 'free'))
            # Set session
            session['logged_in'] = True
            session['license_key'] = key
            session['license_tier'] = result.get('tier', 'free')
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error=result.get('error', 'Invalid key'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout."""
    session.clear()
    return redirect(url_for('login'))


@app.route('/api/topics', methods=['POST'])
def api_add_topic():
    """Add a new topic to idea bank."""
    if not session.get('logged_in'):
        return jsonify({'success': False, 'error': 'Not logged in'}), 401
    
    title = request.form.get('title', '').strip()
    category = request.form.get('category', 'general')
    
    if not title:
        return jsonify({'success': False, 'error': 'Title required'}), 400
    
    # Add to idea bank
    idea_bank = WORKSPACE / 'idea-bank.md'
    with open(idea_bank, 'a') as f:
        entry = f"\n### [M] {title}\n- category: {category}\n- status: idea\n"
        f.write(entry)
    
    return jsonify({'success': True, 'title': title, 'category': category})
    return jsonify({'success': True, 'title': title, 'category': category})



import urllib.request
import json

def fetch_trending_topics():
    """Fetch smart topic suggestions based on user's blog."""
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
    
    from contentpilot.blogger import BloggerClient, ContentAnalyzer
    
    # Get blog config
    config = load_config()
    blog_id = config.get("blog_id", "")
    domain = config.get("domain", "")
    
    if not blog_id:
        # No blog connected — return curated topics
        return [
            {"title": "Cara Install Docker di Ubuntu 24.04", "source": "Curated", "category": "devops", "type": "curated"},
            {"title": "Tutorial Kubernetes untuk Pemula", "source": "Curated", "category": "devops", "type": "curated"},
            {"title": "React vs Vue vs Angular 2024", "source": "Curated", "category": "webdev", "type": "curated"},
            {"title": "Python AI Automation Tools", "source": "Curated", "category": "ai", "type": "curated"},
            {"title": "Linux Security Best Practices", "source": "Curated", "category": "security", "type": "curated"},
        ]
    
    # Fetch existing posts from blog
    blogger = BloggerClient(blog_id=blog_id, domain=domain)
    posts = blogger.fetch_posts(max_results=20)
    
    # Get trending topics
    trending = _fetch_raw_trending()
    
    # Generate smart suggestions
    analyzer = ContentAnalyzer()
    suggestions = analyzer.suggest_topics(posts, trending)
    
    # Convert to template format
    topics = []
    for s in suggestions:
        topics.append({
            "title": s["title"],
            "source": s["type"].replace("_", " ").title(),
            "category": s["category"],
            "type": s["type"],
            "reason": s["reason"],
            "priority": s["priority"],
        })
    
    return topics[:15]


def _fetch_raw_trending():
    """Fetch raw trending data from HackerNews."""
    topics = []
    try:
        url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        req = urllib.request.Request(url, headers={"User-Agent": "ContentPilot/1.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            story_ids = json.loads(resp.read())[:15]
            
            for story_id in story_ids:
                story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
                story_req = urllib.request.Request(story_url, headers={"User-Agent": "ContentPilot/1.0"})
                with urllib.request.urlopen(story_req, timeout=3) as story_resp:
                    story = json.loads(story_resp.read())
                    if story.get("title"):
                        title_lower = story["title"].lower()
                        if any(kw in title_lower for kw in ["ai", "gpt", "llm", "machine learning", "openai"]):
                            category = "ai"
                        elif any(kw in title_lower for kw in ["docker", "kubernetes", "linux", "server", "cloud", "devops"]):
                            category = "devops"
                        elif any(kw in title_lower for kw in ["react", "vue", "angular", "javascript", "web", "node"]):
                            category = "webdev"
                        elif any(kw in title_lower for kw in ["hack", "security", "cyber", "vulnerability"]):
                            category = "security"
                        else:
                            category = "general"
                        
                        topics.append({
                            "title": story["title"],
                            "source": "HackerNews",
                            "category": category,
                        })
    except Exception:
        pass
    
    # Curated fallback
    if len(topics) < 5:
        topics.extend([
            {"title": "Docker Best Practices", "source": "Curated", "category": "devops"},
            {"title": "Python Automation Scripts", "source": "Curated", "category": "ai"},
            {"title": "React Hooks Guide", "source": "Curated", "category": "webdev"},
        ])
    
    return topics


@app.route('/api/status')
def api_status():
    """API endpoint for status."""
    status = get_pipeline_status()
    return jsonify(status)

@app.route('/api/articles')
def api_articles():
    """API endpoint for articles."""
    articles_list = get_articles()
    return jsonify(articles_list)

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def load_license() -> dict:
    """Load license data."""
    if LICENSE_FILE.exists():
        with open(LICENSE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_license(key: str, tier: str):
    """Save license data."""
    WORKSPACE.mkdir(exist_ok=True)
    license_data = {
        "key": key,
        "tier": tier,
        "activated_at": __import__('datetime').datetime.now().isoformat()
    }
    with open(LICENSE_FILE, 'w') as f:
        json.dump(license_data, f, indent=2)

def validate_license_key(key: str) -> dict:
    """Validate license key (simplified)."""
    # Accept CP- keys (ContentPilot) or SB- keys (legacy)
    if key.startswith("CP-") or key.startswith("SB-"):
        return {"valid": True, "tier": "pro"}
    return {"valid": False, "error": "Invalid license key format"}

def get_pipeline_status() -> dict:
    """Get pipeline status."""
    journal = WORKSPACE / "journal.jsonl"
    
    if not journal.exists():
        return {"total": 0, "stages": {}, "wip": 0}
    
    articles = []
    with open(journal, 'r') as f:
        for line in f:
            if line.strip():
                articles.append(json.loads(line))
    
    stages = {}
    for a in articles:
        stage = a.get("stage", "unknown")
        stages[stage] = stages.get(stage, 0) + 1
    
    return {
        "total": len(articles),
        "stages": stages,
        "wip": sum(1 for a in articles if a.get("stage") in ["researching", "drafting", "reviewing"])
    }

def get_articles() -> list:
    """Get list of articles."""
    journal = WORKSPACE / "journal.jsonl"
    
    if not journal.exists():
        return []
    
    articles = []
    with open(journal, 'r') as f:
        for line in f:
            if line.strip():
                articles.append(json.loads(line))
    
    return articles

def load_config() -> dict:
    """Load configuration."""
    if CONFIG_FILE.exists():
        import yaml
        with open(CONFIG_FILE, 'r') as f:
            return yaml.safe_load(f)
    return {}

def save_settings(form: dict):
    """Save settings from form."""
    import yaml
    
    config = {
        "domain": form.get("domain", ""),
        "blog_id": form.get("blog_id", ""),
        "ai": {
            "provider": form.get("ai_provider", "openai"),
            "model": form.get("ai_model", "gpt-4"),
            "api_key": form.get("ai_api_key", "")
        },
        "pipeline": {
            "wip_limit": int(form.get("wip_limit", 3)),
            "publish_mode": form.get("publish_mode", "draft")
        }
    }
    
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)

def slugify(text: str) -> str:
    """Convert text to slug."""
    import re
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text

# ============================================================
# MAIN
# ============================================================

if __name__ == '__main__':
    print("=" * 60)
    print("  ContentPilot — Web Dashboard")
    print("=" * 60)
    print()
    print("  Open: http://localhost:8080")
    print()
    
    app.run(debug=True, host='0.0.0.0', port=8080)

@app.route('/connect-blogger')
def connect_blogger():
    """Connect Blogger page."""
    connected = session.get('blogger_connected', False)
    license_data = load_license()
    return render_template('connect_blogger.html', license=license_data, 
                         connected=connected,
                         blog_name=session.get('blog_name', ''),
                         blog_id=session.get('blog_id', ''))

@app.route('/trending')
def trending():
    """Trending topics page."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    license_data = load_license()
    topics = fetch_trending_topics()
    
    # Get blog analysis
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
    from contentpilot.blogger import BloggerClient, ContentAnalyzer
    
    config = load_config()
    blog_id = config.get("blog_id", "")
    blog_analysis = {"connected": bool(blog_id), "post_count": 0, "categories": {}}
    
    if blog_id:
        blogger = BloggerClient(blog_id=blog_id, domain=config.get("domain", ""))
        posts = blogger.fetch_posts(max_results=20)
        analyzer = ContentAnalyzer()
        blog_analysis = {
            "connected": True,
            "post_count": len(posts),
            "categories": analyzer.extract_categories(posts),
            "style": analyzer.analyze_writing_style(posts),
        }
    
    return render_template('trending.html', license=license_data, topics=topics, blog_analysis=blog_analysis)

@app.route('/publish/<idea_id>')
def publish_page(idea_id):
    """Publish article page."""
    # Load article data
    license_data = load_license()
    return render_template('publish.html', license=license_data,
                         article={'id': idea_id, 'title': 'Sample', 'slug': 'sample', 'word_count': 1000, 'seo_score': 85, 'excerpt': 'Preview...'},
                         blog_name=session.get('blog_name', 'My Blog'),
                         blog_id=session.get('blog_id', ''))

@app.route('/api/trending')
def api_trending():
    """Get trending topics."""
    topics = fetch_trending_topics()
    return jsonify({"topics": topics})

@app.route('/api/gaps')
def api_gaps():
    """Get content gaps."""
    return jsonify({"gaps": [
        {"title": "Advanced Docker Compose Techniques", "opportunity": "High search, low competition"},
        {"title": "Linux Security Best Practices", "opportunity": "Growing demand"}
    ]})

@app.route('/api/blogs')
def api_blogs():
    """Get user's blogs."""
    blogs = session.get('blogs', [])
    return jsonify({"blogs": blogs})

@app.route('/api/blogs/select', methods=['POST'])
def api_select_blog():
    """Select blog to use."""
    data = request.get_json()
    session['blog_id'] = data.get('blog_id')
    return jsonify({"success": True})

@app.route('/api/blogs/disconnect', methods=['POST'])
def api_disconnect_blog():
    """Disconnect Blogger."""
    session.pop('blogger_connected', None)
    session.pop('blog_id', None)
    session.pop('blogs', None)
    return jsonify({"success": True})

@app.route('/api/publish', methods=['POST'])
def api_publish():
    """Publish article."""
    data = request.get_json()
    idea_id = data.get('idea_id')
    mode = data.get('mode', 'draft')
    
    # In production, call Blogger API
    return jsonify({
        "success": True,
        "url": f"https://blog.example.com/{idea_id}",
        "mode": mode
    })
