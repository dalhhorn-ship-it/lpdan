#!/usr/bin/env python3
"""Static checks for the landing page (stdlib only, < 1 s). See docs/design/ARCHITECTURE.md "Test strategy".

Prints "N passed, M failed"; exit 1 on any failure.
"""
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUB = ROOT / "public"
PAGE = PUB / "index.html"
FIXTURE = ROOT / "tests" / "fixtures" / "danfactory-README.md"
TOKENS = ROOT / "design" / "gpm-keynote" / "tokens.json"

EXTERNAL_ALLOW = {
    "https://github.com/dalhhorn-ship-it/danfactory",
    "https://github.com/dalhhorn-ship-it/danfactory/issues",
    "https://github.com/darcyegb/ClaudeCodeAgents",
    "https://github.com/spotify/portal-ai-plugins/tree/main/plugins/shunt",
    "https://github.com/colbymchenry/codegraph",
    "https://github.com/cloudflare/security-audit-skill",
    "https://github.com/davila7/claude-code-templates/blob/main/cli-tool/components/skills/development/cloudflare-deploy/SKILL.md",
}
# Commands not in the README fixture: command -> repo file it must appear in.
# Exact line (stripped) that must exist in the named file; no substring matching.
SNIPPET_ALLOW = {
    "python3 scripts/dashboard.py --print": ("CLAUDE.md", "`python3 scripts/dashboard.py --print` for a cheap status; `dashboard` skill to show the full page."),
    "claude": ("tests/fixtures/danfactory-README.md", "3. Start Claude Code (`claude`) and say **\"let's start\"**. The SessionStart hook tells Claude which phase you're in."),
}
CHALLENGES = [
    "01-setup.md", "02-farm-game.md", "03-tests-green.md", "04-ship-cloudflare.md",
    "05-adopt.md", "06-verified-feature.md", "07-retro-upstream.md",
]
BUDGET = {"index": 64 * 1024, "copy.js": 2 * 1024, "fonts": 60 * 1024, "img": 120 * 1024, "public": 300 * 1024}
BANNED = ("trusted by", "stars", "testimonial")
VOID = {"meta", "link", "br", "hr", "img", "input", "source", "area", "base", "col", "wbr"}
# Google Fonts "latin" subset unicode-range
LATIN = [(0x0, 0xFF), (0x131, 0x131), (0x152, 0x153), (0x2BB, 0x2BC), (0x2C6, 0x2C6), (0x2DA, 0x2DA),
         (0x2DC, 0x2DC), (0x304, 0x304), (0x308, 0x308), (0x329, 0x329), (0x2000, 0x206F), (0x20AC, 0x20AC),
         (0x2122, 0x2122), (0x2191, 0x2191), (0x2193, 0x2193), (0x2212, 0x2212), (0x2215, 0x2215),
         (0xFEFF, 0xFEFF), (0xFFFD, 0xFFFD)]


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.errors = [], []
        self.ids, self.hrefs, self.srcs, self.tags, self.attrs_all = [], [], [], [], []
        self.headings, self.imgs, self.buttons = [], [], []
        self.inline_scripts, self.styles, self.text = 0, [], []
        self.codes = []          # dicts: pre, copy
        self._code = None
        self._in_pre = self._in_style = False
        self._h = None
        self.faq = 0
        self.meta, self.title, self._in_title, self.html_lang = {}, "", False, None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.tags.append(tag)
        self.attrs_all.append((tag, a))
        if "id" in a:
            self.ids.append(a["id"])
        if tag == "a" and "href" in a:
            self.hrefs.append(a["href"])
        if tag in ("link",) and "href" in a:
            self.hrefs.append(a["href"])
        if "src" in a:
            self.srcs.append(a["src"])
        if tag == "html":
            self.html_lang = a.get("lang")
        if tag == "meta":
            self.meta[a.get("name") or a.get("property") or ("charset" if "charset" in a else "?")] = a
        if tag == "title":
            self._in_title = True
        if tag == "script" and "src" not in a:
            self.inline_scripts += 1
        if tag == "style":
            self._in_style = True
            self.styles.append("")
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.headings.append(int(tag[1]))
        if tag == "img":
            self.imgs.append(a)
        if tag == "button":
            self.buttons.append(a)
        if tag == "details" and "faq" in (a.get("class") or "").split():
            self.faq += 1
        if tag == "div" and "code" in (a.get("class") or "").split():
            self._code = {"pre": "", "copy": None}
            self.codes.append(self._code)
        if tag == "pre":
            self._in_pre = True
        if tag == "button" and self._code is not None and "data-copy" in a:
            self._code["copy"] = a["data-copy"]
        if tag not in VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack or self.stack[-1] != tag:
            self.errors.append(f"unbalanced </{tag}> (open: {self.stack[-1] if self.stack else None})")
            if tag in self.stack:
                while self.stack and self.stack.pop() != tag:
                    pass
            return
        self.stack.pop()
        if tag == "title":
            self._in_title = False
        if tag == "style":
            self._in_style = False
        if tag == "pre":
            self._in_pre = False

    def handle_data(self, data):
        if self._in_style:
            self.styles[-1] += data
        elif self._in_title:
            self.title += data
        else:
            self.text.append(data)
        if self._in_pre and self._code is not None:
            self._code["pre"] += data


