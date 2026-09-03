---
name: google-slides-style-guide
description: >-
  Builds on-brand CTCT Google Slides from the Empty Slide template using
  scripts/new-deck.js, CTCT-2024 tokens, layout composition, Nick preferences,
  and a fail-closed QA gate. Use when creating, restyling, or updating a CTCT,
  Unite, or programme slide deck, morning briefing slides, weekday delivery
  briefing, Unite readout, programme board, product roadmap, feature roadmap,
  delivery timeline, winding-road feature path, or any Google Slides
  deliverable that must look like CTCT Brand 2024.
---

# CTCT Google Slides

Build every deck with this skill's builder. Do not hand-roll slides, Apps Script, or a local Python/Slides API builder.

## Story first

The agent needs to figure out the story and slide format best for each use.

Do that **before** opening the recipe list or copying an example spec.

1. Write the deck as an outline: one title and one sentence per slide. That outline **is** the story. Do not pick a `kind` yet.
2. For each slide, choose the format that sentence needs. A weekday briefing, a justification, a handoff, and a product lineup are different uses. Do not reuse the morning-briefing shape for another use.
3. Only then read [layouts.md](layouts.md) for how CTCT figures look, and compose with `draw()` or a recipe that actually matches that sentence.
4. When the use matches a live reference deck (GEM narrative, major programme board, brand gallery), open [examples/reference-decks.md](examples/reference-decks.md) and match that deck’s story shapes and density — do not screenshot-copy slides.

Fail the outline, not the recipe, if they disagree. If the sentence is a named list of programmes, draw the names. Do not replace names with wells, a 100% bar, or a product-icon grid because those recipes exist. If the sentence is **features we deliver along one path**, draw the winding-road figure — not swimlanes and not chevrons.

## Before drawing

Read these companions in this order:

1. [template.md](template.md) — copy Empty Slide, object IDs, photo pipeline, `draw()` + kit
2. [tokens.md](tokens.md) — CTCT-2024 palette and type. **These tokens win any conflict.**
3. [layouts.md](layouts.md) — figure vocabulary after the outline exists; recipes are not a menu
4. [examples/reference-decks.md](examples/reference-decks.md) — live style/layout references (GEM, major programme, CTCT template)
5. [qa.md](qa.md) — automated + visual gate
6. [assets.md](assets.md) and [functional-areas.md](functional-areas.md) when icons or org areas appear
7. [preferences.md](preferences.md) — Nick judgment layer (story shapes, density, audiences). Does not override tokens.

## Tokens (do not substitute)

| Role | Value |
|------|--------|
| Brand orange | `#FF8B00` (theme `ACCENT2`) |
| Body / heading | `#595959` (theme `DARK1`) |
| Card fill | `#F2F2F2` |
| Display | Proxima Nova Bold, slide titles **22–25pt** |
| Body | Inter 12–14pt |
| Canvas | 16:9, **10 × 5.625 in** (query `pageSize`; never assume 7.5 in tall) |

Do not use `#FF6B00`, white card fills, 28–32pt titles, or a plain off-white canvas. Those belong to a leftover prompt, not CTCT 2024.

## Hard rules

1. **Copy the template.** Every new deck is `drive files copy` of Empty Slide (`1Bl1tpH-fqY_vUW8_B2vBcAPkJbVOsMMUlIB5l7u-QYs`). Update slide 1 and slide 2; duplicate slide 2 for more pages. Never delete the two starter slides. Never edit the template file.
2. **Do not draw chrome.** Slide numbers, CONFIDENTIAL badge, cube logo, honeycomb, title scrim and orange rule come from the layout. Do not recreate them.
3. **Fresh title photo.** Generate a photorealistic CTCT-domain photo (≥800×450), no baked-in text, calm left side for white title type. Swap it onto the **layout** photo with `replaceImage` + `CENTER_CROP`.
4. **Builder only.** `node scripts/new-deck.js <spec.json|spec.js>` from this skill folder (or an equivalent wrapper that calls that file). No second builder.
5. **In-place updates.** To keep an existing URL, set `presentationId` in the spec. The builder rebuilds that deck. Do not invent a parallel script.
6. **Hard rule 14 — story, then format.** The outline from **Story first** wins. Write a `.js` spec with `draw(r, page, ctx)` and `ctx.kit` whenever the sentence is not already a stock recipe. See [examples/feature-roadmap-road.js](examples/feature-roadmap-road.js) for a single-path feature roadmap. See [examples/onboarding-waves.js](examples/onboarding-waves.js) for other invented figures. See [examples/morning-briefing.js](examples/morning-briefing.js) only when the use **is** a weekday delivery briefing.
7. **Recipes are not a menu.** Do not walk [layouts.md](layouts.md) and pour the story into wells, panels, chevrons, stacked columns, and a product grid. `cards`, `rows`, `bullets`, `twoCol` are last-resort shortcuts. Morning briefings may use `cards` once for takeaways. Do not add a second text recipe for asks. Do not reuse the same text recipe across slides. Do not map a whole briefing onto cards + rows + twoCol.
8. **Hard rule 12 — visuals that belong.** Every content slide needs a real figure for **that sentence**. An isometric product PNG is only valid when the slide is about that box. Do not decorate a concept, a kill, or a named programme with a nearby product. Missing art is better than the wrong product. No emoji. No letter hex chips (`BL`, `QA`). Do not use the devices SVG library or monoline template chips when an isometric exists **and matches**.
9. **Square corners.** Cards, panels, wells, insight boxes, and process nodes are `RECTANGLE`. Do not use `ROUND_RECTANGLE`. The CONFIDENTIAL pill is template chrome — do not recreate it.
10. **QA fail closed.** Automated QA must pass, then inspect every LARGE thumbnail against [qa.md](qa.md) V1–V9. Do not share, Drive-sync, or Chat-notify on FAIL. Do not treat warnings as a pass.
11. **Jira keys are links.** After drawing, every `\b[A-Z][A-Z0-9]+-\d+\b` key is an orange underlined link to `https://ctctjv.atlassian.net/browse/<KEY>`.
12. **Preferences.** Apply [preferences.md](preferences.md) for audience shape, density, and phrasing. If a preference conflicts with tokens or hard rules 1–11, tokens and hard rules win.

