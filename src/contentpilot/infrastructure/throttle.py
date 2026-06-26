"""Token-bucket throttler + exponential backoff for shared model endpoints.

Problem: N bot profiles concurrent → single endpoint → 429/empty-stream cascade.
Solution: Global token-bucket gates concurrent requests; 429 triggers exponential backoff.

Usage:
    from contentpilot.infrastructure.throttle import ThrottledClient
    client = ThrottledClient()  # uses OLLAMA_URL env var or default
    response = client.post("/chat/completions", json=payload)
"""
from __future__ import annotations

import json
import logging
import os
import threading
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field

log = logging.getLogger(__name__)

# ── defaults (override via env) ──────────────────────────────────────────────

DEFAULT_MAX_CONCURRENT = int(os.getenv("THROTTLE_MAX_CONCURRENT", "2"))
DEFAULT_RATE_PER_SEC = float(os.getenv("THROTTLE_RATE_PER_SEC", "1.0"))  # tokens/sec
DEFAULT_BUCKET_SIZE = int(os.getenv("THROTTLE_BUCKET_SIZE", "3"))
DEFAULT_BACKOFF_BASE = float(os.getenv("THROTTLE_BACKOFF_BASE", "2.0"))
DEFAULT_BACKOFF_MAX = float(os.getenv("THROTTLE_BACKOFF_MAX", "60.0"))
DEFAULT_MAX_RETRIES = int(os.getenv("THROTTLE_MAX_RETRIES", "3"))


# ── token bucket ─────────────────────────────────────────────────────────────

class _TokenBucket:
    """Thread-safe token bucket for rate limiting."""

    def __init__(self, rate: float, max_tokens: int):
        self._rate = rate          # tokens per second
        self._max = max_tokens
        self._tokens = float(max_tokens)
        self._last_refill = time.monotonic()
        self._lock = threading.Lock()

    def acquire(self, timeout: float = 30.0) -> bool:
        """Block until a token is available or timeout expires."""
        deadline = time.monotonic() + timeout
        while True:
            with self._lock:
                self._refill()
                if self._tokens >= 1.0:
                    self._tokens -= 1.0
                    return True
            if time.monotonic() >= deadline:
                return False
            time.sleep(0.05)

    def _refill(self):
        now = time.monotonic()
        elapsed = now - self._last_refill
        self._tokens = min(self._max, self._tokens + elapsed * self._rate)
        self._last_refill = now


# ── semaphore for max concurrent ─────────────────────────────────────────────

class _ConcurrencyGate:
    """Simple counting semaphore with timeout."""

    def __init__(self, max_concurrent: int):
        self._sem = threading.Semaphore(max_concurrent)
        self._max = max_concurrent
        self._current = 0
        self._lock = threading.Lock()

    def acquire(self, timeout: float = 60.0) -> bool:
        got = self._sem.acquire(timeout=timeout)
        if got:
            with self._lock:
                self._current += 1
        return got

    def release(self):
        with self._lock:
            self._current = max(0, self._current - 1)
        self._sem.release()

    @property
    def in_use(self) -> int:
        with self._lock:
            return self._current


# ── throttled HTTP client ────────────────────────────────────────────────────

