"""
ContentPilot — Web Dashboard

User-friendly web interface untuk ContentPilot.
Connects to ContentPilot Server for intelligence features.

Usage:
    python3 app.py

Then open: http://localhost:8080
"""
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_wtf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import json
import os
import sys
from pathlib import Path

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Security: CSRF Protection
csrf = CSRFProtect(app)

# Security: Rate Limiting
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per hour"],
    storage_uri="memory://"
)

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# ============================================================
# CONFIGURATION
# ============================================================

WORKSPACE = Path("workspace")
LICENSE_FILE = WORKSPACE / ".license"
CONFIG_FILE = Path("workspace/config.yaml")
CACHE_DIR = WORKSPACE / "cache"

# Server URL (ContentPilot Server)
SERVER_URL = os.getenv("CONTENTPILOT_SERVER", "http://localhost:5001")

# ============================================================
# SERVER SYNC HELPER
# ============================================================

def load_license() -> dict:
    """Load license data."""
    if LICENSE_FILE.exists():
        with open(LICENSE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_license(key: str, tier: str):
    """Save license data."""
    WORKSPACE.mkdir(parents=True, exist_ok=True)
    license_data = {
        "key": key,
        "tier": tier,
        "activated_at": __import__('datetime').datetime.now().isoformat()
    }
    with open(LICENSE_FILE, 'w') as f:
        json.dump(license_data, f, indent=2)

def get_sync_client():
    """Get sync client for server communication."""
    license_data = load_license()
    if not license_data or not license_data.get("key"):
        return None
    
    from contentpilot.sync.client import SyncClient
    return SyncClient(SERVER_URL, license_data["key"])


def get_cache():
    """Get local cache instance."""
    from contentpilot.sync.cache import SyncCache
    return SyncCache(str(CACHE_DIR))


def server_request(method, path, data=None):
    """Make request to ContentPilot Server (non-blocking)."""
    import urllib.request
    import urllib.error
    
    url = f"{SERVER_URL}{path}"
    headers = {"Content-Type": "application/json"}
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req, timeout=2) as resp:
            return json.loads(resp.read().decode())
    except Exception:
        return None


def proxy_to_server(path, json_body=None, method="POST", timeout=60):
    """Forward a request to ContentPilot Server, returning (data, status_code).

    Unlike server_request(), this surfaces HTTP error bodies/status so the
    frontend can show real errors instead of a silent None.
    """
    import urllib.request
    import urllib.error

    url = f"{SERVER_URL}{path}"
    headers = {"Content-Type": "application/json"}
    body = json.dumps(json_body).encode() if json_body is not None else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode()), resp.status
    except urllib.error.HTTPError as e:
        try:
            return json.loads(e.read().decode()), e.code
        except Exception:
            return {"success": False, "error": f"Server error {e.code}"}, e.code
    except Exception as e:
        return {"success": False, "error": f"Server not available: {e}"}, 503


def startup_sync():
    """Fetch rules, suggestions, trends from server on startup."""
    cache = get_cache()
    
    # Only sync if we have a license
    license_data = load_license()
    if not license_data or not license_data.get("key"):
        return
    
    # Fetch rules (daily)
    if not cache.is_fresh("rules"):
        rules = server_request("GET", "/api/rules")
        if rules and not rules.get("error"):
            cache.set_rules(rules)
    
    # Fetch suggestions (every 6h)
    if not cache.is_fresh("suggestions"):
        suggestions = server_request("GET", f"/api/suggest?key={license_data['key']}")
        if suggestions and not suggestions.get("error"):
            cache.set_suggestions(suggestions)
    
    # Fetch trending (every 1h)
    if not cache.is_fresh("trending"):
        trending = server_request("GET", "/api/trends")
        if trending and not trending.get("error"):
            cache.set_trending(trending)


    app.run(debug=os.getenv("FLASK_DEBUG", "false").lower() == "true", host='0.0.0.0', port=8080)

# ============================================================
# ROUTES — EXISTING
# ============================================================

