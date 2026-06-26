"""
ContentPilot Sync Client — Talks to ContentPilot Server.

Handles: rules, suggestions, trending, schedule, queue.
"""
import json
import urllib.request
import urllib.error
from typing import Dict, Optional, List
import time


class SyncClient:
    """Client to communicate with ContentPilot Server."""
    
    def __init__(self, server_url: str, license_key: str):
        self.server_url = server_url.rstrip("/")
        self.license_key = license_key
        self.timeout = 10
    
    def _request(self, method: str, path: str, data: dict = None) -> Dict:
        """Make HTTP request to server."""
        url = f"{self.server_url}{path}"
        
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "ContentPilot-Client/1.0",
        }
        
        body = json.dumps(data).encode() if data else None
        
        req = urllib.request.Request(url, data=body, headers=headers, method=method)
        
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            return {"error": f"HTTP {e.code}: {e.reason}"}
        except urllib.error.URLError as e:
            return {"error": f"Connection failed: {e.reason}"}
        except Exception as e:
            return {"error": str(e)}
    
    def _get(self, path: str) -> Dict:
        return self._request("GET", path)
    
    def _post(self, path: str, data: dict = None) -> Dict:
        return self._request("POST", path, data)
    
    def _put(self, path: str, data: dict = None) -> Dict:
        return self._request("PUT", path, data)
    
    # ── Rules ──────────────────────────────────────────────────────
    
    def get_rules(self, rule_type: str = None) -> Dict:
        """Get quality rules from server."""
        path = "/api/rules"
        if rule_type:
            path += f"?type={rule_type}"
        return self._get(path)
    
    # ── Suggestions ────────────────────────────────────────────────
    
    def get_suggestions(self) -> Dict:
        """Get topic suggestions for this user."""
        return self._get(f"/api/suggest?key={self.license_key}")
    
    # ── Trending ───────────────────────────────────────────────────
    
    def get_trending(self, category: str = None) -> Dict:
        """Get trending topics."""
        path = "/api/trends"
        if category:
            path += f"?category={category}"
        return self._get(path)
    
    # ── Schedule ───────────────────────────────────────────────────
    
    def get_schedule(self) -> Dict:
        """Get user's cronjob schedule."""
        return self._get(f"/api/user/schedule?key={self.license_key}")
    
    def update_schedule(self, settings: Dict) -> Dict:
        """Update user's cronjob schedule."""
        return self._put("/api/user/schedule", {
            "key": self.license_key,
            **settings,
        })
    
    def get_limits(self) -> Dict:
        """Get user's rate limits."""
        return self._get(f"/api/user/limits?key={self.license_key}")
    
    # ── Queue ──────────────────────────────────────────────────────
    
    def trigger_job(self, job_type: str, metadata: dict = None) -> Dict:
        """Trigger a job in the queue."""
        return self._post("/api/queue/trigger", {
            "key": self.license_key,
            "job_type": job_type,
            "metadata": metadata,
        })
    
    def get_queue_status(self) -> Dict:
        """Get user's queue status."""
        return self._get(f"/api/queue/status?key={self.license_key}")
    
    def get_queue_history(self) -> Dict:
        """Get user's job history."""
        return self._get(f"/api/queue/history?key={self.license_key}")
    
    def get_task_status(self, task_id: str) -> Dict:
        """Get background task status."""
        return self._get(f"/api/task/{task_id}")

    def wait_for_task(self, task_id: str, timeout: int = 300, poll_interval: int = 5) -> Dict:
        """Wait for background task to complete.
        
        Args:
            task_id: Task ID to wait for
            timeout: Max seconds to wait (default: 5 minutes)
            poll_interval: Seconds between polls (default: 5)
        
        Returns:
            Task result or error
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            result = self.get_task_status(task_id)
            
            if result.get("error"):
                return result
            
            status = result.get("status")
            
            if status == "SUCCESS":
                return result.get("result", {})
            elif status == "FAILURE":
                return {"error": "Task failed", "details": result.get("result")}
            elif status in ("PENDING", "STARTED", "RETRY"):
                time.sleep(poll_interval)
            else:
                time.sleep(poll_interval)
        
        return {"error": "Task timeout", "task_id": task_id}
    
    # ── License ────────────────────────────────────────────────────
    
    def validate_license(self) -> Dict:
        """Validate license key."""
        return self._post("/api/validate", {"key": self.license_key})
    
    # ── Health ─────────────────────────────────────────────────────
    
    def health_check(self) -> Dict:
        """Check if server is reachable."""
        return self._get("/api/status")
    
    # ── AI Settings ──────────────────────────────────────────────
    
    def update_ai_settings(self, provider: str, model: str, api_key: str) -> Dict:
        """Update AI provider settings.
        
        Args:
            provider: AI provider (openai, deepseek, ollama)
            model: Model name (gpt-4, deepseek-chat, llama2)
            api_key: API key (will be encrypted server-side)
        
        Returns:
            Dict with success status and masked key hint
        """
        return self._post("/api/settings/ai", {
            "key": self.license_key,
            "provider": provider,
            "model": model,
            "api_key": api_key
        })
    
    def get_ai_settings(self) -> Dict:
        """Get AI provider settings."""
        return self._get(f"/api/settings/ai?key={self.license_key}")
    
    def delete_ai_settings(self) -> Dict:
        """Delete AI provider settings."""
        return self._request("DELETE", f"/api/settings/ai?key={self.license_key}")
    
    def check_article_limit(self) -> Dict:
        """Check article limit for user."""
        return self._get(f"/api/usage/articles?key={self.license_key}")
    
    def test_ai_provider(self) -> Dict:
        """Test AI provider connection."""