## Build

```bash
node scripts/new-deck.js spec.js      # preferred when any slide needs draw()
node scripts/new-deck.js spec.json    # only when every content slide is a true recipe fit
```

New deck:

```json
{
  "title": "Drive file name",
  "deckTitle": "On-slide title",
  "meta": "Programme  |  D Month YYYY",
  "folderId": "Unite-or-target-Drive-folder-id",
  "background": "generated-title-photo.png",
  "slides": []
}
```

Keep a posted Chat URL:

```json
{
  "presentationId": "existing-file-id",
  "background": "generated-title-photo.png",
  "slides": []
}
```

The builder writes `.tmp/presentation.json` (id, url, thumbs, qa) when that directory exists, or `spec.manifestPath`.

## Workflow

1. Outline the story (title + one sentence per slide). Choose a format per slide from that sentence. Check [preferences.md](preferences.md) for audience must-haves.
2. Generate a new title photo for this deck.
3. Compose each content slide. Pick the example to copy with [examples/WHEN-TO-COPY.md](examples/WHEN-TO-COPY.md), and align density/shapes with [examples/reference-decks.md](examples/reference-decks.md):
   - [examples/morning-briefing.js](examples/morning-briefing.js) **only** for a weekday delivery briefing
   - [examples/feature-roadmap-road.js](examples/feature-roadmap-road.js) for a single-path feature / product roadmap (winding road + pins)
   - [examples/onboarding-waves.js](examples/onboarding-waves.js) when inventing other `draw()` figures
   - [examples/programme-readout.js](examples/programme-readout.js) for Unite / programme board readouts
   - Live GEM / major-programme decks in reference-decks.md when the outline is that use (GEM parallel-track roadmaps stay swimlanes)
4. Run `new-deck.js`. Fix automated failures before anything else.
5. Read every thumbnail. Record per-slide V1–V9 pass/fail.
6. Only then share, move to Drive, or notify.
7. If anything looked wrong, append [fail-log.md](fail-log.md) and encode repeats into preferences / hard rules / QA (see README Skill improvement).

## Do not

- Start from wells / panels / chevrons / stacked columns / a product grid and then find content to fill them
- Copy the morning-briefing spec for a use that is not a weekday delivery briefing
- Put an isometric on a slide that does not name that product
- Reuse `EC520` / `WIN10 Display` / `Radio Antenna` as decoration
- Use `ROUND_RECTANGLE` for cards, panels, wells, or nodes
- Hand-roll shapes onto a blank presentation
- Keep a default template landscape photo
- Declare QA passed from overflow checks alone
- Skip `template.md` / `tokens.md` / `layouts.md` / `preferences.md` / `examples/reference-decks.md`
- Screenshot-copy slides from reference decks into a new presentation (compose with the builder instead)
- Use a local `.tmp/build_*.py` or other ad-hoc Slides client
- Map a briefing onto `cards` + `rows` + `twoCol`
- Treat one- or two-letter hex chips as icons
- Use devices-library SVGs or monoline template chips when a matching isometric exists
- Put collector mechanics on a briefing (“Jira confirmed”, “via gh”, “Jenkins main”)
- Draw a one-bar “trends over time” slide when theme history has only today
- Add a separate Asks `twoCol` on a morning briefing (asks live on the project-manager figure)
- Use chevrons or GEM swimlanes when the sentence is a **single** feature-delivery path (use the winding-road `draw()` instead)
- Recreate the winding-road figure with pastel stock colours or `ROUND_RECTANGLE` cards