@app.route('/')
def index():
    """Main dashboard."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

@app.route('/activate', methods=['GET', 'POST'])
@app.route('/activate/<key>')
def activate(key=None):
    """License activation page."""
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
        result = validate_license_key(key)
        if result.get('valid'):
            save_license(key, result.get('tier', 'free'))
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
    
    stats = {
        'ideas': status.get('stages', {}).get('idea', 0),
        'in_progress': status.get('wip', 0),
        'published': status.get('stages', {}).get('published', 0),
        'avg_seo': 0,
    }
    
    pipeline = {
        'researching': status.get('stages', {}).get('researching', 0),
        'drafted': status.get('stages', {}).get('drafted', 0),
        'gated': status.get('stages', {}).get('gated', 0),
        'reviewing': status.get('stages', {}).get('reviewing', 0),
        'published': status.get('stages', {}).get('published', 0),
    }
    
    # Get server suggestions (with cache fallback)
    suggestions = []
    cache = get_cache()
    cached = cache.get_suggestions()
    if cached and not cached.get("error"):
        suggestions = cached.get("suggestions", [])
    
    # Check server connection (cached, non-blocking)
    server_connected = False
    cached_health = cache.get("server_health")
    if cached_health and not cached_health.get("error"):
        server_connected = True
    else:
        # Only check server if no cache (reduces blocking)
        health = server_request("GET", "/api/status")
        if health and health.get("status") == "ok":
            server_connected = True
            cache.set("server_health", health, ttl_hours=1)
    
    return render_template('dashboard.html', 
                         license=license_data, 
                         stats=stats, 
                         pipeline=pipeline, 
                         articles=articles_list,
                         suggestions=suggestions,
                         server_connected=server_connected)

@app.route('/articles')
def articles():
    """Articles management page."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    license_data = load_license()
    articles_list = get_articles()
    
    # Get usage data for article limit display
    usage = {}
    if license_data and license_data.get("key"):
        try:
            result = server_request("GET", f"/api/usage/articles?key={license_data['key']}")
            if result and not result.get("error"):
                usage = result
        except:
            pass
    
    return render_template('articles.html', license=license_data, articles=articles_list, usage=usage)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    """Settings page."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    license_data = load_license()
    
    if request.method == 'POST':
        save_settings(request.form)
        return redirect(url_for('settings'))
    
    config = load_config()
    
    # Get schedule from server (with cache fallback)
    schedule = {}
    cache = get_cache()
    cached = cache.get_schedule()
    if cached and isinstance(cached, dict) and not cached.get("error"):
        schedule = cached
    
    return render_template('settings.html', license=license_data, config=config, schedule=schedule)

@app.route('/settings/save-schedule', methods=['POST'])
def save_schedule():
    """Save schedule settings."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    # Save to cache locally
    cache = get_cache()
    schedule = {
        "suggestion_interval_hours": int(request.form.get('suggestion_interval_hours', 6)),
        "analysis_interval_hours": int(request.form.get('analysis_interval_hours', 24)),
        "trending_interval_hours": int(request.form.get('trending_interval_hours', 2)),
        "auto_suggest": request.form.get('auto_suggest') == 'true',
    }
    cache.set_schedule(schedule)
    
    return redirect(url_for('settings'))

