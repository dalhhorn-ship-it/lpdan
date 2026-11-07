#!/usr/bin/env python3
"""Publish a dated snapshot of this project's dashboard on the landing page (public/dashboard/index.html).

  python3 scripts/site_dashboard.py      # rebuild dashboard/index.html, then write the site copy

The copy is the real dashboard (no JS, CSS radio tabs) plus a bar with a link back to the landing page and
the snapshot date. Numbers are never hand-edited (docs/specs/landing-latest-features.md). One deliberate
filter (Dan, 2026-11-07): new or open security issues are not published. The Security tab keeps only findings
that are fixed or accepted, without hardening notes or audit limits, and open tech-debt items and roadmap cards
that name a finding (SEC-n) or security are left out. The private dashboard (dashboard/index.html) keeps all.
Re-run before a release so the snapshot is not stale.
"""
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "dashboard", "index.html")
DST = os.path.join(ROOT, "public", "dashboard", "index.html")

BAR_CSS = (".site-bar{display:flex;flex-wrap:wrap;gap:4px 16px;align-items:baseline;justify-content:space-between;"
           "max-width:1200px;margin:0 auto;padding:10px 16px;font-size:14px;border-bottom:1px solid var(--border)}"
           ".site-bar a{font-weight:600;color:var(--text);text-decoration:underline}.site-bar a:focus-visible{outline:2px solid currentColor;outline-offset:2px}")


def build(html, generated):
    bar = ('<nav class="site-bar" aria-label="Site"><a href="/">&larr; Back to danfactory</a>'
           '<span>Real snapshot of this landing page\'s own dashboard, generated %s. '
           'Deploy and Security are this site\'s own tabs; the observability tabs come from a danfactory branch not yet merged into the template. Open security issues are not published here.</span></nav>'
           % generated)
    html = html.replace("</style>", BAR_CSS + "\n</style>", 1)
    head = ('<meta name="description" content="Real snapshot of the danfactory landing page\'s own project dashboard: '
            'progress, roadmap, deploys and security.">\n<link rel="icon" href="/favicon.svg" type="image/svg+xml">\n')
    html = html.replace("</head>", head + "</head>", 1)
    html, n = re.subn(r"<body>", "<body>\n" + bar, html, count=1)
    if n != 1:
        raise SystemExit("site_dashboard: <body> not found in dashboard/index.html")
    return html


CLOSED = ("fixed", "accepted")
SECURITY_WORDS = re.compile(r"\bSEC-\d+|secur", re.I)


def public_security(sec):
    """Only closed findings; no hardening notes or limits (they describe what is still open)."""
    if not sec:
        return sec
    sec = dict(sec)
    sec["records"] = [r for r in sec.get("records", []) if r.get("state", "open") in CLOSED]
    sec["hardening"] = []
    sec["limits"] = ["Public copy: new or open findings, hardening notes and audit limits are not shown here."]
    return sec


def public(d):
    d["security"] = public_security(d.get("security"))
    debt = d.get("debt") or {}
    if isinstance(debt.get("open"), list):
        debt["open"] = [x for x in debt["open"] if not SECURITY_WORDS.search(" ".join(
            str(x.get(k, "")) for k in ("id", "title", "area")))]
        if isinstance(debt.get("by_impact"), dict):
            debt["by_impact"] = {k: sum(1 for x in debt["open"] if x.get("impact") == k) for k in debt["by_impact"]}
    for col in (d.get("roadmap") or {}).get("columns", []):
        for lane, cards in col.get("lanes", {}).items():
            col["lanes"][lane] = [c for c in cards if c.get("state") == "done" or not SECURITY_WORDS.search(c.get("title", ""))]
    rm = d.get("roadmap") or {}
    rm["next"] = [x for x in rm.get("next", []) if not SECURITY_WORDS.search(x.get("title", ""))]
    return d


def leaks(html, sec):
    """Open findings (id or title) that still appear anywhere in the page, e.g. via another tab."""
    opened = [r for r in (sec or {}).get("records", []) if r.get("state", "open") not in CLOSED]
    return [r.get("id") for r in opened if (r.get("id") and r["id"] in html) or (r.get("title") and r["title"] in html)]


def main():
    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    import dashboard
    dashboard.build()  # the private, complete dashboard/ stays current too
    d = public(dashboard.collect())
    full_sec = dashboard.security()
    html = dashboard.render(d)
    bad = leaks(html, full_sec)
    if bad:
        raise SystemExit("site_dashboard: open security findings would be published: %s" % ", ".join(bad))
    m = re.search(r"Generated (\d{4}-\d{2}-\d{2} \d{2}:\d{2})", html)
    generated = (m.group(1) + " UTC") if m else "at an unknown time"
    os.makedirs(os.path.dirname(DST), exist_ok=True)
    with open(DST, "w", encoding="utf-8") as fh:
        fh.write(build(html, generated))
    print("wrote %s (%d bytes, generated %s)" % (os.path.relpath(DST, ROOT), os.path.getsize(DST), generated))


if __name__ == "__main__":
    main()
