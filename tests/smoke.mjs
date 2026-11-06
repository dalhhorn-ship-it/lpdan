// Playwright smoke test for the landing page. See docs/design/ARCHITECTURE.md "Test strategy".
// Serves public/ from a tiny local server (.md as text/plain). Prints "N passed, M failed".
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
let chromium;
try { ({ chromium } = require('playwright')); } catch { ({ chromium } = await import('playwright')); }

const PUB = path.join(path.dirname(fileURLToPath(import.meta.url)), '..', 'public');
const TYPES = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.woff2': 'font/woff2',
  '.webp': 'image/webp', '.png': 'image/png', '.md': 'text/plain; charset=utf-8', '.txt': 'text/plain' };

// Apply public/_headers (CSP etc.) like Cloudflare would: blocks of "<pattern>" then indented "Name: value".
const rules = [];
try {
  let cur = null;
  for (const line of fs.readFileSync(path.join(PUB, '_headers'), 'utf8').split('\n')) {
    if (!line.trim()) continue;
    if (!/^\s/.test(line)) { cur = { pat: line.trim(), h: {} }; rules.push(cur); }
    else if (cur) { const i = line.indexOf(':'); cur.h[line.slice(0, i).trim().toLowerCase()] = line.slice(i + 1).trim(); }
  }
} catch { /* no _headers yet */ }
const headersFor = (p) => Object.assign({}, ...rules.filter((r) => r.pat === '/*' || (r.pat.endsWith('*') && p.startsWith(r.pat.slice(0, -1)))).map((r) => r.h));

const server = http.createServer((req, res) => {
  let p = decodeURIComponent(new URL(req.url, 'http://x').pathname);
  if (p.endsWith('/')) p += 'index.html';
  const f = path.join(PUB, path.normalize(p));
  if (!f.startsWith(PUB) || !fs.existsSync(f) || !fs.statSync(f).isFile()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'content-type': TYPES[path.extname(f)] || 'application/octet-stream', ...headersFor(p) });
  fs.createReadStream(f).pipe(res);
});
await new Promise((r) => server.listen(0, '127.0.0.1', r));
const origin = `http://127.0.0.1:${server.address().port}`;

let passed = 0; const failures = [];
const check = (name, ok, detail = '') => { if (ok) passed++; else failures.push(`${name} ${detail}`); };