@app.route('/research', methods=['GET', 'POST'])
def research():
    """Start research for a topic."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    topic = request.args.get('topic', '') or request.form.get('topic', '')
    topic = topic.strip()
    
    if not topic:
        return jsonify({"error": "Please enter a topic"}), 400
    
    idea_id = slugify(topic)
    
    idea_bank = WORKSPACE / 'idea-bank.md'
    with open(idea_bank, 'a') as f:
        entry = f"\n### [H] {topic}\n- idea_id: {idea_id}\n- category: general\n- source: smart-suggestion\n- status: idea\n"
        f.write(entry)
    
    return redirect(url_for('articles'))

@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def login():
    """Login page."""
    if session.get('logged_in'):
        return redirect(url_for('dashboard'))
    
    license_data = load_license()
    if license_data and license_data.get('key'):
        pass
    
    if request.method == 'POST':
        key = request.form.get('key', '').strip()
        if not key:
            return render_template('login.html', error="Please enter a license key")
        result = validate_license_key(key)
        if result.get('valid'):
            save_license(key, result.get('tier', 'free'))
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

# ============================================================
# ROUTES — NEW (Server Sync)
# ============================================================

@app.route('/api/suggestions')
def api_suggestions():
    """Get suggestions from server (with cache fallback)."""
    if not session.get('logged_in'):
        return jsonify({"error": "Not logged in"}), 401
    
    cache = get_cache()
    
    # Try server first
    client = get_sync_client()
    if client:
        result = client.get_suggestions()
        if not result.get("error"):
            cache.set_suggestions(result)
            return jsonify(result)
    
    # Fallback to cache
    cached = cache.get_suggestions()
    if cached:
        return jsonify(cached)
    
    return jsonify({"suggestions": [], "source": "empty"})

@app.route('/api/trending')
def api_trending():
    """Get trending from server (with cache fallback)."""
    category = request.args.get('category')
    
    cache = get_cache()
    
    # Try server first
    client = get_sync_client()
    if client:
        result = client.get_trending(category)
        if not result.get("error"):
            cache.set_trending(result)
            return jsonify(result)
    
    # Fallback to cache
    cached = cache.get_trending()
    if cached:
        return jsonify(cached)
    
    return jsonify({"trends": [], "source": "empty"})

@app.route('/api/rules')
def api_rules():
    """Get rules from server (with cache fallback)."""
    cache = get_cache()
    
    # Try server first
    client = get_sync_client()
    if client:
        result = client.get_rules()
        if not result.get("error"):
            cache.set_rules(result)
            return jsonify(result)
    
    # Fallback to cache
    cached = cache.get_rules()
    if cached:
        return jsonify(cached)
    
    return jsonify({"rules": {}, "source": "empty"})

@app.route('/api/schedule', methods=['GET'])
def api_schedule():
    """Get user's schedule from server."""
    if not session.get('logged_in'):
        return jsonify({"error": "Not logged in"}), 401
    
    client = get_sync_client()
    if client:
        result = client.get_schedule()
        return jsonify(result)
    
    return jsonify({"error": "Server not available"}), 503

@app.route('/api/schedule', methods=['PUT'])
def api_update_schedule():
    """Update user's schedule on server."""
    if not session.get('logged_in'):
        return jsonify({"error": "Not logged in"}), 401
    
    data = request.get_json()
    client = get_sync_client()
    if client:
        result = client.update_schedule(data)
        return jsonify(result)
    
    return jsonify({"error": "Server not available"}), 503

@app.route('/api/queue/status')
def api_queue_status():
    """Get queue status from server."""
    if not session.get('logged_in'):
        return jsonify({"error": "Not logged in"}), 401
    
    client = get_sync_client()
    if client:
        result = client.get_queue_status()
        return jsonify(result)
    
    return jsonify({"error": "Server not available"}), 503

@app.route('/api/trigger', methods=['POST'])
@csrf.exempt
def api_trigger():
    """Trigger a job on server."""
    if not session.get('logged_in'):
        return jsonify({"error": "Not logged in"}), 401

    data = request.get_json()
    job_type = data.get('job_type')
    metadata = data.get('metadata', {})

    client = get_sync_client()
    if client:
        result = client.trigger_job(job_type, metadata)
        return jsonify(result)

    return jsonify({"error": "Server not available"}), 503


# ------------------------------------------------------------
# Proxy routes — forward JSON to ContentPilot Server (:5001).
# The frontend fetch()es these on the client origin; without
# them the Pipeline/Indexing pages 404. CSRF-exempt because they
# are JSON APIs called by our own JS (session-gated), not forms.
# ------------------------------------------------------------

@app.route('/api/pipeline/run', methods=['POST'])
@csrf.exempt
def api_pipeline_run():
    """Run full pipeline (proxied to server)."""
    if not session.get('logged_in'):
        return jsonify({"error": "Not logged in"}), 401
    data = request.get_json(silent=True) or {}
    result, status = proxy_to_server('/api/pipeline/run', data)
    return jsonify(result), status


