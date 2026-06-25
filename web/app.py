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
CONFIG_FILE = Path("config/config.yaml")

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
            return redirect(url_for('index'))
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

@app.route('/research', methods=['POST'])
def research():
    """Start research for a topic."""
    topic = request.form.get('topic', '').strip()
    if not topic:
        return jsonify({"error": "Please enter a topic"}), 400
    
    # Run research (simplified)
    idea_id = slugify(topic)
    
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
    return render_template('trending.html', license=license_data)

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
    return jsonify({"topics": [
        {"title": "Cara Install Docker di Ubuntu 24.04", "source": "Google Trends", "region": "Indonesia"},
        {"title": "Tutorial Kubernetes untuk Pemula", "source": "HackerNews", "region": "Global"},
        {"title": "React vs Vue vs Angular 2024", "source": "Google Trends", "region": "Global"}
    ]})

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
