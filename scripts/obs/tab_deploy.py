"""Deploy tab (lpdan-only): live links, deploy stats and history from integrations.deploy and deploy records.

Offline: reads factory.json and metrics/history.jsonl (kind=deploy) and the git origin URL. Carbon classes and
var(--...) tokens only (see theme.py); no colour literals.
"""
import datetime
import html
import re
import statistics

from . import sources as S

CSS = """
.panel-deploy .card { margin-bottom:var(--sp-05); }
.live-row { display:flex; flex-direction:column; margin-bottom:var(--sp-03); }
a.live { font-size:1.25rem; font-weight:600; overflow-wrap:anywhere; }
.links a, .panel-deploy .mono { overflow-wrap:anywhere; }
.kv { display:grid; grid-template-columns:max-content 1fr; gap:var(--sp-02) var(--sp-05); margin:var(--sp-04) 0 0; }
.kv dt { color:var(--text-secondary); } .kv dd { margin:0; min-width:0; }
td.note { min-width:180px; overflow-wrap:anywhere; font-size:.8125rem; color:var(--text-secondary); }
"""


def e(x):
    return html.escape("" if x is None else str(x), quote=True)


def num(v, suffix=""):
    return "–" if v is None else "%s%s" % (round(v, 1) if isinstance(v, float) and v != int(v) else int(v), suffix)


def tile(label, value, sub, state="na", words=("healthy", "watch", "failing")):
    badge = {"ok": words[0], "warn": words[1], "bad": words[2], "na": ""}[state]
    return ('<div class="tile %s"><div class="label">%s</div><div class="value">%s</div><div class="sub">%s%s</div></div>'
            % (state, e(label), e(value), e(sub), ' · <span class="badge">%s</span>' % e(badge) if badge else ""))


def github_repo(root):
    m = re.search(r"github\.com[:/]+([^/\s]+)/([^/\s]+?)(?:\.git)?/?$", S.git(root, "remote", "get-url", "origin") or "")
    return "%s/%s" % m.groups() if m else ""


def fmt_ago(sec):
    if sec is None:
        return "–"
    d, r = divmod(sec, 86400)
    h, r = divmod(r, 3600)
    m = r // 60
    if d:
        return "%dd %dh ago" % (d, h)
    return ("%dh %dm ago" % (h, m)) if h else ("%dm ago" % m if m else "%ds ago" % r)


def view(f, deps, now_iso, repo=""):
    """Deploy data from factory config `f`, deploy records `deps` (oldest first) and an owner/repo string."""
    cfg = f.get("integrations", {}).get("deploy", {})
    worker, prod = cfg.get("worker_name"), (cfg.get("production_url") or "").rstrip("/")
    acct = cfg.get("account_id")
    dash = ("https://dash.cloudflare.com/%s/workers/services/view/%s/production" % (acct, worker) if acct
            else "https://dash.cloudflare.com/?to=/:account/workers/services/view/%s/production" % worker) if worker else ""
    okr = [r for r in deps if r["ok"]]
    secs = sorted(r["seconds"] for r in okr if r.get("seconds") is not None)
    ago = None
    if deps:
        try:
            ago = max(0, int((datetime.datetime.fromisoformat(now_iso) - datetime.datetime.fromisoformat(deps[-1]["ts"])).total_seconds()))
        except ValueError:
            ago = None
    return {
        "links": {"live": prod, "cloudflare": dash, "version": prod + "/version" if prod else "",
                  "actions": "https://github.com/%s/actions/workflows/deploy-cloudflare.yml" % repo if repo else ""},
        "info": {"worker": worker, "route": cfg.get("route"), "branch": cfg.get("production_branch"),
                 "subdomain": cfg.get("workers_subdomain")},
        "total": len(deps), "ok": len(okr),
        "success_rate": round(100.0 * len(okr) / len(deps)) if deps else None,
        "last_seconds": next((r["seconds"] for r in reversed(deps) if r.get("seconds") is not None), None),
        "budget": f.get("budgets", {}).get("deploy_seconds"),
        "median": round(statistics.median(secs), 1) if secs else None, "best": min(secs) if secs else None,
        "last_ok": okr[-1] if okr else None, "ago_seconds": ago,
        "smoke": next((r["smoke"] for r in reversed(deps) if r.get("smoke")), None),
        "history": list(reversed(deps[-30:])),
    }


def collect(root, base):
    import metrics  # scripts/ is on sys.path when dashboard.py runs
    deps = [r for r in metrics.load(metrics.HISTORY) if r["kind"] == "deploy"]
    return view(metrics.factory(), deps, metrics.now(), github_repo(root))


