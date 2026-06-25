#!/usr/bin/env python3
"""Thin entry point — delegates to the clean-architecture CLI in the `blog` package.

Kept at this path for backward compatibility (cron job, blog-lifecycle-orchestrator
skill, and check-readiness.sh all call `python3 python3 -m contentpilot.pipeline ...`).
Real logic lives in blog/{domain,application,infrastructure,interface}.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from contentpilot.interface.cli import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
