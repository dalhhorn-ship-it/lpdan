#!/usr/bin/env python3
"""Publish a dated snapshot of this project's dashboard on the landing page (public/dashboard/index.html).

  python3 scripts/site_dashboard.py      # rebuild dashboard/index.html, then write the site copy

The copy is the real, unedited dashboard (no JS, CSS radio tabs) plus a bar with a link back to the
landing page and the snapshot date. Numbers are never hand-edited (docs/specs/landing-latest-features.md).
Re-run before a release so the snapshot is not stale.
"""
import os
import re
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "dashboard", "index.html")
DST = os.path.join(ROOT, "public", "dashboard", "index.html")

BAR_CSS = (".site-bar{display:flex;flex-wrap:wrap;gap:4px 16px;align-items:baseline;justify-content:space-between;"
           "max-width:1200px;margin:0 auto;padding:10px 16px;font-size:14px;border-bottom:1px solid var(--border)}"
           ".site-bar a{font-weight:600;color:var(--accent)}.site-bar a:focus-visible{outline:2px solid currentColor;outline-offset:2px}")


def build(html, generated):
    bar = ('<nav class="site-bar" aria-label="Site"><a href="/">&larr; Back to danfactory</a>'
           '<span>Real, unedited snapshot of this landing page\'s own dashboard, generated %s. '
           'The Deploy and Security tabs are in this site\'s dashboard, not yet in the template.</span></nav>'
           % generated)
    html = html.replace("</style>", BAR_CSS + "\n</style>", 1)
    html, n = re.subn(r"<body>", "<body>\n" + bar, html, count=1)
    if n != 1:
        raise SystemExit("site_dashboard: <body> not found in dashboard/index.html")
    return html


def main():
    subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "dashboard.py")], check=True,
                   stdout=subprocess.DEVNULL)
    with open(SRC, encoding="utf-8") as fh:
        html = fh.read()
    m = re.search(r"Generated (\d{4}-\d{2}-\d{2} \d{2}:\d{2})", html)
    generated = (m.group(1) + " UTC") if m else "at an unknown time"
    os.makedirs(os.path.dirname(DST), exist_ok=True)
    with open(DST, "w", encoding="utf-8") as fh:
        fh.write(build(html, generated))
    print("wrote %s (%d bytes, generated %s)" % (os.path.relpath(DST, ROOT), os.path.getsize(DST), generated))


if __name__ == "__main__":
    main()
