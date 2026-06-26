"""Tests for infrastructure modules: throttle, watchdog, reconciler, job_workspace."""
import json
import os
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock


class TestThrottle(unittest.TestCase):
    """Tests for blog.infrastructure.throttle."""

    def test_import(self):
        from blog.infrastructure.throttle import ThrottledClient, get_throttled_client
        self.assertTrue(callable(get_throttled_client))

    def test_token_bucket_acquire(self):
        from blog.infrastructure.throttle import _TokenBucket
        bucket = _TokenBucket(rate=10.0, max_tokens=3)
        # should acquire immediately
        self.assertTrue(bucket.acquire(timeout=1))

    def test_concurrency_gate(self):
        from blog.infrastructure.throttle import _ConcurrencyGate
        gate = _ConcurrencyGate(max_concurrent=2)
        self.assertTrue(gate.acquire(timeout=1))
        self.assertTrue(gate.acquire(timeout=1))
        self.assertEqual(gate.in_use, 2)
        gate.release()
        self.assertEqual(gate.in_use, 1)
        gate.release()
        self.assertEqual(gate.in_use, 0)

    def test_stats(self):
        from blog.infrastructure.throttle import ThrottledClient
        client = ThrottledClient(max_concurrent=1)
        stats = client.stats()
        self.assertEqual(stats["total"], 0)
        self.assertEqual(stats["success"], 0)


class TestWatchdog(unittest.TestCase):
    """Tests for blog.infrastructure.watchdog."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.journal_path = Path(self.tmpdir) / "journal.jsonl"

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _write_entry(self, idea_id, from_s, to_s, ts, metadata=None):
        entry = {
            "timestamp": ts,
            "idea_id": idea_id,
            "from": from_s,
            "to": to_s,
            "by": "test",
        }
        if metadata:
            entry["metadata"] = metadata
        with self.journal_path.open("a") as f:
            f.write(json.dumps(entry) + "\n")

    def test_empty_journal(self):
        from blog.infrastructure.watchdog import PhaseWatchdog
        wd = PhaseWatchdog(self.journal_path)
        stale = wd.check_stale()
        self.assertEqual(stale, [])

    def test_stale_detection(self):
        from blog.infrastructure.watchdog import PhaseWatchdog
        # entry from 2 hours ago with 1h deadline
        old_ts = "2026-06-22T00:00:00+00:00"
        self._write_entry("test-1", "idea", "researching", old_ts,
                          metadata={"started_at": old_ts})
        wd = PhaseWatchdog(self.journal_path, deadlines={"researching": 3600})
        stale = wd.check_stale(now=time.time())  # now is much later
        self.assertEqual(len(stale), 1)
        self.assertEqual(stale[0].idea_id, "test-1")

    def test_healthy_not_stale(self):
        from blog.infrastructure.watchdog import PhaseWatchdog
        from datetime import datetime, timezone
        now_iso = datetime.now(timezone.utc).isoformat()
        self._write_entry("test-2", "idea", "drafted", now_iso,
                          metadata={"started_at": now_iso})
        wd = PhaseWatchdog(self.journal_path, deadlines={"drafted": 3600})
        stale = wd.check_stale()
        self.assertEqual(len(stale), 0)

    def test_mark_failed(self):
        from blog.infrastructure.watchdog import PhaseWatchdog
        wd = PhaseWatchdog(self.journal_path)
        entry = wd.mark_failed("test-3", "drafted", reason="timeout")
        self.assertEqual(entry["by"], "watchdog")
        self.assertTrue(entry["metadata"]["watchdog"])
        # verify it's in the journal
        lines = self.journal_path.read_text().strip().split("\n")
        self.assertEqual(len(lines), 1)

    def test_summary(self):
        from blog.infrastructure.watchdog import PhaseWatchdog
        wd = PhaseWatchdog(self.journal_path)
        s = wd.summary()
        self.assertIn("stale_count", s)
        self.assertIn("deadlines", s)


class TestReconciler(unittest.TestCase):
    """Tests for blog.infrastructure.reconciler."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.journal_path = Path(self.tmpdir) / "journal.jsonl"

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _write_entry(self, idea_id, from_s, to_s, ts):
        entry = {
            "timestamp": ts,
            "idea_id": idea_id,
            "from": from_s,
            "to": to_s,
            "by": "test",
        }
        with self.journal_path.open("a") as f:
            f.write(json.dumps(entry) + "\n")

    def test_empty_journal(self):
        from blog.infrastructure.reconciler import Reconciler
        r = Reconciler(self.journal_path)
        report = r.reconcile(auto_fail=False)
        self.assertEqual(report.total_articles, 0)

    def test_active_articles_detected(self):
        from blog.infrastructure.reconciler import Reconciler
        self._write_entry("art-1", "idea", "researching", "2026-06-22T10:00:00+00:00")
        self._write_entry("art-2", "idea", "drafted", "2026-06-22T11:00:00+00:00")
        r = Reconciler(self.journal_path)
        report = r.reconcile(auto_fail=False)
        self.assertEqual(report.total_articles, 2)
        self.assertEqual(report.active_articles, 2)

    def test_terminal_not_active(self):
        from blog.infrastructure.reconciler import Reconciler
        self._write_entry("art-3", "approved", "published", "2026-06-22T12:00:00+00:00")
        r = Reconciler(self.journal_path)
        report = r.reconcile(auto_fail=False)
        self.assertEqual(report.active_articles, 0)

    def test_summary(self):
        from blog.infrastructure.reconciler import Reconciler
        r = Reconciler(self.journal_path)
        s = r.summary()
        self.assertIn("total_articles", s)


