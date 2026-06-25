"""
ContentPilot — License Validation Module

Validate license before running pipeline.

Usage:
    from blog.license import check_license
    
    if not check_license():
        print("Please activate your license first")
        sys.exit(1)
"""

import json
import hashlib
import platform
import requests
from pathlib import Path
from typing import Optional

LICENSE_SERVER = "https://api.smartblogger.dev"
LICENSE_FILE = Path("workspace/.license")

def get_machine_id() -> str:
    """Generate unique machine ID."""
    system_info = f"{platform.node()}-{platform.system()}-{platform.machine()}"
    return hashlib.md5(system_info.encode()).hexdigest()

def load_local_license() -> dict:
    """Load local license info."""
    if LICENSE_FILE.exists():
        with open(LICENSE_FILE, 'r') as f:
            return json.load(f)
    return {}

def validate_with_server(key: str, server_url: str = LICENSE_SERVER) -> dict:
    """Validate license with server."""
    try:
        response = requests.post(
            f"{server_url}/validate",
            json={"key": key, "machine_id": get_machine_id()},
            timeout=5
        )
        return response.json()
    except requests.exceptions.RequestException:
        return {"valid": False, "error": "Server unavailable"}

def check_license(server_url: str = LICENSE_SERVER) -> dict:
    """
    Check if license is valid.
    
    Returns:
        dict with keys:
            - valid: bool
            - tier: str (if valid)
            - error: str (if invalid)
            - offline_mode: bool (if using local cache)
    """
    local_license = load_local_license()
    
    if not local_license:
        return {
            "valid": False,
            "error": "No license found. Please run: python3 scripts/activate.py"
        }
    
    # Try server validation
    result = validate_with_server(local_license["key"], server_url)
    
    if result.get("valid"):
        return result
    
    # If server unavailable, use offline mode
    if "Server unavailable" in result.get("error", ""):
        return {
            "valid": True,
            "tier": local_license.get("tier", "free"),
            "offline_mode": True
        }
    
    return result

def get_tier_info(tier: str) -> dict:
    """Get tier information."""
    tiers = {
        "free": {
            "name": "Free",
            "articles_limit": 10,
            "features": ["basic_pipeline", "seo_check"]
        },
        "pro": {
            "name": "Pro",
            "articles_limit": -1,
            "features": ["basic_pipeline", "seo_check", "analytics", "auto_publish"]
        },
        "business": {
            "name": "Business",
            "articles_limit": -1,
            "features": ["basic_pipeline", "seo_check", "analytics", "auto_publish", "priority_support"]
        }
    }
    return tiers.get(tier, tiers["free"])

def track_usage(action: str, server_url: str = LICENSE_SERVER):
    """Track usage with server."""
    local_license = load_local_license()
    if not local_license:
        return
    
    try:
        requests.post(
            f"{server_url}/track",
            json={"key": local_license["key"], "action": action},
            timeout=5
        )
    except requests.exceptions.RequestException:
        pass  # Silent fail for tracking

def is_feature_available(feature: str) -> bool:
    """Check if a feature is available for current tier."""
    result = check_license()
    
    if not result.get("valid"):
        return False
    
    tier_info = get_tier_info(result.get("tier", "free"))
    return feature in tier_info.get("features", [])

# ============================================================
# CONVENIENCE FUNCTIONS
# ============================================================

def require_license():
    """Require valid license to proceed."""
    result = check_license()
    
    if not result.get("valid"):
        print()
        print("=" * 60)
        print("  ❌ LICENSE REQUIRED")
        print("=" * 60)
        print()
        print(f"  {result.get('error', 'Unknown error')}")
        print()
        print("  Please activate your license:")
        print("  python3 scripts/activate.py --key YOUR-KEY")
        print()
        print("  Get a free key at: https://smartblogger.dev/free")
        print()
        exit(1)
    
    return result

def print_license_status():
    """Print current license status."""
    result = check_license()
    
    if result.get("valid"):
        tier_info = get_tier_info(result.get("tier", "free"))
        print()
        print("=" * 60)
        print("  ✅ LICENSE ACTIVE")
        print("=" * 60)
        print()
        print(f"  Tier:       {result.get('tier', 'unknown')}")
        print(f"  Features:   {', '.join(tier_info.get('features', []))}")
        if result.get('offline_mode'):
            print(f"  Mode:       Offline")
        print()
    else:
        print()
        print("=" * 60)
        print("  ❌ NO LICENSE")
        print("=" * 60)
        print()
        print(f"  {result.get('error', 'Unknown error')}")
        print()