# ---------- tiny CSS helpers ----------
def css_rules(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    out = []

    def walk(block):
        for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", block):
            out.append((" ".join(m.group(1).split()), m.group(2)))
    # flatten @media: inner rules are matched by the same regex (inner braces closed first)
    walk(css)
    return out


def px_of(val, rootvars):
    """Resolve a font-size expression to its minimum in px, or None."""
    val = val.strip()
    m = re.fullmatch(r"var\((--[\w-]+)\)", val)
    if m:
        return px_of(rootvars.get(m.group(1), ""), rootvars) if m.group(1) in rootvars else None
    m = re.match(r"clamp\(\s*([^,]+),", val)
    if m:
        return px_of(m.group(1), rootvars)
    m = re.fullmatch(r"([\d.]+)(px|rem)", val)
    if m:
        return float(m.group(1)) * (16 if m.group(2) == "rem" else 1)
    return None


def dashboard_checks(check):
    """Roadmap tab of scripts/dashboard.py: global numbering, done milestones collapsed, next-up strip."""
    sys.path.insert(0, str(ROOT / "scripts"))
    import dashboard
    md = ("## Milestone: M0 — Set up (target: 2026-01-01)\n- [x] A (S)\n- [x] B (S)\n"
          "## Milestone: M1 — Launch (target: 2026-02-01)\n> Sequence: ship hero first\n"
          "- [ ] Page (M) #quality. AC: renders\n- [ ] Copy (S)\n- [x] Old (S)\n- [ ] Deploy (S) #infra\n- [ ] Faq (S)\n")
    rm = dashboard.roadmap(dashboard.parse_backlog(md), [])
    seqs = [c["seq"] for col in rm["columns"] for k in ("value", "foundation") for c in col["lanes"][k] if c["seq"]]
    check("dashboard roadmap: open items numbered 1..n across lanes", sorted(seqs) == [1, 2, 3, 4], seqs)
    check("dashboard roadmap: done milestone collapsed", [c["name"] for c in rm["columns"]] == ["M1 — Launch"]
          and rm["done"][0]["done"] == 2, rm["done"])
    check("dashboard roadmap: next up = first 3, short title", [x["short"] for x in rm["next"]] == ["Page", "Copy", "Deploy"],
          rm["next"])
    out = dashboard.render_roadmap(rm)
    check("dashboard roadmap: sequence subtitle and done line", "ship hero first" in out and "Done: M0 — Set up (2/2)" in out)

    # Deploy tab: failed attempts have null seconds; links come from factory.json + git remote.
    deps = [{"ts": "2026-11-06T19:40:21+00:00", "kind": "deploy", "env": "prod", "sha": "aaa1111", "ok": False,
             "seconds": None, "error": "Auth error <10000>"},
            {"ts": "2026-11-07T05:54:46+00:00", "kind": "deploy", "env": "prod", "sha": "bbb2222", "ok": True,
             "seconds": 24.0, "smoke": "ok: 200 /"}]
    cfg = {"budgets": {"deploy_seconds": 120}, "integrations": {"deploy": {
        "production_url": "https://x.workers.dev", "worker_name": "wk", "route": "B-github-actions",
        "production_branch": "main", "workers_subdomain": "sub"}}}
    dv = dashboard.deploy_view(cfg, deps, "2026-11-07T07:54:46+00:00")
    out = dashboard.render_deploy({"deploy_tab": dv})
    check("dashboard deploy: stats", (dv["total"], dv["ok"], dv["success_rate"], dv["median"], dv["best"], dv["last_seconds"])
          == (2, 1, 50, 24.0, 24.0, 24.0) and dv["ago_seconds"] == 7200, dv)
    check("dashboard deploy: links", "https://dash.cloudflare.com/?to=/:account/workers/services/view/wk/production" in out
          and "https://x.workers.dev/version" in out and "/actions/workflows/deploy-cloudflare.yml" in out
          and "B (GitHub Actions)" in out)
    cfg["integrations"]["deploy"]["account_id"] = "acc123"
    check("dashboard deploy: account_id link", "dash.cloudflare.com/acc123/workers/services/view/wk/production"
          in dashboard.deploy_view(cfg, deps, deps[-1]["ts"])["links"]["cloudflare"])
    check("dashboard deploy: failed row null seconds, escaped error, smoke",
          "failed" in out and "Auth error &lt;10000&gt;" in out and "ok: 200 /" in out and "None" not in out)
    empty = dashboard.render_deploy({"deploy_tab": dashboard.deploy_view({}, [], "2026-11-07T00:00:00+00:00")})
    check("dashboard deploy: empty data", "not enough data yet" in empty and "not recorded" in empty and "None" not in empty)
    tpl = dashboard.TEMPLATE
    check("dashboard deploy: tab wired in page", 'id="tab-deploy"' in tpl and 'for="tab-deploy"' in tpl)


def main():
    results = []

    def check(name, ok, detail=""):
        results.append((name, bool(ok), detail))

    html = PAGE.read_text(encoding="utf-8")
    p = Page()
    p.feed(html)
    p.close()
    css = "\n".join(p.styles)
    css_nc = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    text = "".join(p.text)

    # 1 snippets
    readme = FIXTURE.read_text(encoding="utf-8")
    fenced = set()
    for block in re.findall(r"```[^\n]*\n(.*?)```", readme, flags=re.S):
        fenced.update(line.strip() for line in block.splitlines() if line.strip())
    bad = []
    for c in p.codes:
        pre = c["pre"].strip()
        ok = pre in fenced
        if not ok:
            src = SNIPPET_ALLOW.get(pre)
            if src:
                lines = [ln.strip() for ln in (ROOT / src[0]).read_text(encoding="utf-8").splitlines()]
                ok = src[1] in lines and pre in src[1]
        if not ok:
            bad.append(("not in README fixture/allowlist", pre))
        elif c["copy"] is not None and re.sub(r"\s+#\s.*$", "", pre) != c["copy"]:
            bad.append(("data-copy differs from snippet", pre))
    check("snippets verbatim in README fixture", p.codes and not bad, bad)

    # 2 links
    ids = set(p.ids)
    broken = [h for h in p.hrefs if h.startswith("#") and h[1:] and h[1:] not in ids]
    check("internal anchors resolve", not broken, broken)
    rel = [u for u in p.hrefs + p.srcs
           if not re.match(r"(https?:|#|data:|mailto:)", u) and not (PUB / u.split("#")[0].split("?")[0]).exists()]
    check("relative links/src exist", not rel, rel)
    ext = [u for u in p.hrefs + p.srcs if re.match(r"(https?:)?//", u) and u not in EXTERNAL_ALLOW]
    check("external URLs on allowlist only", not ext, ext)
    check("no url(http)/@import in CSS", not re.search(r"url\(\s*['\"]?(https?:|//)|@import", css_nc))
    lowered = html.lower()
    forbidden = [t for t in ("<form", "<input", "<iframe") if t in lowered]
    forbidden += [x for x in ("document.cookie", "fetch(") if x in html]
    forbidden += [f"{t}:{k}" for t, a in p.attrs_all for k in a if k.startswith("on")]
    forbidden += ["style attribute"] if any("style" in a for _, a in p.attrs_all) else []
    check("no forms/iframes/inline handlers/style attrs", not forbidden, forbidden)
    check("no inline <script>", p.inline_scripts == 0)
    check("copy.js loaded with defer", any(t == "script" and a.get("src") == "copy.js" and "defer" in a
                                           for t, a in p.attrs_all))

    # 3 campaign (markup arrives in slice S5; files must exist now)
    missing = [f for f in CHALLENGES if not (PUB / "challenges" / f).is_file()]
    check("7 challenge files exist", not missing, missing)
    bad_ch = []
    for i, f in enumerate(CHALLENGES, 1):
        fp = PUB / "challenges" / f
        if fp.is_file() and f"[challenge-{i}]" not in fp.read_text(encoding="utf-8"):
            bad_ch.append(f)
    check("challenge files contain their [challenge-N] tag", not bad_ch, bad_ch)
    if "campaign" in ids:  # gated until the campaign section is built
        links = [h for h in p.hrefs if h.startswith("challenges/")]
        order = [h.split("/")[-1] for h in links]
        check("each challenge linked twice, in order", order == [f for f in CHALLENGES for _ in (0, 1)], order)
        check("exactly 8 details.faq", p.faq == 8, p.faq)

    # 4 design rules in CSS
    check("no box-shadow/text-shadow/drop-shadow", not re.search(r"(box|text)-shadow\s*:\s*(?!none)|drop-shadow", css_nc))
    radii = re.findall(r"border(?:-[a-z]+){0,2}-radius\s*:\s*([^;}]+)", css_nc)
    check("no border-radius other than 0", all(r.strip() in ("0", "0px") for r in radii), radii)
    check("no gradients/backdrop-filter", not re.search(r"-gradient\(|backdrop-filter", css_nc))
    root = re.search(r":root\s*\{([^}]*)\}", css_nc)
    root_css = root.group(1) if root else ""
    rootvars = dict(re.findall(r"(--[\w-]+)\s*:\s*([^;]+);", root_css))
    tokens = json.loads(TOKENS.read_text(encoding="utf-8"))["color"]["tokens"]
    dark = {t["value"]["dark"].upper() for t in tokens}
    outside = re.findall(r"#[0-9a-fA-F]{3,8}\b", css_nc.replace(root_css, ""))
    outside += re.findall(r"\b(?:rgba?|hsla?|hwb|lab|lch|oklab|oklch|color-mix)\(", css_nc.replace(root_css, ""))
    named = r"\b(?:red|blue|green|black|white|gray|grey|magenta|cyan|yellow|orange|purple|pink|navy|teal|lime|aqua|silver|maroon|olive|fuchsia)\b"
    for _, body in css_rules(css_nc.replace(root_css, "")):
        for m in re.finditer(r"(?<![-\w])(?:color|background(?:-color)?|border(?:-[a-z]+)?(?:-color)?|outline(?:-color)?|fill|stroke)\s*:\s*([^;]+)", body):
            outside += re.findall(named, re.sub(r"var\([^)]*\)", "", m.group(1)), flags=re.I)
    check("colours only via tokens (no hex/rgb()/hsl()/named outside :root)", not outside, outside)
    unknown = [h for h in re.findall(r"#[0-9a-fA-F]{3,8}\b", root_css) if h.upper() not in dark]
    check("root hex colours are tokens.json dark values", not unknown, unknown)
    small = []
    for sel, body in css_rules(css):
        for m in re.finditer(r"(?<![-\w])font-size\s*:\s*([\d.]+)px", body):
            if float(m.group(1)) < 16 and ".dash" not in sel:
                small.append((sel, m.group(1)))
        m = re.search(r"(?<![-\w])font\s*:\s*(?:[\w ]*?\s)?([\d.]+)px", body)
        if m and float(m.group(1)) < 16 and ".dash" not in sel:
            small.append((sel, m.group(1)))
    check("px font sizes < 16 only under .dash", not small, small)

    # magenta text: >= 24px and bold/display (unsized rules only on h1/h2)
    mag = []
    for sel, body in css_rules(css):
        if not re.search(r"(?<![-\w])color\s*:\s*var\(--magenta\)", body):
            continue
        size = None
        m = re.search(r"(?<![-\w])font-size\s*:\s*([^;]+)", body)
        if m:
            size = px_of(m.group(1), rootvars)
        m = re.search(r"(?<![-\w])font\s*:\s*([^;]+)", body)
        if m and size is None:
            sm = re.search(r"((?:clamp\([^)]*\)|[\d.]+(?:px|rem)|var\(--fs-[\w-]+\)))(?:/|\s)", m.group(1) + " ")
            size = px_of(sm.group(1), rootvars) if sm else None
        bold = bool(re.search(r"font-display|Archivo Black|font\s*:\s*[^;]*\b[78]00\b|font-weight\s*:\s*(700|800|900|bold)", body))
        if size is None:
            if not re.search(r"\bh[12]\b", sel):
                mag.append((sel, "size unresolved"))
        elif size < 24 or not bold:
            mag.append((sel, f"{size}px bold={bold}"))
    check("magenta text >= 24px and bold/display", not mag, mag)

    # 5 HTML basics
    check("lang, charset, viewport, title, description",
          p.html_lang == "en" and "charset" in p.meta and "viewport" in p.meta and p.title.strip()
          and "description" in p.meta)
    check("exactly one h1", p.headings.count(1) == 1)
    skips = [(a, b) for a, b in zip(p.headings, p.headings[1:]) if b > a + 1]
    check("no heading level skips", not skips, skips)
    check("unique ids", len(p.ids) == len(ids))
    check("img alt + width + height", all(i.get("alt") and i.get("width") and i.get("height") for i in p.imgs))
    check("buttons have type", all(b.get("type") for b in p.buttons))
    check("balanced tags", not p.errors and not p.stack, p.errors + p.stack)

    # 6 glyphs
    odd = sorted({c for c in html if not any(lo <= ord(c) <= hi for lo, hi in LATIN)})
    check("all characters inside the latin font subset", not odd, [f"U+{ord(c):04X}" for c in odd])

    # 7 budgets + banned phrases
    def size(rel):
        return (PUB / rel).stat().st_size
    fonts = sum(f.stat().st_size for f in (PUB / "fonts").glob("*.woff2"))
    shots = [f.stat().st_size for f in (PUB / "img").glob("dashboard-*")]
    pub_total = sum(f.stat().st_size for f in PUB.rglob("*")
                    if f.is_file() and "challenges" not in f.relative_to(PUB).parts)
    check("index.html <= 64 KB", size("index.html") <= BUDGET["index"], size("index.html"))
    check("copy.js <= 2 KB", size("copy.js") <= BUDGET["copy.js"], size("copy.js"))
    check("fonts <= 60 KB", fonts <= BUDGET["fonts"], fonts)
    check("dashboard screenshot <= 120 KB", all(s <= BUDGET["img"] for s in shots), shots)
    check("public/ (without challenges) <= 300 KB", pub_total <= BUDGET["public"], pub_total)
    check("font licence shipped", (PUB / "fonts" / "OFL.txt").is_file())
    low = text.lower()
    check("no banned proof phrases", not [b for b in BANNED if b in low], [b for b in BANNED if b in low])

    dashboard_checks(check)

    failed = [r for r in results if not r[1]]
    for name, _, detail in failed:
        print(f"FAIL {name}: {detail}")
    print(f"{len(results) - len(failed)} passed, {len(failed)} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
