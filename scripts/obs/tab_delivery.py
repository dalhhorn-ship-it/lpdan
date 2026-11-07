"""Delivery tab: CI pass rate and duration, deploys, releases and open decisions (proposed ADRs).

Offline: reads metrics/ci-runs.json (written by scripts/ci_runs.py, git-ignored cache), deploy records in
metrics/history.jsonl, CHANGELOG.md or release tags, and docs/decisions/. Missing data shows a calm "not enough data yet".
Ported from the danfactory template (dashboard-backflow-from-minespel)."""
import datetime
import html
import json
import re

from . import sources as S

EMPTY = "Not enough data yet: no CI history, deploys or releases recorded."
CI_HINT = "No CI history yet. Run python3 scripts/ci_runs.py (CI does it on every build) to write metrics/ci-runs.json."
CHANGELOG_RE = re.compile(r"^##\s+\[?v?(\d+\.\d+\.\d+)\]?\s*(?:\(|[-–—]\s*)?(\d{4}-\d{2}-\d{2})?", re.M)
UNRELEASED_RE = re.compile(r"(?im)^##\s+\[?unreleased\]?\s*$")


def e(x):
    return html.escape(str(x), quote=True)


def num(v, unit="", nd=0):
    return "–" if v is None else ("%s%s" % (round(v, nd) if nd else int(round(v)), unit))


# ---------------------------------------------------------------- time and stats

def to_time(s):
    try:
        return datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")
    except (TypeError, ValueError):
        return None


def week_of(day):
    y, w, _ = day.isocalendar()
    return "%d-W%02d" % (y, w)


def last_weeks(today, n=8):
    """The last n ISO week keys, oldest first, ending with the week of today."""
    monday = today - datetime.timedelta(days=today.weekday())
    return [week_of(monday - datetime.timedelta(weeks=i)) for i in range(n - 1, -1, -1)]


def pct(part, whole):
    return round(100.0 * part / whole) if whole else None


def median(values):
    v = sorted(values)
    if not v:
        return None
    mid = len(v) // 2
    return v[mid] if len(v) % 2 else (v[mid - 1] + v[mid]) / 2


def p90(values):
    v = sorted(values)
    return v[min(len(v) - 1, int(0.9 * len(v)))] if v else None


# ---------------------------------------------------------------- CI

def parse_ci_runs(text):
    """The runs list from metrics/ci-runs.json text (scripts/ci_runs.py), or None."""
    if not text:
        return None
    try:
        data = json.loads(text)
    except ValueError:
        return None
    runs = data.get("runs") if isinstance(data, dict) else data
    return runs if isinstance(runs, list) else None


def ci_metrics(runs, today, main_branch="main"):
    """Pass rates, durations, last failures and runs per week. Skipped and cancelled runs do not count."""
    if not runs:
        return None
    runs = sorted((r for r in runs if isinstance(r, dict)), key=lambda r: r.get("created_at") or "", reverse=True)
    if not runs:
        return None
    decided = [r for r in runs if r.get("conclusion") in ("success", "failure")]
    last30 = decided[:30]
    main30 = [r for r in decided if r.get("head_branch") == main_branch][:30]
    mins = []
    for r in decided[:100]:
        a, b = to_time(r.get("run_started_at") or r.get("created_at")), to_time(r.get("updated_at"))
        if a and b and b >= a:
            mins.append((b - a).total_seconds() / 60)
    fail = next((r for r in runs if r.get("conclusion") == "failure"), None)
    main_fail = next((r for r in runs if r.get("conclusion") == "failure" and r.get("head_branch") == main_branch), None)
    weeks = last_weeks(today)
    per = {w: {"runs": 0, "ok": 0, "decided": 0} for w in weeks}
    for r in runs:
        t = to_time(r.get("created_at"))
        w = week_of(t.date()) if t else None
        if w in per:
            per[w]["runs"] += 1
            if r.get("conclusion") in ("success", "failure"):
                per[w]["decided"] += 1
                per[w]["ok"] += r.get("conclusion") == "success"

    def short(r):
        return None if r is None else {"date": (r.get("created_at") or "")[:10], "branch": r.get("head_branch") or "",
                                       "url": r.get("html_url") or ""}
    return {
        "runs": len(runs), "main_branch": main_branch,
        "pass_rate_30": pct(sum(r["conclusion"] == "success" for r in last30), len(last30)),
        "decided_30": len(last30),
        "main_pass_rate": pct(sum(r["conclusion"] == "success" for r in main30), len(main30)),
        "main_decided": len(main30),
        "median_min": round(median(mins), 1) if mins else None,
        "p90_min": round(p90(mins), 1) if mins else None,
        "last_failure": short(fail), "last_main_failure": short(main_fail),
        "weeks": weeks,
        "runs_per_week": [per[w]["runs"] for w in weeks],
        "pass_per_week": [pct(per[w]["ok"], per[w]["decided"]) for w in weeks],
    }