@app.route('/api/indexing/check', methods=['POST'])
@csrf.exempt
def api_indexing_check():
    """Check indexing status (proxied to server)."""
    if not session.get('logged_in'):
        return jsonify({"error": "Not logged in"}), 401
    data = request.get_json(silent=True) or {}
    result, status = proxy_to_server('/api/indexing/check', data)
    return jsonify(result), status


@app.route('/api/indexing/submit', methods=['POST'])
@csrf.exempt
def api_indexing_submit():
    """Submit URL for indexing (proxied to server)."""
    if not session.get('logged_in'):
        return jsonify({"error": "Not logged in"}), 401
    data = request.get_json(silent=True) or {}
    result, status = proxy_to_server('/api/indexing/submit', data)
    return jsonify(result), status


@app.route('/api/indexing/coverage', methods=['POST'])
@csrf.exempt
def api_indexing_coverage():
    """Get indexing coverage report (proxied to server)."""
    if not session.get('logged_in'):
        return jsonify({"error": "Not logged in"}), 401
    data = request.get_json(silent=True) or {}
    result, status = proxy_to_server('/api/indexing/coverage', data)
    return jsonify(result), status

@app.route('/api/pipeline/status/<task_id>')
def api_pipeline_status(task_id):
    """Get pipeline task status from server."""
    if not session.get('logged_in'):
        return jsonify({"error": "Not logged in"}), 401
    
    client = get_sync_client()
    if client:
        result = client.get_task_status(task_id)
        return jsonify(result)
    
    return jsonify({"error": "Server not available"}), 503

@app.route('/api/server/status')
def api_server_status():
    """Check server connection status."""
    health = server_request("GET", "/api/status")
    if health and health.get("status") == "ok":
        return jsonify({"connected": True, "version": health.get("version")})
    return jsonify({"connected": False})

# ============================================================
# ROUTES — EXISTING (unchanged)
# ============================================================

@app.route('/connect-blogger')
def connect_blogger():
    """Connect Blogger page."""
    connected = session.get('blogger_connected', False)
    license_data = load_license()
    return render_template('connect_blogger.html', license=license_data, 
                         connected=connected,
                         blog_name=session.get('blog_name', ''),
                         blog_id=session.get('blog_id', ''))

@app.route('/monitor')
def monitor():
    """Monitor page — real-time pipeline progress."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    license_data = load_license()
    return render_template('monitor.html', license=license_data)

@app.route('/trending')
def trending():
    """Trending topics page."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    license_data = load_license()
    topics = fetch_trending_topics()
    
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
    """Publish page for an article."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    license_data = load_license()
    return render_template('publish.html', license=license_data, idea_id=idea_id)

@app.route('/pipeline')
def pipeline():
    """Pipeline page."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    license_data = load_license()
    blogs = get_user_blogs()
    pipelines = get_user_pipelines()
    return render_template('pipeline.html', license=license_data, blogs=blogs, pipelines=pipelines)

@app.route('/voice-guide')
def voice_guide():
    """Voice Guide page."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    license_data = load_license()
    blogs = get_user_blogs()
    return render_template('voice-guide.html', license=license_data, blogs=blogs)

@app.route('/indexing')
def indexing():
    """Indexing page."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    license_data = load_license()
    articles = get_published_articles()
    return render_template('indexing.html', license=license_data, articles=articles)

def get_user_blogs():
    """Get user's blogs from database."""
    try:
        import psycopg2
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5432'),
            database=os.getenv('DB_NAME', 'contentpilot'),
            user=os.getenv('DB_USER', 'contentpilot'),
            password=os.getenv('DB_PASSWORD', '')
        )
        cur = conn.cursor()
        cur.execute('SELECT id, domain, platform FROM blogs LIMIT 10')
        blogs = [{'id': row[0], 'domain': row[1], 'platform': row[2]} for row in cur.fetchall()]
        cur.close()
        conn.close()
        return blogs
    except:
        return []

