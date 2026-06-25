#!/usr/bin/env python3
"""
ContentPilot — License Activation

Jalankan script ini untuk activate license key.

Usage:
    python3 scripts/activate.py
    python3 scripts/activate.py --key SB-XXXX-XXXX-XXXX
"""

import argparse
import json
import hashlib
import platform
import requests
from pathlib import Path

LICENSE_SERVER = "http://localhost:5000"
LICENSE_FILE = Path("workspace/.license")

def get_machine_id() -> str:
    """Generate unique machine ID."""
    system_info = f"{platform.node()}-{platform.system()}-{platform.machine()}"
    return hashlib.md5(system_info.encode()).hexdigest()

def validate_key(key: str, server_url: str = LICENSE_SERVER) -> dict:
    """Validate license key with server."""
    try:
        response = requests.post(
            f"{server_url}/validate",
            json={"key": key, "machine_id": get_machine_id()},
            timeout=10
        )
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"valid": False, "error": f"Cannot connect to license server: {e}"}

def activate_key(key: str, server_url: str = LICENSE_SERVER) -> dict:
    """Activate license key with server."""
    try:
        response = requests.post(
            f"{server_url}/activate",
            json={"key": key, "machine_id": get_machine_id()},
            timeout=10
        )
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"Cannot connect to license server: {e}"}

def save_license_locally(key: str, tier: str):
    """Save license info locally for offline validation."""
    LICENSE_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    license_data = {
        "key": key,
        "tier": tier,
        "machine_id": get_machine_id(),
        "activated_at": __import__('datetime').datetime.now().isoformat()
    }
    
    with open(LICENSE_FILE, 'w') as f:
        json.dump(license_data, f, indent=2)

def load_local_license() -> dict:
    """Load local license info."""
    if LICENSE_FILE.exists():
        with open(LICENSE_FILE, 'r') as f:
            return json.load(f)
    return {}

def check_license() -> dict:
    """Check if license is valid."""
    local_license = load_local_license()
    
    if not local_license:
        return {"valid": False, "error": "No license found. Please activate first."}
    
    # Validate with server
    result = validate_key(local_license["key"])
    
    if result.get("valid"):
        return result
    
    # If server unavailable, check local
    if "Cannot connect" in result.get("error", ""):
        # Offline mode - trust local license
        return {
            "valid": True,
            "tier": local_license.get("tier", "free"),
            "offline_mode": True
        }
    
    return result

def main():
    parser = argparse.ArgumentParser(description="Activate ContentPilot license")
    parser.add_argument("--key", help="License key to activate")
    parser.add_argument("--server", default=LICENSE_SERVER, help="License server URL")
    parser.add_argument("--check", action="store_true", help="Check current license status")
    
    args = parser.parse_args()
    
    if args.check:
        # Check license
        result = check_license()
        
        if result.get("valid"):
            print()
            print("=" * 60)
            print("  ✅ License Active")
            print("=" * 60)
            print()
            print(f"  Tier:       {result.get('tier', 'unknown')}")
            print(f"  Expires:    {result.get('expires_at', 'unknown')}")
            if result.get('offline_mode'):
                print("  Mode:       Offline (server unavailable)")
            print()
        else:
            print()
            print("=" * 60)
            print("  ❌ License Invalid")
            print("=" * 60)
            print()
            print(f"  Error: {result.get('error', 'Unknown error')}")
            print()
            print("  Please activate your license:")
            print("  python3 scripts/activate.py --key YOUR-KEY")
            print()
        
        return
    
    # Activate license
    if not args.key:
        print("Please enter your license key:")
        key = input("Key: ").strip()
    else:
        key = args.key
    
    if not key:
        print("Error: No license key provided")
        return
    
    print()
    print("Activating license...")
    
    # First validate
    result = validate_key(key, args.server)
    
    if not result.get("valid") and result.get("needs_activation"):
        # Need to activate
        result = activate_key(key, args.server)
        
        if result.get("success"):
            # Save locally
            licenses = {}
            license_data = None
            
            # Get tier from server
            validate_result = validate_key(key, args.server)
            tier = validate_result.get("tier", "free")
            
            save_license_locally(key, tier)
            
            print()
            print("=" * 60)
            print("  ✅ License Activated!")
            print("=" * 60)
            print()
            print(f"  Key:    {key}")
            print(f"  Tier:   {tier}")
            print()
            print("  You can now use ContentPilot!")
            print("  Run: python3 -m blog.pipeline status")
            print()
        else:
            print()
            print("=" * 60)
            print("  ❌ Activation Failed")
            print("=" * 60)
            print()
            print(f"  Error: {result.get('error', 'Unknown error')}")
            print()
    elif result.get("valid"):
        # Already valid
        tier = result.get("tier", "free")
        save_license_locally(key, tier)
        
        print()
        print("=" * 60)
        print("  ✅ License Already Active")
        print("=" * 60)
        print()
        print(f"  Tier: {tier}")
        print()
    else:
        print()
        print("=" * 60)
        print("  ❌ Invalid License Key")
        print("=" * 60)
        print()
        print(f"  Error: {result.get('error', 'Unknown error')}")
        print()

if __name__ == "__main__":
    main()