# ---------------------------------------------------------------- deploys and releases

def deploy_metrics(dates, today, source=""):
    """Deploys per week from a list of YYYY-MM-DD dates; None when there are no dates at all."""
    if not dates:
        return None
    days = []
    for s in dates:
        try:
            days.append(datetime.date.fromisoformat(str(s).strip()[:10]))
        except ValueError:
            pass
    weeks = last_weeks(today)
    return {"total": len(days), "last": max(days).isoformat() if days else None, "source": source,
            "weeks": weeks, "per_week": [sum(1 for d in days if week_of(d) == w) for w in weeks]}


def deploy_dates(root):
    """Deploy dates recorded by `metrics.py deploy` in metrics/history.jsonl."""
    out = []
    for ln in S.read(root, "metrics/history.jsonl").splitlines():
        try:
            r = json.loads(ln)
        except ValueError:
            continue
        if isinstance(r, dict) and r.get("kind") == "deploy" and isinstance(r.get("ts"), str):
            out.append(r["ts"][:10])
    return out


def parse_changelog(text):
    """Releases and the bullet count under Unreleased. Accepts `## 1.2.0 (2026-01-02)` and `## [1.2.0] - 2026-01-02`."""
    res = {"latest": "", "latest_date": "", "unreleased": None, "releases": []}
    if not text:
        return res
    for m in CHANGELOG_RE.finditer(text):
        res["releases"].append({"version": m.group(1), "date": m.group(2) or ""})
    if res["releases"]:
        res["latest"], res["latest_date"] = res["releases"][0]["version"], res["releases"][0]["date"]
    m = UNRELEASED_RE.search(text)
    if m:
        body = re.split(r"(?m)^##\s", text[m.end():], maxsplit=1)[0]
        res["unreleased"] = sum(1 for l in body.splitlines() if re.match(r"^\s*[*-] ", l))
    return res


def release_metrics(releases, today):
    """Count, median gap and days since the last release, from [{version, date}] (CHANGELOG or tags)."""
    rel = []
    for r in releases or []:
        try:
            rel.append((r["version"], datetime.date.fromisoformat(r["date"])))
        except (KeyError, TypeError, ValueError):
            pass
    if not rel:
        return None
    rel.sort(key=lambda x: x[1])
    gaps = [(b[1] - a[1]).days for a, b in zip(rel, rel[1:])]
    gap = median(gaps)
    return {"count": len(rel), "versions": [{"version": v, "date": d.isoformat()} for v, d in rel],
            "median_gap_days": (int(gap) if gap == int(gap) else gap) if gaps else None,
            "days_since_last": (today - rel[-1][1]).days, "last": rel[-1][0]}


