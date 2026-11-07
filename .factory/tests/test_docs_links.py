"""Doc-graph links: bare .md paths count as edges; the generated INDEX never rescues an orphan."""
import json
import os
import sys
import tempfile
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import docs_index  # noqa: E402
from obs import tab_docs  # noqa: E402


class Links(unittest.TestCase):
    def targets(self, line):
        return [m.group(1) or m.group(3) or m.group(4) for m in docs_index.LINK_RE.finditer(line)]

    def test_bare_paths_are_links(self):
        self.assertEqual(self.targets("see (docs/policies/security.md) and paths/x.md."),
                         ["docs/policies/security.md", "paths/x.md"])
        self.assertEqual(self.targets("[a](b.md) and `docs/c.md`"), ["b.md", "docs/c.md"])
        self.assertEqual(self.targets("https://x.org/y.md and README.mdx"), [])

    def test_real_repo_parse_resolves_bare_relative_path(self):
        doc = docs_index.parse(os.path.join(ROOT, "docs", "OPERATING-MODEL.md"))
        self.assertIn("docs/policies/testing-and-metrics.md", doc["links"])

    def test_index_edges_do_not_count(self):
        d = tempfile.mkdtemp()
        os.makedirs(os.path.join(d, "docs"))
        g = {"nodes": [{"id": "docs/INDEX.md"}, {"id": "docs/a.md"}, {"id": "docs/b.md"}, {"id": "docs/c.md"}],
             "edges": [{"from": "docs/INDEX.md", "to": "docs/a.md"}, {"from": "docs/b.md", "to": "docs/c.md"}]}
        with open(os.path.join(d, "docs", "knowledge-graph.json"), "w") as fh:
            json.dump(g, fh)
        out = tab_docs.collect(d, {})
        self.assertEqual(out["orphans"], ["docs/a.md"])


INDEX_FIRST = ("developer", "reviewer", "product-manager", "code-writer", "data-builder", "spreadsheet-architect",
               "bulk-reader")  # docs/specs/agents-index-first.md; test-runner/deploy-watcher read logs, not docs


class IndexFirst(unittest.TestCase):
    G = {"nodes": [{"id": "docs/a.md", "title": "A", "summary": "about a"}, {"id": "docs/b.md", "title": "B", "summary": "about b"},
                   {"id": "docs/c.md", "title": "C"}, {"id": "docs/lone.md", "title": "Lone"}],
         "edges": [{"from": "docs/a.md", "to": "docs/b.md"}, {"from": "docs/c.md", "to": "docs/a.md"},
                   {"from": "docs/b.md", "to": "docs/c.md"}]}

    def test_agents_point_at_the_index(self):  # AC1
        for a in INDEX_FIRST:
            with open(os.path.join(ROOT, ".claude", "agents", a + ".md"), encoding="utf-8") as fh:
                self.assertIn("docs/INDEX.md", fh.read(), a)

    def test_related_lists_exact_neighbours_with_summaries(self):  # AC2
        self.assertEqual(docs_index.related(self.G, "docs/a.md"),
                         [("from", "docs/c.md", "C"), ("to", "docs/b.md", "about b")])

    def test_related_no_edges_and_unknown(self):  # AC3, AC4 (pure part)
        self.assertEqual(docs_index.related(self.G, "docs/lone.md"), [])
        self.assertIsNone(docs_index.related(self.G, "docs/nope.md"))

    def run_cli(self, *args):
        import subprocess
        return subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "docs_index.py"), *args],
                              cwd=ROOT, capture_output=True, text=True)

    def test_cli_unknown_doc_exits_nonzero(self):  # AC4
        r = self.run_cli("--related", "docs/does-not-exist.md")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("not a doc", r.stdout)

    def test_cli_real_doc_and_stale_warning(self):  # AC2 on the repo, AC5
        r = self.run_cli("--related", "docs/policies/token-economy.md")
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("<- CLAUDE.md", r.stdout)
        self.assertNotIn("stale", r.stdout)  # the committed graph is current (check.sh enforces it)
        graph = os.path.join(ROOT, "docs", "knowledge-graph.json")
        with open(graph, encoding="utf-8") as fh:
            keep = fh.read()
        try:
            with open(graph, "w", encoding="utf-8") as fh:
                fh.write(keep.replace('"lines": ', '"lines": 1', 1))
            self.assertIn("stale", self.run_cli("--related", "docs/policies/token-economy.md").stdout)
        finally:
            with open(graph, "w", encoding="utf-8") as fh:
                fh.write(keep)

    def test_token_economy_mentions_related(self):  # AC6
        with open(os.path.join(ROOT, "docs", "policies", "token-economy.md"), encoding="utf-8") as fh:
            self.assertIn("docs_index.py --related", fh.read())


if __name__ == "__main__":
    unittest.main()
