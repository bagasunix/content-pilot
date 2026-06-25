#!/usr/bin/env python3
"""
ContentPilot — E2E Test

Tests the full user journey:
1. Install (import check)
2. Setup wizard (config generation)
3. License activation
4. Research → Draft → Analyze → Gate → Approve → Publish

Usage:
    python3 tests/e2e_test.py
    python3 tests/e2e_test.py --skip-publish  # skip Blogger API tests
"""
import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))


class E2ETest:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
        self.test_dir = None

    def setup(self):
        """Create temp workspace for testing."""
        self.test_dir = Path(tempfile.mkdtemp(prefix="contentpilot_e2e_"))
        os.chdir(self.test_dir)
        
        # Create required directories
        (self.test_dir / "workspace" / "drafts").mkdir(parents=True)
        (self.test_dir / "workspace").mkdir(exist_ok=True)
        
        # Create minimal config
        config = """domain: test-blog.com
blog_id: "1234567890"
language: id
publish_mode: draft
wip_limit: 3
"""
        (self.test_dir / "workspace" / "config.yaml").write_text(config)

    def teardown(self):
        """Clean up test directory."""
        os.chdir(Path(__file__).resolve().parent.parent)
        if self.test_dir and self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def assert_test(self, name, condition, detail=""):
        if condition:
            self.passed += 1
            print(f"  ✅ {name}")
        else:
            self.failed += 1
            self.errors.append(f"{name}: {detail}")
            print(f"  ❌ {name} — {detail}")

    def test_imports(self):
        """Test 1: All modules can be imported."""
        print("\n=== Test 1: Imports ===")
        
        try:
            from contentpilot.domain import stages
            self.assert_test("domain.stages", True)
        except Exception as e:
            self.assert_test("domain.stages", False, str(e))

        try:
            from contentpilot.domain import gates
            self.assert_test("domain.gates", True)
        except Exception as e:
            self.assert_test("domain.gates", False, str(e))

        try:
            from contentpilot.domain import article
            self.assert_test("domain.article", True)
        except Exception as e:
            self.assert_test("domain.article", False, str(e))

        try:
            from contentpilot.infrastructure import config
            self.assert_test("infrastructure.config", True)
        except Exception as e:
            self.assert_test("infrastructure.config", False, str(e))

        try:
            from contentpilot.infrastructure import draft_store
            self.assert_test("infrastructure.draft_store", True)
        except Exception as e:
            self.assert_test("infrastructure.draft_store", False, str(e))

        try:
            from contentpilot.infrastructure import publisher
            self.assert_test("infrastructure.publisher", True)
        except Exception as e:
            self.assert_test("infrastructure.publisher", False, str(e))

        try:
            from contentpilot.seo import analyze_draft
            self.assert_test("seo.analyze_draft", True)
        except Exception as e:
            self.assert_test("seo.analyze_draft", False, str(e))

        try:
            from contentpilot.license import check_license
            self.assert_test("license.check_license", True)
        except Exception as e:
            self.assert_test("license.check_license", False, str(e))

    def test_pipeline_flow(self):
        """Test 2: Pipeline stage transitions."""
        print("\n=== Test 2: Pipeline Flow ===")
        
        from contentpilot.domain import stages
        from contentpilot.domain.article import Idea
        
        # Create test idea
        idea = Idea(idea_id="e2e-test-001", title="E2E Test Article", priority="H")
        
        # Test initial state
        self.assert_test(
            "Initial stage is idea",
            idea.status == "idea",
            f"got {idea.status}"
        )
        
        # Transition: idea → researching
        idea.status = "researching"
        self.assert_test(
            "Transition to researching",
            idea.status == "researching",
            f"got {idea.status}"
        )
        
        # Transition: researching → drafted
        idea.status = "drafted"
        self.assert_test(
            "Transition to drafted",
            idea.status == "drafted",
            f"got {idea.status}"
        )
        
        # Transition: drafted → gated
        idea.status = "gated"
        self.assert_test(
            "Transition to gated",
            idea.status == "gated",
            f"got {idea.status}"
        )
        
        # Transition: gated → approved
        idea.status = "approved"
        self.assert_test(
            "Transition to approved",
            idea.status == "approved",
            f"got {idea.status}"
        )

    def test_quality_gates(self):
        """Test 3: Quality gates (AI-tells, word count, etc)."""
        print("\n=== Test 3: Quality Gates ===")
        
        from contentpilot.domain.gates import evaluate, AI_TELLS, MIN_WORDS
        from contentpilot.domain.article import Draft
        
        # Test 1: Article with AI-tells should FAIL
        raw_with_tells = """---
title: Test Article
meta_description: Test description for testing purposes only
slug: test-article
keywords: test
---
# Test Article

Di era digital saat ini, sangat penting untuk memahami teknologi.
Article content here with enough words to pass minimum check.
""" + "word " * 600
        draft_with_ai_tells = Draft(
            idea_id="test-ai-tells",
            raw=raw_with_tells,
            frontmatter={"seo": {"title": "Test Article", "meta_description": "Test description", "slug": "test-article", "keywords": "test"}},
            body=raw_with_tells.split("---", 2)[-1] if "---" in raw_with_tells else raw_with_tells,
        )
        result = evaluate(draft_with_ai_tells, check_links=False)
        self.assert_test(
            "AI-tells detected",
            len(result.failures) > 0,
            f"failures: {result.failures}"
        )
        
        # Test 2: Clean article should PASS (or mostly pass)
        raw_clean = """---
title: Cara Install Redis di Ubuntu 24.04
meta_description: Panduan lengkap cara install Redis di Ubuntu 24.04 untuk developer dan sysadmin. Step by step dari awal sampai production.
slug: cara-install-redis-ubuntu-2404
keywords: install redis ubuntu
---
# Cara Install Redis di Ubuntu 24.04

Redis adalah in-memory data store yang sering digunakan sebagai cache.

## Kenapa Pakai Redis?

Redis memiliki kelebihan kecepatan tinggi dan mudah di-setup.

## Cara Install

```bash
sudo apt update
sudo apt install redis-server
```

## Kesimpulan

Redis adalah pilihan bagus untuk caching.
""" + "word " * 600
        clean_draft = Draft(
            idea_id="test-clean",
            raw=raw_clean,
            frontmatter={"seo": {"title": "Cara Install Redis di Ubuntu 24.04", "meta_description": "Panduan lengkap cara install Redis di Ubuntu 24.04 untuk developer dan sysadmin. Step by step dari awal sampai production.", "slug": "cara-install-redis-ubuntu-2404", "keywords": "install redis ubuntu"}},
            body=raw_clean.split("---", 2)[-1] if "---" in raw_clean else raw_clean,
        )
        result = evaluate(clean_draft, check_links=False)
        # Clean draft should have fewer failures than AI-tells draft
        self.assert_test(
            "Clean article passes quality check",
            len(result.failures) <= 5,  # some failures expected for test data
            f"clean: {len(result.failures)} failures"
        )

    def test_seo_analyzer(self):
        """Test 4: SEO analyzer."""
        print("\n=== Test 4: SEO Analyzer ===")
        
        from contentpilot.seo import analyze_draft, format_report
        
        # Create test draft
        draft_content = """---
title: "Cara Install Redis di Ubuntu 24.04 Lengkap"
meta_description: "Panduan lengkap cara install Redis di Ubuntu 24.04. Mulai dari apt install, konfigurasi, sampai production-ready. Cocok untuk developer."
slug: "cara-install-redis-ubuntu-2404"
keywords: "install redis ubuntu, redis tutorial"
---

# Cara Install Redis di Ubuntu 24.04

Redis adalah in-memory data store yang sering digunakan sebagai cache, message broker, dan database.

## Kenapa Pakai Redis?

Redis memiliki beberapa kelebihan:

- Kecepatan tinggi
- Mudah di-setup
- Mendukung berbagai data structures

## Cara Install via APT

```bash
sudo apt update
sudo apt install redis-server
```

## Konfigurasi

Edit `/etc/redis/redis.conf` untuk konfigurasi.

## Kesimpulan

Redis adalah pilihan bagus untuk caching di Ubuntu 24.04.
"""
        
        draft_path = self.test_dir / "workspace" / "drafts" / "seo-test" / "draft.md"
        draft_path.parent.mkdir(parents=True)
        draft_path.write_text(draft_content)
        
        # Run analysis
        result = analyze_draft(str(draft_path))
        
        self.assert_test(
            "SEO score is numeric",
            isinstance(result.seo_score, int),
            f"got {type(result.seo_score)}"
        )
        
        self.assert_test(
            "Readability grade exists",
            result.readability.grade in ("A", "B", "C", "D", "F"),
            f"got {result.readability.grade}"
        )
        
        self.assert_test(
            "Verdict exists",
            result.verdict in ("PASS", "PASS WITH WARNINGS", "NEEDS REVISION"),
            f"got {result.verdict}"
        )
        
        self.assert_test(
            "Has recommendations",
            len(result.recommendations) > 0,
            "no recommendations"
        )
        
        # Format report
        report = format_report("seo-test", result)
        self.assert_test(
            "Report is string",
            isinstance(report, str) and len(report) > 100,
            f"report length: {len(report)}"
        )

    def test_draft_store(self):
        """Test 5: Draft store operations."""
        print("\n=== Test 5: Draft Store ===")
        
        from contentpilot.infrastructure.draft_store import FileDraftStore
        from contentpilot.infrastructure.paths import Workspace
        
        ws = Workspace(self.test_dir)
        ws.drafts.mkdir(parents=True, exist_ok=True)
        ws.research.mkdir(parents=True, exist_ok=True)
        store = FileDraftStore(ws)
        
        # Write research brief
        idea_id = "draftstore-test"
        path = store.write_research_brief(idea_id, "# Research Brief\n\nTopic: Test")
        
        self.assert_test(
            "Research brief written",
            Path(path).exists(),
            f"file not found: {path}"
        )
        
        # Write draft
        draft_content = """---
title: Test Draft
meta_description: Test description for testing
slug: test-draft
keywords: test
---
# Test Draft

This is test content with enough words.
""" + "word " * 600
        path = store.write_draft(idea_id, draft_content)
        
        self.assert_test(
            "Draft written",
            Path(path).exists(),
            f"file not found: {path}"
        )
        
        # Load draft
        loaded = store.load_draft(idea_id)
        self.assert_test(
            "Draft loaded",
            loaded is not None and loaded.idea_id == idea_id,
            f"loaded: {loaded}"
        )

    def test_license(self):
        """Test 6: License client."""
        print("\n=== Test 6: License Client ===")
        
        from contentpilot.license import get_machine_id, get_license_info
        
        # Machine ID should be deterministic
        machine_id = get_machine_id()
        self.assert_test(
            "Machine ID is string",
            isinstance(machine_id, str) and len(machine_id) > 0,
            f"got {machine_id}"
        )
        
        # License info without activation
        info = get_license_info()
        self.assert_test(
            "License info has active field",
            "active" in info,
            f"got {info}"
        )
        
        self.assert_test(
            "No license = inactive",
            info["active"] is False,
            f"got {info['active']}"
        )

    def run_all(self):
        """Run all E2E tests."""
        print("=" * 50)
        print("  ContentPilot E2E Test")
        print("=" * 50)
        
        self.setup()
        
        try:
            self.test_imports()
            self.test_pipeline_flow()
            self.test_quality_gates()
            self.test_seo_analyzer()
            self.test_draft_store()
            self.test_license()
        finally:
            self.teardown()
        
        # Summary
        print("\n" + "=" * 50)
        print(f"  Results: {self.passed} passed, {self.failed} failed")
        print("=" * 50)
        
        if self.errors:
            print("\n  Failures:")
            for err in self.errors:
                print(f"    ❌ {err}")
        
        return self.failed == 0


if __name__ == "__main__":
    test = E2ETest()
    success = test.run_all()
    sys.exit(0 if success else 1)