def get_user_pipelines():
    """Get user's pipeline runs."""
    try:
        import psycopg2
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5432'),
            database=os.getenv('DB_NAME', 'contentpilot'),
            user=os.getenv('DB_USER', 'contentpilot'),
            password=os.getenv('DB_PASSWORD', '')
        )
        cur = conn.cursor()
        cur.execute('SELECT topic, status, created_at FROM pipeline_runs ORDER BY created_at DESC LIMIT 10')
        pipelines = [{'topic': row[0], 'status': row[1], 'created_at': str(row[2])} for row in cur.fetchall()]
        cur.close()
        conn.close()
        return pipelines
    except:
        return []

def get_published_articles():
    """Get published articles for indexing."""
    try:
        import psycopg2
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5432'),
            database=os.getenv('DB_NAME', 'contentpilot'),
            user=os.getenv('DB_USER', 'contentpilot'),
            password=os.getenv('DB_PASSWORD', '')
        )
        cur = conn.cursor()
        cur.execute('SELECT title, published_url, indexing_status FROM articles WHERE status = %s ORDER BY created_at DESC LIMIT 10', ('published',))
        articles = [{'title': row[0], 'published_url': row[1], 'indexing_status': row[2]} for row in cur.fetchall()]
        cur.close()
        conn.close()
        return articles
    except:
        return []

# ============================================================
# API ROUTES — EXISTING
# ============================================================

@app.route('/api/topics', methods=['POST'])
def api_add_topic():
    """Add a new topic to idea bank."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    title = request.form.get('title', '').strip()
    category = request.form.get('category', 'general')
    
    if not title:
        return redirect(url_for('articles'))
    
    idea_bank = WORKSPACE / 'idea-bank.md'
    with open(idea_bank, 'a') as f:
        entry = f"\n### [M] {title}\n- category: {category}\n- status: idea\n"
        f.write(entry)
    
    return redirect(url_for('articles'))

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


def validate_license_key(key: str) -> dict:
    """Validate license key (secure)."""
    import re
    
    # Basic format validation
    if not key or not isinstance(key, str):
        return {"valid": False, "error": "Invalid key"}
    
    key = key.strip()
    
    # Length check
    if len(key) < 10 or len(key) > 100:
        return {"valid": False, "error": "Invalid key length"}
    
    # Format check: CP-XXXX-XXXX or SB-XXXX-XXXX (alphanumeric only)
    if not re.match(r'^(CP|SB)-[A-Z0-9]{4,}-[A-Z0-9]{4,}$', key):
        return {"valid": False, "error": "Invalid key format"}
    
    # Check if key exists in local license file
    if LICENSE_FILE.exists():
        try:
            with open(LICENSE_FILE, 'r') as f:
                stored_data = json.load(f)
                stored_key = stored_data.get("key", "")
                if stored_key == key:
                    tier = "pro" if key.startswith("CP-") else "starter"
                    return {"valid": True, "tier": tier}
        except:
            pass
    
    # Check server API
    try:
        result = server_request("POST", "/api/validate", {"key": key})
        if result and result.get("valid"):
            return {"valid": True, "tier": result.get("tier", "free")}
    except:
        pass
    
    return {"valid": False, "error": "Invalid license key"}

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
    """Merge submitted settings into the existing config.

    Settings are split across several small forms that each POST to /settings,
    so we update only the fields present in this submission. Rebuilding the whole
    config from one form would wipe the other forms' values.
    """
    import yaml

    config = load_config() or {}
    config.setdefault("ai", {})
    config.setdefault("pipeline", {})

    if "domain" in form:
        config["domain"] = form.get("domain", "")
    if "blog_id" in form:
        config["blog_id"] = form.get("blog_id", "")
    # Publishing autonomy — single source of truth (also decides draft vs live).
    if "approval_mode" in form:
        config["approval_mode"] = form.get("approval_mode", "soft")
    if "wip_limit" in form:
        config["pipeline"]["wip_limit"] = int(form.get("wip_limit", 3))

    ai_submitted = "ai_provider" in form
    if ai_submitted:
        config["ai"] = {
            "provider": form.get("ai_provider", "openai"),
            "model": form.get("ai_model", "gpt-4"),
            "api_key": form.get("ai_api_key", ""),
        }

    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)

    # Sync AI settings to server only when the AI form was the one submitted
    # (avoids re-sending a stale/blank key on every unrelated save).
    if ai_submitted:
        license_data = load_license()
        ai_config = config.get("ai", {})
        if license_data and license_data.get("key") and ai_config.get("api_key"):
            server_request("POST", "/api/settings/ai", {
                "key": license_data["key"],
                "provider": ai_config.get("provider"),
                "model": ai_config.get("model"),
                "api_key": ai_config.get("api_key")
            })

def slugify(text: str) -> str:
    """Convert text to slug."""
    import re
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text

def fetch_trending_topics():
    """Fetch smart topic suggestions based on user's blog."""
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
    
    from contentpilot.blogger import BloggerClient, ContentAnalyzer
    
    config = load_config()
    blog_id = config.get("blog_id", "")
    domain = config.get("domain", "")
    
    if not blog_id:
        return [
            {"title": "Cara Install Docker di Ubuntu 24.04", "source": "Curated", "category": "devops", "type": "curated"},
            {"title": "Tutorial Kubernetes untuk Pemula", "source": "Curated", "category": "devops", "type": "curated"},
            {"title": "React vs Vue vs Angular 2024", "source": "Curated", "category": "webdev", "type": "curated"},
            {"title": "Python AI Automation Tools", "source": "Curated", "category": "ai", "type": "curated"},
            {"title": "Linux Security Best Practices", "source": "Curated", "category": "security", "type": "curated"},
        ]
    
    blogger = BloggerClient(blog_id=blog_id, domain=domain)
    posts = blogger.fetch_posts(max_results=20)
    
    trending = _fetch_raw_trending()
    
    analyzer = ContentAnalyzer()
    suggestions = analyzer.suggest_topics(posts, trending)
    
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
        import urllib.request
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
    
    if len(topics) < 5:
        topics.extend([
            {"title": "Docker Best Practices", "source": "Curated", "category": "devops"},
            {"title": "Python Automation Scripts", "source": "Curated", "category": "ai"},
            {"title": "React Hooks Guide", "source": "Curated", "category": "webdev"},
        ])
    
    return topics