def tag_releases(root):
    """Release-looking git tags (v1.2.3 or 1.2.3) with their dates."""
    out = S.git(root, "for-each-ref", "refs/tags", "--format=%(refname:short)|%(creatordate:short)")
    rows = []
    for line in out.splitlines():
        name, _, date = line.partition("|")
        if re.fullmatch(r"v?\d+\.\d+(\.\d+)?", name):
            rows.append({"version": name, "date": date})
    return rows


def open_decisions(root):
    """ADRs waiting for a decision (status proposed)."""
    rows = S.adrs(root)
    return {"total": len(rows), "open": [{"num": a["num"], "title": a["title"]} for a in rows if a["status"] == "proposed"]}


# ---------------------------------------------------------------- collect / line / render

def collect(root, base=None, today=None):
    today = today or datetime.date.today()
    try:
        f = json.loads(S.read(root, "factory.json") or "{}")
    except ValueError:
        f = {}
    prod = ((f.get("integrations") or {}).get("deploy") or {}).get("production_branch") or "main"
    cl = parse_changelog(S.read(root, "CHANGELOG.md"))
    return {"ci": ci_metrics(parse_ci_runs(S.read(root, "metrics/ci-runs.json")), today, prod),
            "deploys": deploy_metrics(deploy_dates(root), today, "metrics/history.jsonl"),
            "releases": release_metrics(cl["releases"] or tag_releases(root), today),
            "changelog": cl, "decisions": open_decisions(root)}


def line(d):
    ci, rel, dec = d["ci"], d["releases"], d["decisions"]
    parts = ["CI %s%% (last %d)" % (ci["pass_rate_30"], ci["decided_30"]) if ci and ci["pass_rate_30"] is not None else "no CI data yet"]
    parts.append("%d deploys" % d["deploys"]["total"] if d["deploys"] else "no deploys recorded")
    parts.append("%d releases, %d days since last" % (rel["count"], rel["days_since_last"]) if rel else "no releases")
    parts.append("%d open decisions" % len(dec["open"]))
    return ", ".join(parts)


def tile(label, value, sub, state="na"):
    return ('<div class="tile %s"><div class="label">%s</div><div class="value">%s</div><div class="sub">%s</div></div>'
            % (e(state), e(label), e(value), e(sub)))


def pass_state(v):
    return "na" if v is None else "ok" if v >= 90 else "warn" if v >= 70 else "bad"


def bars(values, weeks, title, unit=""):
    """Small inline SVG bar chart, one bar per week (no JS). None values draw as an empty stub."""
    nums = [v for v in values if isinstance(v, (int, float))]
    top = max(nums) if nums and max(nums) > 0 else 1
    rects = []
    for i, (v, w) in enumerate(zip(values, weeks)):
        x = i * 14 + 2
        if isinstance(v, (int, float)):
            h = max(1.5, 36.0 * v / top) if v else 1.5
            rects.append('<rect x="%d" y="%.1f" width="10" height="%.1f" rx="1.5"%s><title>%s: %s%s</title></rect>'
                         % (x, 40 - h, h, ' class="zero"' if not v else "", e(w), e(v), e(unit)))
        else:
            rects.append('<rect x="%d" y="38.5" width="10" height="1.5" class="zero"><title>%s: no data</title></rect>'
                         % (x, e(w)))
    last = values[-1] if values else None
    return ('<figure class="bars"><figcaption>%s <b>%s</b> <span class="muted">this week</span></figcaption>'
            '<svg viewBox="0 0 %d 40" preserveAspectRatio="none" role="img" aria-label="%s per week">%s</svg>'
            '<div class="axis"><span>%s</span><span>%s</span></div></figure>'
            % (e(title), num(last, unit) if isinstance(last, (int, float)) else "–", len(weeks) * 14, e(title),
               "".join(rects), e(weeks[0] if weeks else ""), e(weeks[-1] if weeks else "")))


