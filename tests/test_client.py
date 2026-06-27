"""
ContentPilot Client — Tests

Tests for Flask app and client modules.
"""
import sys
import os
import json
import unittest

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from web.app import app


class TestFlaskApp(unittest.TestCase):
    """Test Flask application."""
    
    def setUp(self):
        """Set up test client."""
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'test-secret'
        # Disable CSRF for form-post tests; real forms send csrf_token() and
        # JSON APIs are @csrf.exempt, so this only affects the test client.
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()
    
    def test_login_page(self):
        """Test login page loads."""
        resp = self.client.get('/login')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Welcome Back', resp.data)
    
    def test_login_with_key(self):
        """Test login with license key."""
        resp = self.client.post('/login', 
            data={'key': 'CP-TEST1234-TEST5678'},
            follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
    
    def test_dashboard_requires_login(self):
        """Test dashboard requires login."""
        resp = self.client.get('/dashboard')
        self.assertEqual(resp.status_code, 302)  # Redirect to login
    
    def test_settings_requires_login(self):
        """Test settings requires login."""
        resp = self.client.get('/settings')
        self.assertEqual(resp.status_code, 302)
    
    def test_articles_requires_login(self):
        """Test articles requires login."""
        resp = self.client.get('/articles')
        self.assertEqual(resp.status_code, 302)
    
    def test_monitor_requires_login(self):
        """Test monitor requires login."""
        resp = self.client.get('/monitor')
        self.assertEqual(resp.status_code, 302)
    
    def test_trending_requires_login(self):
        """Test trending requires login."""
        resp = self.client.get('/trending')
        self.assertEqual(resp.status_code, 302)
    
    def test_api_status(self):
        """Test /api/status endpoint."""
        resp = self.client.get('/api/status')
        self.assertEqual(resp.status_code, 200)
    
    def test_api_server_status(self):
        """Test /api/server/status endpoint."""
        resp = self.client.get('/api/server/status')
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('connected', data)


class TestSyncCache(unittest.TestCase):
    """Test SyncCache module."""
    
    def test_cache_init(self):
        """Test SyncCache can be initialized."""
        import tempfile
        from contentpilot.sync.cache import SyncCache
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = SyncCache(tmpdir)
            self.assertIsNotNone(cache)
    
    def test_cache_set_get(self):
        """Test cache set and get."""
        import tempfile
        from contentpilot.sync.cache import SyncCache
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = SyncCache(tmpdir)
            cache.set("test", {"key": "value"})
            result = cache.get("test")
            self.assertEqual(result, {"key": "value"})
    
    def test_cache_is_fresh(self):
        """Test cache freshness check."""
        import tempfile
        from contentpilot.sync.cache import SyncCache
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = SyncCache(tmpdir)
            cache.set("test", {"key": "value"}, ttl_hours=1)
            self.assertTrue(cache.is_fresh("test"))
            self.assertFalse(cache.is_fresh("nonexistent"))


class TestSyncClient(unittest.TestCase):
    """Test SyncClient module."""
    
    def test_client_init(self):
        """Test SyncClient can be initialized."""
        from contentpilot.sync.client import SyncClient
        client = SyncClient("http://localhost:5001", "CP-TEST")
        self.assertIsNotNone(client)
        self.assertEqual(client.server_url, "http://localhost:5001")
        self.assertEqual(client.license_key, "CP-TEST")
    
    def test_client_methods_exist(self):
        """Test SyncClient has all required methods."""
        from contentpilot.sync.client import SyncClient
        client = SyncClient("http://localhost:5001", "CP-TEST")
        self.assertTrue(hasattr(client, 'get_rules'))
        self.assertTrue(hasattr(client, 'get_suggestions'))
        self.assertTrue(hasattr(client, 'get_trending'))
        self.assertTrue(hasattr(client, 'get_schedule'))
        self.assertTrue(hasattr(client, 'update_schedule'))
        self.assertTrue(hasattr(client, 'trigger_job'))
        self.assertTrue(hasattr(client, 'get_queue_status'))
        self.assertTrue(hasattr(client, 'get_task_status'))


if __name__ == '__main__':
    unittest.main()
