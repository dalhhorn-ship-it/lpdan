# 0006 — Sync to danfactory template 1.2.0 by three-way merge; publish template evals with a label

> Status: accepted (Dan approved docs/specs/template-update-2026-11.md in chat, 2026-11-11) · Date: 2026-11-11

## Context
lpdan was created from danfactory at decision tree 1.1.0 and last synced at 2edcba8. Template 9cb70c5 (1.2.0) adds behavioural evals, an Evals tab, roadmap views, a Carbon-styled dashboard, a Delivery card, the auto-compact handoff loop and security hardening. lpdan has local edits to 41 template files, including its own SEC-001..003 fixes (d2ba4f0) to the same security files the template hardened independently.

## Options
1. **Overwrite with the template.** Simple, but it loses lpdan's own changes (Deploy and Security tabs, deny rules, docs_index --related).
2. **Three-way merge per file.** The base is the template version closest to lpdan's file. Files lpdan never changed are taken as-is. Conflicts are resolved by hand.
3. **Port by feature only.** Safest for a single feature, but too slow for 100+ files.

## Decision
Option 2. Where the security files conflicted (bash guard, adopt, cf_scaffold, deploy template, ship skill, security policy), the template's hardened version wins, and lpdan's own SEC regression tests must still pass against it. settings.json takes the template's hooks and deny rules plus lpdan's extra wrangler deny rules. factory.json gets the `evals` and `dashboard` blocks, version 1.2.0, and pinned skill refs. lpdan's project, deploy and dashboard URL values are kept. dashboard.py starts from the template's version, and lpdan's Deploy and Security tabs move to `scripts/obs/tab_*.py`.

lpdan has no eval runs of its own. The public Evals tab shows danfactory's `metrics/evals.jsonl` and baseline, labelled "danfactory template evals". The page's numbers come from that file, are not presented as README quotes, and are checked against a fixture by `tests/check_page.py`.

## Consequences
- `templates/deploy-cloudflare.yml` (for new projects) now has no preview job, because route A is the template default. lpdan's live `.github/workflows/deploy-cloudflare.yml` is lpdan's own, is unchanged, and still follows ADR 0003.
- `tests/fixtures/` now holds the README, evals.jsonl and evals policy at 9cb70c5. Refresh them at the next sync.
- The public dashboard filters SEC-n and security items out of the data before any view renders.