class TestJobWorkspace(unittest.TestCase):
    """Tests for blog.infrastructure.job_workspace."""

    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp())
        self.jw = None

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _make_jw(self, job_id="BLG-TEST"):
        from blog.infrastructure.job_workspace import JobWorkspace
        self.jw = JobWorkspace(self.tmpdir, job_id)
        return self.jw

    def test_creates_directories(self):
        jw = self._make_jw()
        self.assertTrue(jw.research_dir.is_dir())
        self.assertTrue(jw.drafts_dir.is_dir())

    def test_state_persist(self):
        from blog.infrastructure.job_workspace import JobState
        jw = self._make_jw()
        state = jw.create_state("Test Topic", "test-topic")
        self.assertEqual(state.job_id, "BLG-TEST")
        # reload
        loaded = jw.load_state()
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded.topic, "Test Topic")

    def test_idempotency(self):
        from blog.infrastructure.job_workspace import JobState
        jw = self._make_jw()
        state = jw.create_state("T", "t")
        self.assertTrue(jw.add_event(state, "t:research:complete"))
        self.assertFalse(jw.add_event(state, "t:research:complete"))  # duplicate

    def test_transition(self):
        from blog.infrastructure.job_workspace import JobState
        jw = self._make_jw()
        state = jw.create_state("T", "t")
        self.assertTrue(jw.transition(state, "research"))
        self.assertEqual(state.current_phase, "research")
        self.assertFalse(jw.transition(state, "brief"))  # can't go back

    def test_draft_read_write(self):
        jw = self._make_jw()
        content = "---\ntitle: test\n---\n\nHello world"
        jw.write_draft("test-article", content)
        self.assertTrue(jw.draft_exists("test-article"))
        draft = jw.load_draft("test-article")
        self.assertIsNotNone(draft)
        self.assertEqual(draft.body.strip(), "Hello world")

    def test_research_read_write(self):
        jw = self._make_jw()
        jw.write_research("test-idea", "# Research Brief\n- keyword: test")
        content = jw.read_research("test-idea")
        self.assertIn("Research Brief", content)


if __name__ == "__main__":
    unittest.main()
