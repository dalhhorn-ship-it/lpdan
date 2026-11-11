"""scripts/site_dashboard.py: the public snapshot must never show open security items (PRD template-update-2026-11 AC 7, 8)."""
import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
if not os.path.isfile(os.path.join(ROOT, "scripts", "site_dashboard.py")):
    raise unittest.SkipTest("no public dashboard snapshot in this tree")
import copy  # noqa: E402

import dashboard  # noqa: E402
import site_dashboard as SD  # noqa: E402
from obs import roadmap_data  # noqa: E402

BACKLOG = """# Backlog
## Milestone: M1 — First (target: 2026-12-15)
- [ ] SEC-1 Rotate the leaked deploy token (S) #infra
- [ ] AAA-1 Ordinary open work (M) #feature
- [x] AAA-2 Ordinary done work (S) #feature
## Milestone: M2 — Next (release: v0.3)
- [ ] Harden security headers (S)
- [ ] AAA-3 Ordinary later work (S)
"""
GANTT_PANEL = 'class="rv rv-gantt"'


def data_with_open_sec():
    d = dashboard.collect()
    ms = dashboard.parse_backlog(BACKLOG)
    d["roadmap"] = dashboard.roadmap(ms, [])
    d["roadmap_views"] = roadmap_data.collect(ROOT, ms, None)
    d["backlog"]["next"] = ["SEC-1 Rotate the leaked deploy token", "AAA-1 Ordinary open work"]
    return d


class PublicFilter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.src = data_with_open_sec()
        cls.raw = dashboard.render(copy.deepcopy(cls.src))
        cls.pub = dashboard.render(SD.public(copy.deepcopy(cls.src)))

    def test_control_unfiltered_gantt_shows_the_item(self):
        # proves the test below would catch a leak: without the filter the Gantt carries SEC-1
        gantt = self.raw[self.raw.index(GANTT_PANEL):]
        self.assertIn("SEC-1", gantt.split("</svg>")[0] + gantt)

    def test_open_sec_item_absent_from_every_view(self):
        self.assertNotIn("SEC-1", self.pub)
        self.assertNotIn("Rotate the leaked deploy token", self.pub)
        self.assertNotIn("security headers", self.pub)
        gantt = self.pub[self.pub.index(GANTT_PANEL):]
        self.assertNotIn("SEC-1", gantt)

    def test_ordinary_items_stay(self):
        self.assertIn("Ordinary open work", self.pub)
        self.assertIn("Ordinary later work", self.pub)

    def test_done_items_stay(self):
        self.assertIn("Ordinary done work", self.pub)

    def test_scrub_covers_nested_lists_of_strings(self):
        out = SD.scrub({"x": {"covers": ["PROC-1", "SEC-3"], "rows": [{"t": "keep"}, {"t": "SEC-9 drop"}]}})
        self.assertEqual(out, {"x": {"covers": ["PROC-1"], "rows": [{"t": "keep"}]}})


class Leaks(unittest.TestCase):
    SEC = {"records": [{"id": "SEC-7", "title": "Token in logs", "state": "open"},
                       {"id": "SEC-8", "title": "Old finding", "state": "fixed"}]}

    def test_leak_detected_by_id_and_title(self):
        self.assertEqual(SD.leaks("<p>see SEC-7</p>", self.SEC), ["SEC-7"])
        self.assertEqual(SD.leaks("<p>Token in logs</p>", self.SEC), ["SEC-7"])

    def test_fixed_findings_may_show(self):
        self.assertEqual(SD.leaks("<p>SEC-8 Old finding</p>", self.SEC), [])

    def test_clean_page(self):
        self.assertEqual(SD.leaks("<p>nothing</p>", self.SEC), [])


if __name__ == "__main__":
    unittest.main()
