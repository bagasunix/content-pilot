#!/usr/bin/env python3
"""Backward-compat shim → `pipeline.py attach-images <idea_id>`.

The real logic now lives in the clean-architecture pipeline (service use case
`attach_images` + DriveImageHost adapter). Kept so existing callers keep working.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from blog.interface.cli import main  # noqa: E402

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: attach_images.py <idea_id>")
        sys.exit(2)
    sys.exit(main(["attach-images", sys.argv[1]]))