def line(d):
    if not d["total"]:
        return "no deploys recorded"
    return "%d/%d deploys ok, last push-to-live %s" % (d["ok"], d["total"], num(d["last_seconds"], "s"))


def render(dv):
    L, info = dv["links"], dv["info"]

    def link(url, text):
        return '<a href="%s" rel="noopener">%s</a>' % (e(url), e(text)) if url else '<span class="muted">not configured</span>'

    live = ('<a class="live" href="%s" rel="noopener">%s</a>' % (e(L["live"]), e(L["live"]))
            if L["live"] else '<span class="muted">no production_url in factory.json</span>')
    route = {"B-github-actions": "B (GitHub Actions)"}.get(info["route"] or "", info["route"] or "–")
    links = ('<div class="live-row"><span class="muted small">Live site</span>%s</div>'
             '<ul class="plain links">'
             '<li><span class="muted">Cloudflare Worker</span> %s</li>'
             '<li><span class="muted">GitHub Actions deploy runs</span> %s</li>'
             '<li><span class="muted">/version endpoint</span> %s</li></ul>'
             '<dl class="kv"><dt>Worker</dt><dd class="mono">%s</dd><dt>Route</dt><dd>%s</dd>'
             '<dt>Production branch</dt><dd class="mono">%s</dd><dt>workers.dev subdomain</dt><dd class="mono">%s</dd></dl>'
             % (live, link(L["cloudflare"], "dashboard"), link(L["actions"], "deploy-cloudflare.yml"),
                link(L["version"], "/version"), e(info["worker"] or "–"), e(route), e(info["branch"] or "–"),
                e(info["subdomain"] or "–")))
    ok = dv["last_ok"]
    last_ok = ("%s · %s · %s" % (ok["ts"][:16].replace("T", " "), ok.get("sha") or "–", ok.get("env") or "–")) if ok else "–"
    ls, bud = dv["last_seconds"], dv["budget"]
    tiles = "".join([
        tile("Deploys", "%d / %d" % (dv["ok"], dv["total"]) if dv["total"] else "–", "succeeded / attempts"),
        tile("Success rate", num(dv["success_rate"], "%"), "all attempts" if dv["total"] else "not enough data yet",
             "na" if dv["success_rate"] is None else ("ok" if dv["success_rate"] >= 80 else "warn"),
             words=("healthy", "failures seen", "failing")),
        tile("Last push-to-live", num(ls, "s"), "budget %ss" % bud if ls is not None else "not enough data yet",
             "na" if ls is None or bud is None else ("ok" if ls <= bud else "bad"), words=("on budget", "watch", "over budget")),
        tile("Median / best", "%s / %s" % (num(dv["median"], "s"), num(dv["best"], "s")),
             "successful deploys" if dv["median"] is not None else "not enough data yet"),
        tile("Last successful", ok["ts"][5:16].replace("T", " ") if ok else "–", last_ok if ok else "not enough data yet"),
        tile("Since last deploy", fmt_ago(dv["ago_seconds"]), "any result" if dv["total"] else "not enough data yet"),
    ])
    rows = "".join(
        '<tr><td class="nowrap">%s</td><td>%s</td><td class="mono">%s</td><td>%s</td><td>%s</td><td class="note">%s</td></tr>'
        % (e(r["ts"][:16].replace("T", " ")), e(r.get("env") or "–"), e(r.get("sha") or "–"),
           '<span class="imp %s">%s</span>' % ("low" if r["ok"] else "high", "ok" if r["ok"] else "failed"),
           num(r.get("seconds"), "s"), e(r.get("error") or r.get("smoke") or "–")) for r in dv["history"]) \
        or '<tr><td colspan="6" class="muted">No deploys recorded (python3 scripts/metrics.py deploy).</td></tr>'
    return ('<section class="card"><h2>Links</h2>%s</section>'
            '<section class="tiles" aria-label="Deploy stats">%s</section>'
            '<section class="card"><h2>Deploy history</h2><div class="scroll"><table><thead><tr><th>When (UTC)</th><th>Env</th>'
            '<th>Commit</th><th>Result</th><th>Time</th><th>Error / note</th></tr></thead><tbody>%s</tbody></table></div>'
            '<p class="small"><b>Live checks:</b> %s</p></section>'
            % (links, tiles, rows, e(dv["smoke"]) if dv["smoke"] else '<span class="muted">not recorded</span>'))
