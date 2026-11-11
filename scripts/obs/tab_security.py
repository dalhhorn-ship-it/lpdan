"""Security tab (lpdan-only): latest audit summary from docs/security/latest.json.

Summaries only, never payloads or secrets. Carbon classes and var(--...) tokens only (see theme.py).
The public snapshot (scripts/site_dashboard.py) filters the DATA (open findings removed) before rendering.
"""
import html
import json

from . import sources as S

CSS = ""
SEV_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3, "informational": 4}
SEV_CLASS = {"critical": "high", "high": "high", "medium": "medium", "low": "low", "informational": "low"}
CLOSED = ("fixed", "accepted")


def e(x):
    return html.escape("" if x is None else str(x), quote=True)


def tile(label, value, sub, state="na", words=("ok", "watch", "bad")):
    badge = {"ok": words[0], "warn": words[1], "bad": words[2], "na": ""}[state]
    return ('<div class="tile %s"><div class="label">%s</div><div class="value">%s</div><div class="sub">%s%s</div></div>'
            % (state, e(label), e(value), e(sub), ' · <span class="badge">%s</span>' % e(badge) if badge else ""))


def collect(root, base):
    try:
        return json.loads(S.read(root, "docs/security/latest.json") or "null")
    except ValueError:
        return None


def line(sec):
    if not sec:
        return "no audit yet"
    open_n = sum(r.get("state", "open") not in CLOSED for r in sec.get("records", []))
    return "%d open of %d records" % (open_n, len(sec.get("records", [])))


def render(sec):
    if not sec:
        return ('<div class="card"><h2>Security</h2><p class="muted">No security audit has run yet. '
                'Run the security-audit-run skill to fill this tab.</p></div>')
    recs = sorted(sec.get("records", []), key=lambda r: (r.get("verdict") != "confirmed",
                  SEV_ORDER.get(r.get("severity"), 9), r.get("id", "")))
    still_open = [r for r in recs if r.get("state", "open") not in CLOSED]
    n_conf = sum(r.get("verdict") == "confirmed" for r in still_open)  # fixed findings need no fix any more
    n_nv = sum(r.get("verdict") == "needs_validation" for r in still_open)
    cov = sec.get("coverage", {})
    tiles = "".join([
        tile("Open confirmed findings", str(n_conf), "verified by an independent agent, not yet fixed", "bad" if n_conf else "ok",
             words=("none", "", "fix needed")),
        tile("Open, needs validation", str(n_nv), "blocked on a fact outside the repo", "warn" if n_nv else "ok",
             words=("none", "owner check", "")),
        tile("Open items", str(len(still_open)), "of %d records" % len(recs), "bad" if still_open else "ok",
             words=("all closed", "", "open")),
        tile("Coverage", "%s/%s" % (cov.get("closed", 0), cov.get("units", 0)),
             "units closed (%s profile)" % sec.get("profile", "?"), "na")])
    rows = []
    for r in recs:
        sev = r.get("severity") if r.get("verdict") == "confirmed" else None
        label = sev or ("needs validation" if r.get("verdict") == "needs_validation" else r.get("verdict", ""))
        cls = SEV_CLASS.get(sev, "medium" if r.get("verdict") == "needs_validation" else "low")
        rows.append('<tr><td><span class="imp %s">%s</span></td><td>%s<div class="muted mono">%s</div></td>'
                    '<td>%s</td><td>%s</td><td>%s</td></tr>' % (
                        cls, e(label), e(r.get("title")), e(r.get("location")), e(r.get("boundary")),
                        e(r.get("fix")), e(r.get("state", "open"))))
    table = ('<div class="scroll"><table><thead><tr><th>Severity</th><th>Finding</th><th>Boundary</th>'
             '<th>Smallest fix</th><th>State</th></tr></thead><tbody>%s</tbody></table></div>' % "".join(rows)
             if rows else '<p class="muted">No findings survived independent verification.</p>')
    hard = "".join("<li><b>%s</b> %s</li>" % (e(h.get("area")), e(h.get("note"))) for h in sec.get("hardening", []))
    good = "".join("<li>%s</li>" % e(g) for g in sec.get("positive", []))
    limits = "".join("<li>%s</li>" % e(x) for x in sec.get("limits", []))
    meta = '%s · %s profile · <span class="mono">%s</span> · run %s' % (
        e(sec.get("date")), e(sec.get("profile")), e(sec.get("source_ref", "")[:12]), e(sec.get("status")))
    return ('<section class="tiles" aria-label="Security summary">%s</section>'
            '<section class="grid">'
            '<div class="card" style="grid-column:1/-1"><h2>Findings</h2><p class="muted">%s</p>%s</div>'
            '<div class="card"><h2>Hardening notes</h2><ul class="plain">%s</ul></div>'
            '<div class="card"><h2>What is already solid</h2><ul class="plain">%s</ul>'
            '<h3>Limits of this run</h3><ul class="plain">%s</ul></div>'
            '</section>' % (tiles, meta, table, hard or '<li class="muted">None.</li>',
                            good or '<li class="muted">None recorded.</li>', limits or '<li class="muted">None.</li>'))