@dataclass
class ThrottledClient:
    """HTTP client with token-bucket rate limiting + exponential backoff on 429."""

    base_url: str = os.getenv("OLLAMA_URL", "http://127.0.0.1:20128/v1")
    max_concurrent: int = DEFAULT_MAX_CONCURRENT
    rate_per_sec: float = DEFAULT_RATE_PER_SEC
    bucket_size: int = DEFAULT_BUCKET_SIZE
    backoff_base: float = DEFAULT_BACKOFF_BASE
    backoff_max: float = DEFAULT_BACKOFF_MAX
    max_retries: int = DEFAULT_MAX_RETRIES
    timeout: int = 120  # HTTP request timeout in seconds

    # internal state (initialized lazily)
    _bucket: _TokenBucket | None = field(default=None, init=False, repr=False)
    _gate: _ConcurrencyGate | None = field(default=None, init=False, repr=False)
    _stats_lock: threading.Lock = field(default_factory=threading.Lock, init=False, repr=False)
    _stats: dict = field(default_factory=lambda: {
        "total": 0, "success": 0, "retries": 0, "failed": 0, "throttled": 0,
    }, init=False, repr=False)

    def _ensure_init(self):
        if self._bucket is None:
            self._bucket = _TokenBucket(self.rate_per_sec, self.bucket_size)
            self._gate = _ConcurrencyGate(self.max_concurrent)

    def post(self, path: str, json_data: dict | None = None,
             headers: dict | None = None, api_key: str = "") -> dict:
        """POST to base_url + path with throttling + retry.

        Returns the parsed JSON response, or {'error': ..., 'status': ...} on failure.
        """
        self._ensure_init()
        url = self.base_url.rstrip("/") + path
        hdrs = {"Content-Type": "application/json"}
        if api_key:
            hdrs["Authorization"] = f"Bearer {api_key}"
        if headers:
            hdrs.update(headers)

        body = json.dumps(json_data).encode() if json_data else None

        last_error = None
        for attempt in range(self.max_retries + 1):
            # rate limit
            if not self._bucket.acquire(timeout=30):
                with self._stats_lock:
                    self._stats["throttled"] += 1
                log.warning("Throttle: rate limit timeout after 30s")
                return {"error": "rate_limit_timeout", "status": 429}

            # concurrency gate
            if not self._gate.acquire(timeout=60):
                with self._stats_lock:
                    self._stats["throttled"] += 1
                log.warning("Throttle: concurrency gate timeout (max=%d)", self.max_concurrent)
                return {"error": "concurrency_timeout", "status": 503}

            try:
                with self._stats_lock:
                    self._stats["total"] += 1

                req = urllib.request.Request(url, data=body, headers=hdrs, method="POST")
                resp = urllib.request.urlopen(req, timeout=self.timeout)
                data = json.loads(resp.read().decode())

                with self._stats_lock:
                    self._stats["success"] += 1
                return data

            except urllib.error.HTTPError as e:
                if e.code == 429:
                    # rate limited — backoff and retry
                    wait = min(self.backoff_base ** attempt, self.backoff_max)
                    log.warning("429 from %s — retry %d/%d in %.1fs",
                                path, attempt + 1, self.max_retries, wait)
                    with self._stats_lock:
                        self._stats["retries"] += 1
                    time.sleep(wait)
                    last_error = {"error": "rate_limited", "status": 429, "attempt": attempt + 1}
                    continue
                else:
                    # non-retryable HTTP error
                    error_body = ""
                    try:
                        error_body = e.read().decode()[:500]
                    except Exception:
                        pass
                    with self._stats_lock:
                        self._stats["failed"] += 1
                    return {"error": f"http_{e.code}", "status": e.code, "detail": error_body}

            except (urllib.error.URLError, TimeoutError, OSError) as e:
                wait = min(self.backoff_base ** attempt, self.backoff_max)
                log.warning("Network error from %s: %s — retry %d/%d in %.1fs",
                            path, e, attempt + 1, self.max_retries, wait)
                with self._stats_lock:
                    self._stats["retries"] += 1
                time.sleep(wait)
                last_error = {"error": "network_error", "detail": str(e), "attempt": attempt + 1}
                continue

            finally:
                self._gate.release()

        # all retries exhausted
        with self._stats_lock:
            self._stats["failed"] += 1
        return last_error or {"error": "max_retries_exceeded"}

    def stats(self) -> dict:
        """Return copy of request statistics."""
        with self._stats_lock:
            return {**self._stats, "concurrent_in_use": self._gate.in_use if self._gate else 0}


# ── singleton for pipeline use ───────────────────────────────────────────────

_default_client: ThrottledClient | None = None
_default_lock = threading.Lock()


def get_throttled_client(**kwargs) -> ThrottledClient:
    """Get or create the global throttled client (singleton)."""
    global _default_client
    if _default_client is None:
        with _default_lock:
            if _default_client is None:
                _default_client = ThrottledClient(**kwargs)
    return _default_client
