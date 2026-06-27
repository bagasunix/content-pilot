#!/usr/bin/env python3
"""ContentPilot Desktop — PyWebView wrapper.

Launches the Flask web UI inside a native desktop window.
No browser needed — feels like a real desktop application.

Usage:
    python3 web/desktop.py              # default 1200x800
    python3 web/desktop.py --width 1400 --height 900
    python3 web/desktop.py --fullscreen
"""
from __future__ import annotations

import argparse
import os
import sys
import threading
import time
from pathlib import Path

# Ensure parent dirs are importable
_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parent
sys.path.insert(0, str(_ROOT / "src"))
sys.path.insert(0, str(_ROOT))


# Window configuration
WINDOW_CONFIG = {
    "title": "ContentPilot — Blog Automation",
    "width": 1200,
    "height": 800,
    "min_size": (800, 600),
    "resizable": True,
    "text_select": True,
}


def _start_flask(port: int) -> None:
    """Run Flask in a background thread."""
    from web.app import app
    app.run(host="127.0.0.1", port=port, debug=False, use_reloader=False)


def _wait_for_server(port: int, timeout: float = 10.0) -> bool:
    """Block until Flask is ready to accept connections."""
    import socket
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=1):
                return True
        except OSError:
            time.sleep(0.15)
    return False


def main() -> None:
    parser = argparse.ArgumentParser(description="ContentPilot Desktop")
    parser.add_argument("--port", type=int, default=8080, help="Flask port (default: 8080)")
    parser.add_argument("--width", type=int, default=WINDOW_CONFIG["width"], 
                        help=f"Window width (default: {WINDOW_CONFIG['width']})")
    parser.add_argument("--height", type=int, default=WINDOW_CONFIG["height"],
                        help=f"Window height (default: {WINDOW_CONFIG['height']})")
    parser.add_argument("--fullscreen", action="store_true", help="Start in fullscreen")
    args = parser.parse_args()

    # Start Flask in background
    flask_thread = threading.Thread(
        target=_start_flask, args=(args.port,), daemon=True
    )
    flask_thread.start()

    # Wait for Flask to be ready
    if not _wait_for_server(args.port):
        print("ERROR: Flask server did not start in time.", file=sys.stderr)
        sys.exit(1)

    # Open native window
    import webview

    window = webview.create_window(
        title=WINDOW_CONFIG["title"],
        url=f"http://127.0.0.1:{args.port}",
        width=args.width,
        height=args.height,
        min_size=WINDOW_CONFIG["min_size"],
        resizable=WINDOW_CONFIG["resizable"],
        text_select=WINDOW_CONFIG["text_select"],
        fullscreen=args.fullscreen,
    )

    webview.start()


if __name__ == "__main__":
    main()
