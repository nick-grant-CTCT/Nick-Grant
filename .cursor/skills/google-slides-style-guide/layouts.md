# Layout design

Finish the per-slide outline in [SKILL.md](SKILL.md) and check [preferences.md](preferences.md) **before** using anything below. Patterns are a **vocabulary**, not a menu. For live GEM / programme / brand examples, also open [examples/reference-decks.md](examples/reference-decks.md).

## Designing a layout for the story

1. Keep the outline sentence as the title.
2. Ask what shape that sentence is — named work, change over time, comparison, sequence, split of a whole, relationship, or a single number.
3. Pick or invent the figure that shows that shape; size it to dominate the content band.
4. Reserve one accent (brand orange) for the point.
5. Label directly on the figure.
6. Check the figure survives a thumbnail.

| The sentence is about | Figure that often shows it |
|-----------------------|----------------------------|
| Named work and how it ended | Named columns, lanes, or a compact register — not a substitute chart |
| Today vs platform / previously vs next | Paired comparison bars or columns (GEM value slide); emotional Now→Next bridge first when the story needs it |
| Numbered changes with rationale | Numbered panels: name + Change + Why (GEM UX slide) |
| Problems and matching strategy | Two columns of numbered items that answer each other |
| Near-term roadmap with parallel workstreams | Swimlane timeline (spikes / builds / UX / UA) — GEM reference only |
| Features we deliver along a path | Winding-road `draw()` with pins — see [feature-roadmap-road.js](examples/feature-roadmap-road.js) |
| Cost or effort multiplier | Big metric callouts on their own slide; keep the prose argument on the prior slide |
| Change over time | Columns per period; lines only for continuous measures |
| Split of a whole / machine mix | One 100% bar or labelled % composition (Major Program data slide) |
| A few options side by side | Colour-headed panels — only if the sentence is a comparison |
| A sequence of stages (process, not feature delivery) | Chevron rail or phase timeline — only if the sentence is a process sequence, not a product roadmap |
| Components and connections | System/flow diagram (isolation test / API bridge) |
| A single number that matters | Big stat in a well or outlined card |

If the composition is reusable, leave it in the deck spec first. Promote into `scripts/deck.js` / this file only when a **third** deck needs it. See [examples/WHEN-TO-COPY.md](examples/WHEN-TO-COPY.md).

## Recurring builder kinds (not a picker)

Use a recipe **only** when the outline sentence is already that shape. Otherwise `draw()`.

| Slide intent | Recipe / approach |
|--------------|-------------------|
| Compare 2–4 options / named programmes side by side | `panels` or `draw()` register |
| Three takeaways (briefing only) | `cards` **once** |
| Outcome snapshot (briefing only) | `draw()` status wells matching 🟢/🟡/🔴 |
| Custom sequence / waves / handoff | `draw()` — see onboarding-waves.js |
| Single-path feature / product roadmap | `draw()` winding road — see feature-roadmap-road.js |
| Programme board + decision | See programme-readout.js + Major Program reference deck |
| GEM value / UX / parallel-track roadmap | `draw()` matching Draft GEM patterns in reference-decks.md |

## Winding-road feature roadmap

Use this figure when the outline sentence is **named features we ship along one delivery path** (product roadmap, feature roadmap, “features on a road”). Do **not** use it for GEM parallel workstreams (those stay swimlanes).

Geometry (16:9, content band `y` ≈ 2.0–5.05 in):

1. Horizontal winding road: three peaks and two valleys (`cos(t · 4π)` for `t` in 0…1) when there are **5** pins. For **4** pins use `cos(t · 3π)` so pins still alternate peak / valley (see [site-contractor-roadmap.js](examples/site-contractor-roadmap.js)). Road fill `#555555`, **brand-orange** `#FF8B00` edge, white dashed centerline.
2. Default **5** pins (allow 4–6) at `t` = 0, 0.25, 0.5, 0.75, 1 — peaks and valleys, left-to-right delivery order.
3. Pin head = `ELLIPSE` (plus a small `TRIANGLE`/`RECTANGLE` stem). Cards, panels, and nodes stay `RECTANGLE`.
4. Info card above each pin: feature title + up to 3 bullets. Card fill `#F2F2F2`, heading `#595959`.
5. Stage colour: **one** brand-orange pin marks “now” / next delivery. Other pins cycle diagram accents `#00A3D6`, `#6AA84F`, `#A64D79`, `#555555`.
6. Copy from [examples/feature-roadmap-road.js](examples/feature-roadmap-road.js); rewrite the milestone list from the outline.

Do **not** walk this file top to bottom and pour the story into every recipe.
