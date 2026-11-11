#!/usr/bin/env python3
"""Publish a dated snapshot of this project's dashboard on the landing page (public/dashboard/index.html).

  python3 scripts/site_dashboard.py      # rebuild dashboard/index.html, then write the site copy

The copy is the real dashboard (no JS, CSS radio tabs) plus a bar with a link back to the landing page and
the snapshot date. Numbers are never hand-edited (docs/specs/landing-latest-features.md). One deliberate
filter (Dan, 2026-11-07): new or open security issues are not published. The Security tab keeps only findings
that are fixed or accepted, without hardening notes or audit limits, and open tech-debt items and roadmap cards
that name a finding (SEC-n) or security are left out of the data before any view renders (public(d), scrub()). The private dashboard (dashboard/index.html) keeps all.
Re-run before a release so the snapshot is not stale.
"""
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "dashboard", "index.html")
DST = os.path.join(ROOT, "public", "dashboard", "index.html")

BAR_CSS = (".site-bar{display:flex;flex-wrap:wrap;gap:4px 16px;align-items:baseline;justify-content:space-between;"
           "max-width:1200px;margin:0 auto;padding:10px 16px;font-size:14px;border-bottom:1px solid var(--border-subtle-01)}"
           ".site-bar a{font-weight:600;color:var(--text-primary);text-decoration:underline}.site-bar a:focus-visible{outline:2px solid currentColor;outline-offset:2px}")


def build(html, generated):
    bar = ('<nav class="site-bar" aria-label="Site"><a href="/">&larr; Back to danfactory</a>'
           '<span>Real snapshot of this landing page\'s own dashboard, generated %s. '
           'Deploy is this site\'s own tab. The Evals tab shows danfactory template evals, not runs of this site.</span></nav>'
           % generated)
    html = html.replace("</style>", BAR_CSS + "\n</style>", 1)
    head = ('<meta name="description" content="Real snapshot of the danfactory landing page\'s own project dashboard: '
            'progress, roadmap, deploys and template evals.">\n<link rel="icon" href="/favicon.svg" type="image/svg+xml">\n')
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


SEV_LABEL = {"critical": "critical", "high": "high", "medium": "medium", "low": "low", "informational": "info"}


def security_panel(sec, e):
    """Public Security tab: closed findings as severity, title and state only (no exploit paths or file locations)."""
    recs = [r for r in (sec or {}).get("records", []) if r.get("state", "open") in CLOSED]
    if not recs:
        return '<div class="card"><h2>Security</h2><p class="muted">No published findings.</p></div>'
    rows = "".join('<tr><td><span class="imp low">%s</span></td><td>%s</td><td>%s</td></tr>' % (
        e(SEV_LABEL.get(r.get("severity"), r.get("verdict", "").replace("_", " ")) or "finding"),
        e(r.get("title")), e(r.get("state"))) for r in recs)
    good = "".join("<li>%s</li>" % e(g) for g in (sec or {}).get("positive", []))
    return ('<section class="grid"><div class="card" style="grid-column:1/-1"><h2>Fixed findings</h2>'
            '<p class="muted">Last audit %s. This public copy lists fixed findings only.</p>'
            '<div class="scroll"><table><thead><tr><th>Severity</th><th>Finding</th><th>State</th></tr></thead>'
            '<tbody>%s</tbody></table></div></div>%s</section>' % (
                e(sec.get("date")), rows,
                '<div class="card"><h2>What is already solid</h2><ul class="plain">%s</ul></div>' % good if good else ""))


def _hit(text):
    return bool(SECURITY_WORDS.search(text))


def scrub(o):
    """Remove security items from the data itself, whatever view renders them later (Overview, Roadmap, 6-month,
    Gantt, Releases, Evals ...). A dict is dropped from its list when one of its own string values names a finding
    (SEC-n) or security, unless it is done; a matching string is dropped from a list of strings. Nested containers
    are scrubbed on their own, so a card never takes its whole column with it."""
    if isinstance(o, dict):
        return {k: (v if k == "security" else scrub(v)) for k, v in o.items()}
    if isinstance(o, list):
        out = []
        for x in o:
            if isinstance(x, str):
                if not _hit(x):
                    out.append(x)
            elif isinstance(x, dict) and x.get("state") != "done" and any(isinstance(v, str) and _hit(v) for v in x.values()):
                continue
            else:
                out.append(scrub(x))
        return out
    return o


def public(d):
    """Copy of the dashboard data that is safe to publish: items filtered first, then rendered."""
    d = scrub(d)
    d["security"] = public_security(d.get("security"))
    debt = d.get("debt") or {}
    if isinstance(debt.get("by_impact"), dict) and isinstance(debt.get("open"), list):
        debt["by_impact"] = {k: sum(1 for x in debt["open"] if x.get("impact") == k) for k in debt["by_impact"]}
    return d


def leaks(html, sec):
    """Open findings (id or title) that still appear anywhere in the page, e.g. via another tab."""
    opened = [r for r in (sec or {}).get("records", []) if r.get("state", "open") not in CLOSED]
    return [r.get("id") for r in opened if (r.get("id") and r["id"] in html) or (r.get("title") and r["title"] in html)]


def main():
    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    import dashboard
    dashboard.build()  # the private, complete dashboard/ stays current too
    full = dashboard.collect()
    full_sec = full.get("security")
    d = public(full)
    # the public Security tab shows fixed findings as severity, title and state only
    dashboard.tab_security.render = lambda sec: security_panel(sec, dashboard.e)
    gates_render = dashboard.tab_gates.render  # a static row label, not a finding: keep the date, drop the word
    dashboard.tab_gates.render = lambda g: gates_render(g).replace("Last security audit", "Last audit")
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
