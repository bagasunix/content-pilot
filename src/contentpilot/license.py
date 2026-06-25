"""ContentPilot — License Client

Validates license key against ContentPilot server.
Stores activation locally for offline use.

Usage:
    from contentpilot.license import check_license, activate_license

    if not check_license():
        print("Please activate your license first")
        sys.exit(1)
"""
from __future__ import annotations

import hashlib
import json
import platform
import sys
from pathlib import Path

# Server URL
LICENSE_SERVER = "https://api.contentpilot.dev"

# Local storage
LICENSE_FILE = Path("workspace/.license")


def get_machine_id() -> str:
    """Generate unique machine ID from hardware info."""
    system_info = f"{platform.node()}-{platform.system()}-{platform.machine()}"
    return hashlib.md5(system_info.encode()).hexdigest()


def load_local_license() -> dict:
    """Load local license info."""
    if LICENSE_FILE.exists():
        try:
            return json.loads(LICENSE_FILE.read_text())
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def save_local_license(data: dict) -> None:
    """Save license info locally."""
    LICENSE_FILE.parent.mkdir(parents=True, exist_ok=True)
    LICENSE_FILE.write_text(json.dumps(data, indent=2))


def validate_with_server(key: str) -> dict:
    """Validate license with server."""
    try:
        import requests
        response = requests.post(
            f"{LICENSE_SERVER}/validate",
            json={"key": key, "machine_id": get_machine_id()},
            timeout=5,
        )
        return response.json()
    except Exception:
        return {"valid": False, "error": "Server unavailable"}


def activate_with_server(key: str) -> dict:
    """Activate license with server."""
    try:
        import requests
        response = requests.post(
            f"{LICENSE_SERVER}/activate",
            json={"key": key, "machine_id": get_machine_id()},
            timeout=5,
        )
        return response.json()
    except Exception:
        return {"success": False, "error": "Server unavailable"}


def check_license() -> bool:
    """
    Check if license is valid.

    Returns True if:
    - Local license exists AND is valid
    - OR server confirms valid
    - OR server is offline (grace period)
    """
    local = load_local_license()

    # No local license
    if not local.get("key"):
        return False

    # Check expiry
    if local.get("expires_at"):
        from datetime import datetime, timezone
        try:
            expires = datetime.fromisoformat(local["expires_at"])
            if datetime.now(timezone.utc) > expires:
                return False
        except (ValueError, TypeError):
            pass

    # Try server validation (online check)
    result = validate_with_server(local["key"])
    if result.get("valid"):
        # Update local cache
        save_local_license({
            "key": local["key"],
            "tier": result.get("tier", local.get("tier", "free")),
            "expires_at": result.get("expires_at", local.get("expires_at")),
            "validated_at": datetime.now(timezone.utc).isoformat(),
        })
        return True

    # Server unavailable — use local cache with grace period
    if result.get("error") == "Server unavailable":
        if local.get("validated_at"):
            from datetime import datetime, timedelta, timezone
            try:
                validated = datetime.fromisoformat(local["validated_at"])
                if datetime.now(timezone.utc) - validated < timedelta(days=7):
                    return True  # 7-day offline grace
            except (ValueError, TypeError):
                pass

    return False


def activate_license(key: str) -> dict:
    """
    Activate a license key.

    Returns:
        {"success": True, "tier": "free", "expires_at": "..."}
        or {"success": False, "error": "..."}
    """
    result = activate_with_server(key)

    if result.get("success"):
        save_local_license({
            "key": key,
            "tier": result.get("tier", "free"),
            "expires_at": result.get("expires_at"),
            "activated_at": result.get("activated_at"),
            "validated_at": result.get("activated_at"),
        })
        return result

    return result


def get_license_info() -> dict:
    """Get current license info."""
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
    """Check license, exit if invalid."""
    if not check_license():
        info = get_license_info()
        if info.get("error") == "No license key":
            print("❌ No license key found.")
            print("   Run: contentpilot activate --key YOUR-KEY")
        else:
            print("❌ License invalid or expired.")
            print("   Run: contentpilot activate --key YOUR-KEY")
        sys.exit(1)
