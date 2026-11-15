# PRD: Landing page: danfactory v0.2.0 features and system diagram

> Status: approved · 2026-11-15 · by user in chat ("1. svg is ok, 2. ok, [3] ok separate section, 4. ok"): inline SVG, keep the 7-step figure, separate section, Layers of safety as own list · Owner: product-manager · Backlog: M2 → UPD-4

## Problem
#autonomy and #example cover the three controls and the pilot, but not what v0.2.0 actually ships: the 11 merge-gate checks, locked acceptance tests, issue ledger, fixer caps, release train, learning loop, lean-by-default. Dan's brief (danfactory tag v0.2.0, 7428d46) lists them with a diagram prompt. Claims in docs/claims-v0-2-0.md are anchored to 4c6a68d, before the tag.

## Goal and success measure
Visitors see, in one scroll, how agents work between the three human controls and which safeguards bound them. Success: every new claim checkable at 7428d46; page budgets and checks stay green.

## Scope
1. Copy for the features in the brief that the page lacks (list above), plain words, no claim beyond the brief or danfactory.
2. One system diagram: hand-built inline SVG in the page's tokens (light and dark), same flow as the brief; 390px gets a stacked or simplified layout, no horizontal scroll. Alt text from the brief; "Layers of safety" also available as text.
3. Re-anchor docs/claims-v0-2-0.md to 7428d46, re-verify old claims, add new ones (danfactory added read-only at build time).

## Non-goals
Claims beyond the brief/danfactory; lpdan turning on autonomy; raster image generation here; new JS or external requests.

## Acceptance criteria
1. Given docs/claims-v0-2-0.md, when read, then it names 7428d46 and every sentence in the new copy maps to a file or line there.
2. Given the 11 gate checks, 3 attempts, 5 USD/day, 2 USD/run, 4 parallel, ~4,800 lines on the page, then each equals the danfactory value at the tag.
3. Given JS disabled, then all copy, diagram and legend render.
4. Given check_page, smoke and a11y runs, then all pass.
5. Given 390px and 1440px in light and dark, then screenshots show no h-scroll, legible labels and contrast.
6. Given the diagram, then it has a title/desc and the brief's alt text, and zero external requests.

## Risks and assumptions
Riskiest: the diagram stays legible at 390px. Test with a stacked variant first. Brief's navy palette clashes with light mode, so tokens win. Tag may differ from 4c6a68d in the pilot numbers; re-check.

## Effort and sequencing
M. Slices: claims re-anchor, then copy, then diagram. Depends on danfactory read-only checkout. Branch and preview, Dan approves the merge.

## Open questions
1. Diagram: inline SVG in page tokens (recommended, no-JS, themed) or Dan supplies a PNG from the prompt (fixed navy, needs a dark frame in light mode)?
2. Existing 7-step figure: keep and add the new diagram (recommended, they answer different questions) or replace it?
3. Placement: ~~block inside #autonomy~~ → **decided: separate section** after #autonomy.
4. "Layers of safety": own numbered list beside or under the diagram (recommended, accessible and works at 390px) or only drawn in the figure?
