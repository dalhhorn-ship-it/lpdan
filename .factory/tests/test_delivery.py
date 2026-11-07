"""Delivery tab: CI metrics, changelog and release parsing, deploy dates, open decisions, empty state."""
import datetime
import json
import os
import sys
import tempfile
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from obs import tab_delivery as D  # noqa: E402

TODAY = datetime.date(2026, 11, 6)  # Friday, ISO week 45


def run_row(i, day, concl, branch="feature", minutes=5):
    start = "2026-11-%02dT10:00:00Z" % day
    return {"id": i, "head_branch": branch, "conclusion": concl, "created_at": start, "run_started_at": start,
            "updated_at": "2026-11-%02dT10:%02d:00Z" % (day, minutes), "html_url": "https://example.test/%d" % i}


def write(root, rel, text):
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


class Delivery(unittest.TestCase):
    def test_ci_metrics(self):
        runs = [run_row(1, 6, "success", "main", 2), run_row(2, 5, "failure", "main", 4), run_row(3, 5, "cancelled"),
                run_row(4, 4, "skipped", minutes=0), run_row(5, 3, "success", minutes=6), run_row(6, 2, "failure", minutes=8)]
        m = D.ci_metrics(runs, TODAY, "main")
        self.assertEqual((m["runs"], m["decided_30"], m["pass_rate_30"], m["main_pass_rate"]), (6, 4, 50, 50))
        self.assertEqual((m["median_min"], m["p90_min"]), (5.0, 8.0))
        self.assertEqual(m["last_main_failure"]["url"], "https://example.test/2")
        self.assertEqual((m["weeks"][-1], len(m["weeks"]), m["runs_per_week"][-1], m["runs_per_week"][-2]), ("2026-W45", 8, 6, 0))
        self.assertEqual((m["pass_per_week"][-1], m["pass_per_week"][-2]), (50, None))
        text = '{"source": "x", "runs": [%s]}' % ",".join(json.dumps(r) for r in runs)
        self.assertEqual(len(D.parse_ci_runs(text)), 6)
        self.assertIsNone(D.parse_ci_runs("not json"))
        self.assertIsNone(D.ci_metrics(None, TODAY))
        self.assertIsNone(D.ci_metrics(["junk"], TODAY))
        out = D.bars(m["pass_per_week"], m["weeks"], "CI pass rate", "%")
        self.assertIn("<svg", out)
        self.assertIn("no data", out)

    def test_deploy_metrics(self):
        dep = D.deploy_metrics(["2026-11-06", "2026-11-02T09:00:00+00:00", "2026-10-26", "bad"], TODAY)
        self.assertEqual((dep["total"], dep["last"], dep["per_week"][-1], dep["per_week"][-2]), (3, "2026-11-06", 2, 1))
        self.assertIsNone(D.deploy_metrics([], TODAY))

    def test_changelog_and_release_metrics(self):
        cl = D.parse_changelog("# Changelog\n\n## [Unreleased]\n\n* a\n- b\n\n## [0.4.0] - 2026-10-24\n\n- old\n\n"
                               "## 0.3.0 (2026-10-22)\n\n## 0.2.0 (2026-10-19)\n\n## 0.1.0 (2026-10-19)\n")
        self.assertEqual((cl["latest"], cl["latest_date"], cl["unreleased"]), ("0.4.0", "2026-10-24", 2))
        rel = D.release_metrics(cl["releases"], TODAY)
        self.assertEqual((rel["count"], rel["median_gap_days"], rel["days_since_last"], rel["last"]), (4, 2, 13, "0.4.0"))
        self.assertIsNone(D.release_metrics([], TODAY))
        self.assertIsNone(D.parse_changelog("")["unreleased"])

    def test_empty_state_is_calm(self):
        root = tempfile.mkdtemp()
        d = D.collect(root, {}, TODAY)
        self.assertEqual(d["decisions"], {"total": 0, "open": []})
        page = D.render(d)
        self.assertIn("Not enough data yet", page)
        self.assertNotIn("None", page)
        self.assertNotIn("None", D.line(d))
        self.assertNotIn("None", D.delivery_html(d))

    def test_collect_with_data_and_open_decisions(self):
        root = tempfile.mkdtemp()
        write(root, "metrics/ci-runs.json", json.dumps({"runs": [run_row(1, 6, "success", "main", 2)]}))
        write(root, "metrics/history.jsonl", json.dumps({"ts": "2026-11-05T10:00:00+00:00", "kind": "deploy"}) + "\nnot json\n")
        write(root, "CHANGELOG.md", "## [Unreleased]\n- x\n## 1.0.0 (2026-10-01)\n")
        write(root, "docs/decisions/0000-template.md", "# t\n> Status: proposed\n")
        write(root, "docs/decisions/0001-db.md", "# 0001 — Pick a DB\n> Status: proposed · Date: 2026-11-01\n")
        write(root, "docs/decisions/0002-x.md", "# 0002 — X\n> Status: accepted\n")
        d = D.collect(root, {}, TODAY)
        self.assertEqual((d["ci"]["pass_rate_30"], d["deploys"]["total"], d["releases"]["count"]), (100, 1, 1))
        self.assertEqual([a["num"] for a in d["decisions"]["open"]], ["0001"])
        self.assertEqual(D.line(d), "CI 100% (last 1), 1 deploys, 1 releases, 36 days since last, 1 open decisions")
        page = D.render(d)
        for needle in ("Delivery", "Open decisions", "Pick a DB", "<svg", "Since last release"):
            self.assertIn(needle, page)
        self.assertNotIn("<script", page)

    def test_escaping(self):
        d = D.collect(tempfile.mkdtemp(), {}, TODAY)
        d["decisions"] = {"total": 1, "open": [{"num": "0001", "title": "<script>alert(1)</script>"}]}
        page = D.render(d)
        self.assertNotIn("<script>", page)
        self.assertIn("&lt;script&gt;", page)

    def test_ci_runs_script(self):
        sys.path.insert(0, os.path.join(ROOT, "scripts"))
        import ci_runs
        self.assertEqual(ci_runs.parse_repo("https://github.com/acme/app.git"), "acme/app")
        self.assertEqual(ci_runs.parse_repo("git@github.com:acme/app.git"), "acme/app")
        self.assertEqual(ci_runs.parse_repo(""), "")
        path = os.path.join(tempfile.mkdtemp(), "ci-runs.json")
        n = ci_runs.write([run_row(1, 5, "success"), dict(run_row(2, 6, "failure"), extra="dropped")], "test", path)
        with open(path, encoding="utf-8") as fh:
            runs = D.parse_ci_runs(fh.read())
        self.assertEqual((n, [r["id"] for r in runs]), (2, [2, 1]))
        self.assertNotIn("extra", runs[0])


if __name__ == "__main__":
    unittest.main()