# ============================================================
# MAIN
# ============================================================

if __name__ == '__main__':
    print("=" * 60)
    print("  ContentPilot — Web Dashboard")
    print("=" * 60)
    print()
    print(f"  Open: http://localhost:8080")
    print(f"  Server: {SERVER_URL}")
    print()
    
    app.run(debug=os.getenv("FLASK_DEBUG", "false").lower() == "true", host='0.0.0.0', port=8080)

def validate_input(input_str: str, max_length: int = 100) -> bool:
    """Validate input string."""
    if not input_str or not isinstance(input_str, str):
        return False
    if len(input_str.strip()) > max_length:
        return False
    # Check for potentially dangerous characters
    dangerous_chars = ['<', '>', '"', "'", '&', ';', '|', '`']
    for char in dangerous_chars:
        if char in input_str:
            return False
    return True

def is_valid_url(url: str) -> bool:
    """Validate URL to prevent SSRF."""
    import re
    from urllib.parse import urlparse
    
    try:
        parsed = urlparse(url)
        # Only allow http/https
        if parsed.scheme not in ('http', 'https'):
            return False
        # Block localhost and internal IPs
        hostname = parsed.hostname or ''
        if hostname in ('localhost', '127.0.0.1', '0.0.0.0', '::1'):
            return False
        # Block private IP ranges
        if re.match(r'^(10\.|172\.(1[6-9]|2[0-9]|3[01])\.|192\.168\.)', hostname):
            return False
        return True
    except:
        return False

@app.after_request
def set_security_headers(response):
    """Set security headers."""
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    return response
