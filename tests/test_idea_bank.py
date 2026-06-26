"""Idea-bank markdown parser (infrastructure)."""
import tempfile
import unittest
from pathlib import Path

from blog.infrastructure.idea_bank import MarkdownIdeaBank
from blog.infrastructure.paths import Workspace

SAMPLE = """# Idea Bank

## High

### [H] (CONTOH — hapus) Topik contoh
- idea_id:        contoh-skip
- angle/pengalaman: harus dilewati

### [H] Docker Compose untuk Pemula
- idea_id:        docker-compose-untuk-pemula
- keyword target: docker compose, compose vs run
- kategori:       Tutorials
- sumber:         riset
- angle/pengalaman: lanjutan dari artikel install Docker
- status:         idea

## Medium

### [M] SSH Key Setup
- idea_id:        ssh-key-setup
- keyword target: ssh key
- kategori:       Tutorials
- angle/pengalaman:
- status:         idea
"""


class TestIdeaBank(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        ws = Workspace(Path(self.tmp.name))
        ws.idea_bank.write_text(SAMPLE)
        self.bank = MarkdownIdeaBank(ws)

    def tearDown(self):
        self.tmp.cleanup()

    def test_skips_examples_and_parses_fields(self):
        ideas = self.bank.list_ideas()
        ids = [i.idea_id for i in ideas]
        self.assertNotIn("contoh-skip", ids)
        self.assertEqual(ids, ["docker-compose-untuk-pemula", "ssh-key-setup"])

        docker = ideas[0]
        self.assertEqual(docker.priority, "H")
        self.assertEqual(docker.category, "Tutorials")
        self.assertIn("compose", docker.keyword)
        self.assertTrue(docker.has_angle)

    def test_missing_angle_detected(self):
        ssh = [i for i in self.bank.list_ideas() if i.idea_id == "ssh-key-setup"][0]
        self.assertFalse(ssh.has_angle)

    def test_priority_rank_ordering(self):
        ideas = sorted(self.bank.list_ideas(), key=lambda i: i.priority_rank)
        self.assertEqual(ideas[0].priority, "H")


if __name__ == "__main__":
    unittest.main()
