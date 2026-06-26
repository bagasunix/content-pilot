"""
ContentPilot Sync Cache — Local cache for server data.

Stores: rules, suggestions, trending, schedule.
Falls back to cache when offline.
"""
import json
from pathlib import Path
from typing import Dict, Optional


class SyncCache:
    """Local cache for server data."""
    
    def __init__(self, cache_dir: str = None):
        if cache_dir:
            self.cache_dir = Path(cache_dir)
        else:
            # Default: workspace/cache/
            self.cache_dir = Path("workspace/cache")
        
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_path(self, key: str) -> Path:
        """Get cache file path for key."""
        return self.cache_dir / f"{key}.json"
    
    def get(self, key: str) -> Optional[Dict]:
        """Get cached data (unwrapped)."""
        path = self._get_path(key)
        if path.exists():
            try:
                with open(path, "r") as f:
                    wrapper = json.load(f)
                # Unwrap: return just the data, not the wrapper
                return wrapper.get("data")
            except Exception:
                return None
        return None
    
    def set(self, key: str, data: Dict, ttl_hours: int = 6) -> bool:
        """Set cached data with TTL."""
        path = self._get_path(key)
        cache_data = {
            "data": data,
            "cached_at": __import__("datetime").datetime.now().isoformat(),
            "ttl_hours": ttl_hours,
        }
        try:
            with open(path, "w") as f:
                json.dump(cache_data, f, indent=2)
            return True
        except Exception:
            return False
    
    def _get_raw(self, key: str) -> Optional[Dict]:
        """Get raw wrapper (for TTL check)."""
        path = self._get_path(key)
        if path.exists():
            try:
                with open(path, "r") as f:
                    return json.load(f)
            except Exception:
                return None
        return None
    
    def is_fresh(self, key: str) -> bool:
        """Check if cache is still fresh (within TTL)."""
        raw = self._get_raw(key)
        if not raw:
            return False
        
        from datetime import datetime, timedelta
        
        cached_at = datetime.fromisoformat(raw["cached_at"])
        ttl_hours = raw.get("ttl_hours", 6)
        
        return datetime.now() < cached_at + timedelta(hours=ttl_hours)
    
    def get_or_fetch(self, key: str, fetch_fn, ttl_hours: int = 6) -> Dict:
        """Get from cache if fresh, otherwise fetch and cache."""
        if self.is_fresh(key):
            cached = self.get(key)
            if cached:
                return cached
        
        # Fetch fresh data
        data = fetch_fn()
        if data and not data.get("error"):
            self.set(key, data, ttl_hours)
        return data
    
    def invalidate(self, key: str) -> bool:
        """Remove cached data."""
        path = self._get_path(key)
        if path.exists():
            path.unlink()
            return True
        return False
    
    def clear(self) -> int:
        """Clear all cached data."""
        count = 0
        for path in self.cache_dir.glob("*.json"):
            path.unlink()
            count += 1
        return count
    
    # ── Convenience methods ────────────────────────────────────────
    
    def get_rules(self) -> Optional[Dict]:
        return self.get("rules")
    
    def set_rules(self, rules: Dict) -> bool:
        return self.set("rules", rules, ttl_hours=24)
    
    def get_suggestions(self) -> Optional[Dict]:
        return self.get("suggestions")
    
    def set_suggestions(self, suggestions: Dict) -> bool:
        return self.set("suggestions", suggestions, ttl_hours=6)
    
    def get_trending(self) -> Optional[Dict]:
        return self.get("trending")
    
    def set_trending(self, trending: Dict) -> bool:
        return self.set("trending", trending, ttl_hours=1)
    
    def get_schedule(self) -> Optional[Dict]:
        return self.get("schedule")
    
    def set_schedule(self, schedule: Dict) -> bool:
        return self.set("schedule", schedule, ttl_hours=24)