const browser = await chromium.launch();
try {
  // Viewports: overflow, console, network, above the fold
  for (const [w, h] of [[375, 667], [1280, 800], [1440, 900]]) {
    const ctx = await browser.newContext({ viewport: { width: w, height: h } });
    const page = await ctx.newPage();
    const errors = [], foreign = [];
    page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
    await page.addInitScript(() => document.addEventListener('securitypolicyviolation', (e) => console.error('CSP violation: ' + e.violatedDirective + ' ' + e.blockedURI)));
    page.on('pageerror', (e) => errors.push(String(e)));
    page.on('request', (r) => { const u = r.url(); if (!u.startsWith(origin) && !u.startsWith('data:')) foreign.push(u); });
    const resp = await page.goto(origin + '/', { waitUntil: 'networkidle' });
    check(`CSP header applied @${w}`, !!(await resp.allHeaders())['content-security-policy']);
    const ov = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    check(`no horizontal overflow @${w}`, ov <= 0, `(+${ov}px)`);
    check(`no console/CSP errors @${w}`, errors.length === 0, errors.join('; '));
    check(`no non-local requests @${w}`, foreign.length === 0, foreign.join(', '));
    const fold = await page.evaluate((vh) => {
      const bottom = (s) => { const e = document.querySelector(s); return e ? e.getBoundingClientRect().bottom : Infinity; };
      return { h1: bottom('.hero h1'), sub: bottom('.hero .lede'), cta: bottom('.hero .btn.p') };
    }, h);
    for (const [k, v] of Object.entries(fold)) check(`hero ${k} above the fold @${w}x${h}`, v <= h, `(bottom ${Math.round(v)})`);
    const hero = await page.evaluate(() => {
      const nav = document.querySelector('nav.top'), cs = getComputedStyle(nav);
      const small = [...document.querySelectorAll('nav.top a, .hero .btn, .copy')].filter((a) => { const r = a.getBoundingClientRect(); return a.offsetParent && (Math.round(r.height) < 44 || Math.round(r.width) < 44); }).map((a) => a.textContent.trim());
      return { h1s: document.querySelectorAll('h1').length, h1fs: parseFloat(getComputedStyle(document.querySelector('.hero h1')).fontSize),
        sticky: cs.position === 'sticky' && cs.top === '0px' && cs.backdropFilter === 'none' && cs.backgroundColor === 'rgb(11, 11, 46)', navText: nav.textContent, small,
        hrefs: [...nav.querySelectorAll('a')].map((a) => a.getAttribute('href')).join(' '),
        cap: /sample data/i.test(document.querySelector('.hero .dash')?.getAttribute('aria-label') || '') && /sample data/i.test(document.querySelector('.hero .mockcap')?.textContent || ''),
        feedback: /share feedback/i.test(document.body.textContent) };
    });
    check(`one h1, size >= 40px @${w}`, hero.h1s === 1 && hero.h1fs >= 40, `(${hero.h1fs})`);
    check(`nav sticky, solid @${w}`, hero.sticky);
    check(`nav has no Challenges link, no Share feedback @${w}`, !/challenges/i.test(hero.navText) && !hero.feedback);
    check(`nav links are exactly spec §0 @${w}`, hero.hrefs === '#top #why #flow #dashboard #habits #start https://github.com/dalhhorn-ship-it/danfactory', `(${hero.hrefs})`);
    check(`nav/hero targets >= 44px @${w}`, hero.small.length === 0, hero.small.join(', '));
    check(`dash mock labelled sample data @${w}`, hero.cap);
    // magenta text must be large and bold/display
    const mag = await page.evaluate(() => {
      const bad = []; const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      for (let n; (n = w.nextNode());) {
        if (!n.textContent.trim()) continue;
        const el = n.parentElement; const cs = getComputedStyle(el);
        if (cs.display === 'none' || cs.color !== 'rgb(230, 0, 126)') continue;
        if (el.closest('[aria-hidden="true"]')) continue;
        const big = parseFloat(cs.fontSize) >= 24, bold = +cs.fontWeight >= 700 || cs.fontFamily.includes('Archivo Black');
        if (!big || !bold) bad.push(`${el.tagName}.${el.className} ${cs.fontSize}`);
      }
      return bad;
    });
    check(`magenta text is large + bold @${w}`, mag.length === 0, mag.join(', '));
    // first Tab focuses the skip link
    await page.keyboard.press('Tab');
    check(`first Tab focuses skip link @${w}`, await page.evaluate(() => document.activeElement?.classList.contains('skip')));
    await ctx.close();
  }

  // JS off: content present, copy buttons hidden
  const off = await browser.newContext({ javaScriptEnabled: false, viewport: { width: 375, height: 667 } });
  const po = await off.newPage();
  await po.goto(origin + '/');
  const offInfo = await po.evaluate(() => ({
    h1: !!document.querySelector('h1'),
    btns: [...document.querySelectorAll('.copy')].map((b) => getComputedStyle(b).display),
    pre: document.querySelectorAll('.code pre').length,
  }));
  check('JS off: content present', offInfo.h1 && offInfo.pre > 0);
  check('JS off: copy buttons hidden', offInfo.btns.length > 0 && offInfo.btns.every((d) => d === 'none'));
  await off.close();

  // JS on: copy writes data-copy to the clipboard, aria-live status announces
  const on = await browser.newContext({ viewport: { width: 1280, height: 800 }, permissions: ['clipboard-read', 'clipboard-write'] });
  const pn = await on.newPage();
  await pn.goto(origin + '/');
  const btn = pn.locator('.copy').first();
  check('JS on: copy button visible', await btn.isVisible());
  const want = await btn.getAttribute('data-copy');
  await btn.scrollIntoViewIfNeeded();
  await btn.click();
  check('JS on: clipboard holds data-copy', (await pn.evaluate(() => navigator.clipboard.readText())) === want);
  check('JS on: "Copied" status announced', (await pn.locator('[role=status]').textContent()) === 'Copied');
  // challenge files are served as text
  for (const f of fs.readdirSync(path.join(PUB, 'challenges'))) {
    const r = await pn.request.get(`${origin}/challenges/${f}`);
    check(`challenge ${f} is 200 text/*`, r.status() === 200 && (r.headers()['content-type'] || '').startsWith('text/'));
  }
  await on.close();
} finally {
  await browser.close();
  server.close();
}
for (const f of failures) console.log('FAIL ' + f);
console.log(`${passed} passed, ${failures.length} failed`);
process.exit(failures.length ? 1 : 0);
