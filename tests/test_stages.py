"""Domain stage helpers."""
import unittest

from blog.domain import stages


class TestStages(unittest.TestCase):
    def test_wip_stages_are_in_flight(self):
        for s in (stages.RESEARCHING, stages.DRAFTED, stages.GATED, stages.APPROVED):
            self.assertTrue(stages.counts_as_wip(s))

    def test_terminal_stages_not_wip(self):
        self.assertFalse(stages.counts_as_wip(stages.PUBLISHED))
        self.assertFalse(stages.counts_as_wip(stages.PUBLISHED))
        self.assertFalse(stages.counts_as_wip(stages.IDEA))
        self.assertFalse(stages.counts_as_wip(None))

    def test_wip_limit(self):
        self.assertEqual(stages.WIP_LIMIT, 3)


if __name__ == "__main__":
    unittest.main()