STYLE = ("<style>.charts{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:16px;margin:12px 0}"
         "figure.bars{margin:0}figure.bars figcaption{font-size:13px}"
         "figure.bars svg{width:100%;height:56px;display:block;fill:var(--ok,#2a7)}"
         "figure.bars rect.zero{fill:var(--border,#ccc)}"
         "figure.bars .axis{display:flex;justify-content:space-between;font-size:11px;color:var(--muted,#777)}</style>")


def delivery_html(d):
    ci, dep, rel, cl, dec = d["ci"], d["deploys"], d["releases"], d["changelog"], d["decisions"]
    g = lambda x, k: None if x is None else x.get(k)  # noqa: E731
    stale = rel is not None and rel["days_since_last"] > 14 and bool(cl["unreleased"])
    tiles = "".join([
        tile("CI pass rate", num(g(ci, "pass_rate_30"), "%"), "last %s finished runs" % (g(ci, "decided_30") or 0),
             pass_state(g(ci, "pass_rate_30"))),
        tile("Pass rate on %s" % (g(ci, "main_branch") or "main"), num(g(ci, "main_pass_rate"), "%"),
             "last %s runs" % (g(ci, "main_decided") or 0), pass_state(g(ci, "main_pass_rate"))),
        tile("CI time", num(g(ci, "median_min"), " min", 1), "median · p90 %s" % num(g(ci, "p90_min"), " min", 1)),
        tile("Deploys", num(g(dep, "total")), "last %s" % (g(dep, "last") or "–")),
        tile("Releases", num(g(rel, "count")), "median %s days apart" % num(g(rel, "median_gap_days"))),
        tile("Since last release", "%s days" % rel["days_since_last"] if rel else "–",
             "%s unreleased changes" % (cl["unreleased"] if cl["unreleased"] is not None else "–"),
             "warn" if stale else "na"),
        tile("Open decisions", str(len(dec["open"])), "proposed ADRs of %d" % dec["total"],
             "warn" if dec["open"] else "na"),
    ])
    charts = []
    if ci:
        charts.append(bars(ci["runs_per_week"], ci["weeks"], "CI runs"))
        charts.append(bars(ci["pass_per_week"], ci["weeks"], "CI pass rate", "%"))
    if dep:
        charts.append(bars(dep["per_week"], dep["weeks"], "Deploys"))
    lines = []
    if ci is None:
        lines.append(e(CI_HINT))
    else:
        for label, fl in (("Last failure", ci["last_failure"]), ("Last failure on " + ci["main_branch"], ci["last_main_failure"])):
            lines.append("%s: %s" % (e(label), "none" if fl is None else '%s on <span class="mono">%s</span>%s' % (
                e(fl["date"]), e(fl["branch"]), ' · <a href="%s">run</a>' % e(fl["url"]) if fl["url"] else "")))
    lines.append(e("Deploys: " + (dep["source"] if dep else "none recorded yet (python3 scripts/metrics.py deploy)")))
    lines.append(e("Releases: " + ("CHANGELOG.md or release tags" if rel else "none yet (CHANGELOG.md headings like ## 1.2.0 (2026-01-02), or v1.2.0 tags)")))
    for a in dec["open"]:
        lines.append("Open decision: <span class=\"mono\">%s</span> %s" % (e(a["num"]), e(a["title"])))
    lines.append(e("Skipped and cancelled CI runs do not count toward pass rates."))
    return (STYLE + '<div class="card"><h2>Delivery</h2><div class="tiles">%s</div>%s<ul class="plain">%s</ul></div>' % (
        tiles, '<div class="charts">%s</div>' % "".join(charts) if charts else "",
        "".join("<li>%s</li>" % l for l in lines)))


def render(d):
    if not (d["ci"] or d["deploys"] or d["releases"] or d["decisions"]["open"]):
        return '<div class="card"><h2>Delivery</h2><p class="muted">%s</p><p class="muted small">%s</p></div>' % (e(EMPTY), e(CI_HINT))
    return delivery_html(d)
