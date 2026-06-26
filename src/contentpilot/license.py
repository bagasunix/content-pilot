"""ContentPilot — License Client

Works offline (local validation) + online (server validation).
"""
from __future__ import annotations

import hashlib
import json
import platform
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

LICENSE_SERVER = "https://api.contentpilot.dev"
LICENSE_FILE = Path("workspace/.license")


def get_machine_id() -> str:
    system_info = f"{platform.node()}-{platform.system()}-{platform.machine()}"
    return hashlib.md5(system_info.encode()).hexdigest()


def load_local_license() -> dict:
    if LICENSE_FILE.exists():
        try:
            return json.loads(LICENSE_FILE.read_text())
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def save_local_license(data: dict) -> None:
    LICENSE_FILE.parent.mkdir(parents=True, exist_ok=True)
    LICENSE_FILE.write_text(json.dumps(data, indent=2))


def activate_license(key: str) -> dict:
    """Activate license — tries server first, falls back to local."""
    # Try server
    try:
        import requests
        resp = requests.post(
            f"{LICENSE_SERVER}/activate",
            json={"key": key, "machine_id": get_machine_id()},
            timeout=5,
        )
        if resp.status_code == 200:
            result = resp.json()
            if result.get("success"):
                save_local_license({
                    "key": key,
                    "tier": result.get("tier", "free"),
                    "expires_at": result.get("expires_at"),
                    "activated_at": datetime.now(timezone.utc).isoformat(),
                    "validated_at": datetime.now(timezone.utc).isoformat(),
                })
                return result
    except Exception:
        pass

    # Offline activation — accept any CP- prefixed key
    if key.startswith("CP-"):
        expires = (datetime.now(timezone.utc) + timedelta(days=365)).isoformat()
        save_local_license({
            "key": key,
            "tier": "pro",
            "expires_at": expires,
            "activated_at": datetime.now(timezone.utc).isoformat(),
            "validated_at": datetime.now(timezone.utc).isoformat(),
        })
        return {"success": True, "tier": "pro", "expires_at": expires}

    return {"success": False, "error": "Invalid key format"}


def check_license() -> bool:
    """Check if license is valid."""
    local = load_local_license()
    if not local.get("key"):
        return False
    if local.get("expires_at"):
        try:
            expires = datetime.fromisoformat(local["expires_at"])
            if datetime.now(timezone.utc) > expires:
                return False
        except (ValueError, TypeError):
            pass
    return True


def get_license_info() -> dict:
    local = load_local_license()
    if not local.get("key"):
        return {"active": False, "error": "No license key"}
    return {
        "active": check_license(),
        "key": local["key"][:8] + "..." if len(local.get("key", "")) > 8 else local.get("key"),
        "tier": local.get("tier", "unknown"),
        "expires_at": local.get("expires_at"),
    }


def require_license() -> None:
    if not check_license():
        print("❌ No valid license. Run: contentpilot activate --key YOUR-KEY")
        sys.exit(1)
