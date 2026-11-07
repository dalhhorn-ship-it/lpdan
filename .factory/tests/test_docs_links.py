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


if __name__ == "__main__":
    unittest.main()
