#!/usr/bin/env python3
"""
Generate SOUL.md for all blog-lifecycle profiles.

Shared protocol boilerplate defined once in profiles/_shared/protocol.md.
Per-profile unique content in profiles/_unique/<name>.md.
Orchestrator has no shared protocol — its _unique file IS the full SOUL.md.

Usage:
    python3 scripts/generate_souls.py              # Dry-run: show what would change
    python3 scripts/generate_souls.py --write       # Write SOUL.md files
    python3 scripts/generate_souls.py --check       # Exit 1 if any file needs updating (CI)
"""

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROFILES_DIR = PROJECT_ROOT / "profiles"
SHARED_DIR = PROFILES_DIR / "_shared"
UNIQUE_DIR = PROFILES_DIR / "_unique"

WORKERS = {
    "researcher": "researcher",
    "writer": "writer",
    "editor": "editor",
    "analyst": "analyst",
    "imagery": "imagery",
    "publisher": "publisher",
}

ORCHESTRATOR = "blog_orchestrator"


def generate():
    protocol_path = SHARED_DIR / "protocol.md"
    if not protocol_path.exists():
        print(f"ERROR: {protocol_path} not found")
        sys.exit(1)

    protocol_template = protocol_path.read_text()
    results = {}

    for name, role_lower in WORKERS.items():
        unique_path = UNIQUE_DIR / f"{name}.md"
        if not unique_path.exists():
            print(f"WARNING: {unique_path} not found, skipping {name}")
            continue

        unique = unique_path.read_text()
        protocol = protocol_template.replace("{role_lower}", role_lower)
        results[f"{name}-SOUL.md"] = unique.rstrip("\n") + "\n\n" + protocol

    orch_path = UNIQUE_DIR / f"{ORCHESTRATOR}.md"
    if orch_path.exists():
        results[f"{ORCHESTRATOR}-SOUL.md"] = orch_path.read_text()
    else:
        print(f"WARNING: {orch_path} not found, skipping orchestrator")

    return results


def main():
    parser = argparse.ArgumentParser(description="Generate SOUL.md files from shared + unique parts")
    parser.add_argument("--write", action="store_true", help="Write generated files")
    parser.add_argument("--check", action="store_true", help="Exit 1 if any file needs updating")
    args = parser.parse_args()

    results = generate()
    needs_update = False

    print(f"Source: {UNIQUE_DIR.relative_to(PROJECT_ROOT)}/  +  {(SHARED_DIR / 'protocol.md').relative_to(PROJECT_ROOT)}")
    print(f"Output: {PROFILES_DIR.relative_to(PROJECT_ROOT)}/\n")

    for filename, content in sorted(results.items()):
        output_path = PROFILES_DIR / filename
        existing = output_path.read_text() if output_path.exists() else ""

        new_lines = content.count("\n") + 1
        old_lines = existing.count("\n") + 1 if existing else 0
        changed = content != existing
        delta = new_lines - old_lines
        sign = "+" if delta > 0 else ""

        if changed:
            needs_update = True
            status = "CHANGED"
        else:
            status = "ok"

        print(f"  {filename:<30s} {old_lines:>4d} → {new_lines:>4d} lines ({sign}{delta:>+3d})  [{status}]")

        if args.write and changed:
            output_path.write_text(content)
            print(f"    → written")

    print()
    if needs_update:
        if args.write:
            print("Done. Files updated.")
        elif args.check:
            print("FAIL: Some SOUL.md files are out of date. Run with --write to update.")
            sys.exit(1)
        else:
            print("Dry-run. Use --write to save changes.")
    else:
        print("All SOUL.md files are up to date.")


if __name__ == "__main__":
    main()
