#!/usr/bin/env python3
"""ContentPilot Desktop — PyWebView wrapper.

Launches the Flask web UI inside a native desktop window.
No browser needed — feels like a real desktop application.

Usage:
    python3 web/desktop.py              # default 1200x800
    python3 web/desktop.py --width 1400 --height 900
    python3 web/desktop.py --fullscreen
    python3 web/desktop.py --debug      # Flask debug mode
"""
from __future__ import annotations

import argparse
import logging
import os
import signal
import socket
import sys
import threading
import time
from pathlib import Path

# Force Qt backend for PyWebView (cross-platform)
os.environ["WEBVIEW_GUI"] = "qt"

# Ensure parent dirs are importable
_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parent
sys.path.insert(0, str(_ROOT / "src"))
sys.path.insert(0, str(_ROOT))

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("contentpilot-desktop")

# ── Window Configuration ──────────────────────────────────────────
WINDOW_CONFIG = {
    "title": "ContentPilot — Blog Automation",
    "width": 1200,
    "height": 800,
    "min_size": (800, 600),
    "resizable": True,
    "text_select": True,
}

# Icon path (cross-platform)
_ICON_DIR = _HERE / "static" / "favicon"
_ICON_CANDIDATES = [
    _ICON_DIR / "app-icon-256x256.png",  # Linux/Mac
    _ICON_DIR / "favicon.ico",            # Windows
]


def _find_icon() -> str | None:
    """Find the best available icon file."""
    for p in _ICON_CANDIDATES:
        if p.exists():
            return str(p)
    return None


# ── Flask Lifecycle ────────────────────────────────────────────────

_flask_server = None
_flask_port = 8080


def _start_flask(port: int, debug: bool = False) -> None:
    """Run Flask in a background thread."""
    global _flask_server
    try:
        from web.app import app
        _flask_server = app
        log.info(f"Flask starting on http://127.0.0.1:{port}")
        app.run(host="127.0.0.1", port=port, debug=debug, use_reloader=False)
    except Exception as e:
        log.error(f"Flask failed to start: {e}")
        sys.exit(1)


def _wait_for_server(port: int, timeout: float = 15.0) -> bool:
    """Block until Flask is ready to accept connections."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=1):
                log.info(f"Flask ready on port {port}")
                return True
        except OSError:
            time.sleep(0.2)
    return False


def _stop_flask() -> None:
    """Attempt graceful Flask shutdown."""
    log.info("Shutting down Flask...")
    # Flask's dev server doesn't have a clean shutdown API
    # The daemon thread will die when main thread exits
    # For production, use gunicorn with signal handling


# ── Window Event Handlers ─────────────────────────────────────────

def _on_window_closed() -> None:
    """Called when the PyWebView window is closed."""
    log.info("Window closed, exiting...")
    _stop_flask()
    os._exit(0)  # Force exit to kill Flask thread


def _inject_js_api(window) -> None:
    """Expose Python functions to JavaScript (optional)."""
    class Api:
        def get_version(self):
            return "1.1.0"

        def get_server_url(self):
            return f"http://127.0.0.1:{_flask_port}"

    window.expose(Api())


# ── Main Entry Point ──────────────────────────────────────────────

def main() -> None:
    global _flask_port

    parser = argparse.ArgumentParser(
        description="ContentPilot Desktop — AI Blog Automation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 web/desktop.py                    # Start with defaults
  python3 web/desktop.py --port 5001        # Use server port 5001
  python3 web/desktop.py --fullscreen       # Fullscreen mode
  python3 web/desktop.py --debug            # Flask debug mode
        """,
    )
    parser.add_argument(
        "--port", type=int, default=8080,
        help="Flask server port (default: 8080)",
    )
    parser.add_argument(
        "--server-url", type=str, default=None,
        help="Connect to existing server URL (skip Flask start)",
    )
    parser.add_argument(
        "--width", type=int, default=WINDOW_CONFIG["width"],
        help=f"Window width (default: {WINDOW_CONFIG['width']})",
    )
    parser.add_argument(
        "--height", type=int, default=WINDOW_CONFIG["height"],
        help=f"Window height (default: {WINDOW_CONFIG['height']})",
    )
    parser.add_argument(
        "--fullscreen", action="store_true",
        help="Start in fullscreen mode",
    )
    parser.add_argument(
        "--debug", action="store_true",
        help="Enable Flask debug mode (development only)",
    )
    args = parser.parse_args()

    _flask_port = args.port

    # ── Start Flask (unless connecting to existing server) ─────────
    if args.server_url:
        url = args.server_url
        log.info(f"Connecting to existing server: {url}")
    else:
        flask_thread = threading.Thread(
            target=_start_flask,
            args=(args.port, args.debug),
            daemon=True,
        )
        flask_thread.start()

        if not _wait_for_server(args.port):
            log.error("Flask server did not start in time (15s timeout)")
            log.error("Check if port is already in use or dependencies missing")
            sys.exit(1)

        url = f"http://127.0.0.1:{args.port}"

    # ── Create Native Window ───────────────────────────────────────
    try:
        import webview
    except ImportError:
        log.error("pywebview not installed. Run: pip install pywebview[qt]")
        sys.exit(1)

    icon = _find_icon()
    if icon:
        log.info(f"Using icon: {icon}")

    log.info(f"Opening window: {args.width}x{args.height} {'fullscreen' if args.fullscreen else ''}")

    # Add desktop=1 parameter for frontend detection
    desktop_url = url + ("&" if "?" in url else "?") + "desktop=1"

    window = webview.create_window(
        title=WINDOW_CONFIG["title"],
        url=desktop_url,
        width=args.width,
        height=args.height,
        min_size=WINDOW_CONFIG["min_size"],
        resizable=WINDOW_CONFIG["resizable"],
        text_select=WINDOW_CONFIG["text_select"],
        fullscreen=args.fullscreen,
    )

    if window is None:
        log.error("Failed to create window")
        sys.exit(1)

    # Inject JS API
    _inject_js_api(window)

    # Handle window close
    window.events.closed += _on_window_closed

    # ── Start GUI Loop ─────────────────────────────────────────────
    # gui="qt" works cross-platform (Qt5/Qt6)
    # debug=True enables dev tools in webview
    try:
        webview.start(
            gui="qt",
            debug=args.debug,
        )
    except Exception as e:
        log.error(f"PyWebView error: {e}")
        log.error("Try: pip install PyQt5 or PyQt6")
        sys.exit(1)

    # Cleanup after window closes
    _stop_flask()
    log.info("ContentPilot Desktop exited.")


if __name__ == "__main__":
    # Handle Ctrl+C gracefully
    signal.signal(signal.SIGINT, lambda *_: (_stop_flask(), sys.exit(0)))
    main()
