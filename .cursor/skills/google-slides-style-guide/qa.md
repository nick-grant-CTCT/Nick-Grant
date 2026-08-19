# Deck QA Gate

Every deck must pass this gate **before** sharing, Drive sync of deliverables, or
Chat notify. Fail closed: fix, re-render thumbnails, and re-check until pass.

The builder (`node scripts/new-deck.js`) runs the automated checks and prints a
QA summary. Agents must still complete the visual thumbnail checklist. Automated
`ok: true` is not a visual pass.

## 1. Automated checks

Run against the live presentation (`slides.presentations.get` with
`pageSize`, slides, and layouts).

| Check | Pass criteria |
|-------|----------------|
| Page bounds | Every agent-drawn or text element stays inside the page (tolerance ≤ 0.02") |
| Content band | Drawn content stays within `y≈2.0`–`5.05` on content slides — **hard fail** |
| Placeholders | No leftover `[…replace me…]` / `[Slide title` instruction text |
| Empty text | Title, centered title, and subtitle placeholders are not empty |
| Text collisions | Inherited text boxes do not overlap |
| Title photo | Title **layout** photo is full-bleed (≥8×4 in). Tiny slide-level images do not count |
| Visual presence | Content slides need a real figure (`draw()`, `panels`, `chevrons`, `cards`, `twoCol`). An isometric is optional and only valid when the slide names that product. **Letter hex chips on `rows`/`bullets` are not icons** and hard-fail unless `qaAllowLabelChips` is set on example specs |
| Square corners | Agent-drawn cards, panels, wells, and nodes are `RECTANGLE`. `ROUND_RECTANGLE` hard-fails (the template CONFIDENTIAL pill is inherited chrome, not agent-drawn) |

Builder exit code is non-zero on any of the failures above.

```bash
node scripts/new-deck.js spec.js
```

Story-shape checks run **before** draw:

- Snapshot / trend / metric titles may not use `cards`, `rows`, `bullets`, or `twoCol`
- The same text recipe may not be reused across slides
- A deck of three or more content slides may not be text-recipe-only

## 2. Visual thumbnail checklist

Render every slide (the builder writes LARGE PNGs). **Read** each image. Mark
pass/fail:

| # | Check |
|---|--------|
| V1 | No clipped text, overlaps, or elements colliding with footer / CONFIDENTIAL / logo |
| V2 | Hierarchy clear: title > one-line summary > body |
| V3 | Margins and whitespace look intentional (not cramped, not sparse empty cards) |
| V4 | Functional-area colours match [functional-areas.md](functional-areas.md) when areas are named |
| V5 | Icons only where the slide names that product; stroke weight consistent; no emoji |
| V6 | Icons are isometric product PNGs from the product-components library **and match the named box**; not devices SVGs, not monoline chips, not a nearby ECU/display/radio used as decoration |
| V7 | Diagrams: labels readable at thumbnail size; arrows unambiguous; ≤8 nodes |
| V8 | Title photo: photorealistic, text-free, calm left side, on-topic for CTCT + deck |
| V9 | Corners are square (`RECTANGLE`). The figure is the outline sentence. Do not FAIL a slide for lacking an isometric when the sentence is not about a catalog product |

### Encoded visual fail notes (from critiques)

Treat these as automatic V-fails even if a checklist row is ambiguous:

- **V2 / V3:** A content slide that is mostly empty cards or a second text recipe beside the figure → FAIL (figure should dominate; see [preferences.md](preferences.md) density).
- **V5 / V6:** Any `EC520`, `WIN10 Display`, or `Radio Antenna` isometric on a slide that does not name that product → FAIL.
- **V5:** One- or two-letter hex chips (`BL`, `QA`, …) used as icons → FAIL (unless `qaAllowLabelChips` on an example spec).
- **V9 / story:** Morning-briefing layout (snapshot wells + takeaway cards + audience wells) on a non-briefing use → FAIL story-format; rebuild from outline.
- **Audience:** Separate Asks `twoCol` on a weekday briefing → FAIL; asks belong on the project-manager figure.
- **Audience:** Collector mechanics text (“Jira confirmed”, “via gh”, “Jenkins main”) on slides → FAIL.
- **Trends:** Single-bar “over time” figure when only today’s point exists → FAIL; use a snapshot figure instead.

## 3. QA result (required before done)

```
QA
  slide 1 title     PASS
  slide 2 cards     PASS (icons: 3)
  slide 3 custom    PASS (timeline)
  automated         PASS (0 overflows, 0 placeholders, 0 visual fails)
```

Do not declare the deck complete while any slide is FAIL.

## 4. Morning report / other skills

Consumers must use **this** checklist, the CTCT-2024 tokens in
[tokens.md](tokens.md), and [preferences.md](preferences.md). Do not reintroduce
alternate palettes, skip thumbnail inspection, or map a briefing onto
`cards` + `rows` + `twoCol`. Snapshot, trend, and audience slides need `draw()`
or a figure recipe. Morning briefings add engineering, product, and project
manager figures (see [examples/morning-briefing.js](examples/morning-briefing.js))
and must not add a separate Asks `twoCol`. To keep a posted URL, set
`presentationId` on the spec and rebuild with `new-deck.js`.

After QA, if anything failed visually, append [fail-log.md](fail-log.md) before
sharing the next similar deck.
