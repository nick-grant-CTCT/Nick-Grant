# Nick preferences (judgment layer)

CTCT-2024 tokens, the Empty Slide template, and the builder stay fixed.
This file personalizes **story judgment, density, phrasing, and audience shape**.
Read after [tokens.md](tokens.md) / [layouts.md](layouts.md); never override brand tokens here.

## Story shapes by use

| Use | Prefer | Avoid |
|-----|--------|--------|
| Weekday delivery briefing | Snapshot wells + takeaway cards once + EM/PM/PjM `draw()` figures | Reusing briefing shape for other uses; separate Asks `twoCol`; collector mechanics |
| Status / programme board | Named columns or lanes for named work; one accent for the ask | Status-well triplets when the sentence lists programmes by name |
| Decision / justification | Comparison panels or a single decisive figure + clear ask | Bullets that restate the figure; decorative product icons |
| Handoff / onboarding | Sequence or wave figure designed for that sentence (`draw()`) | Pouring into wells + chevrons + product grid because recipes exist |
| Product lineup | Isometrics **only** for products the slide names | Nearby ECU / display / radio as decoration |

## Density and hierarchy

- **Figure first.** The figure is the slide; text is the caption. One-line summary under the title, then the figure.
- Prefer **one dominant visual** per content slide. Do not stack a second text recipe beside it.
- Titles: **outcome-led** where possible (“What shipped”, “Where we are blocked”), not process labels (“Update”, “Notes”).
- Keep body copy short. If a slide needs a long explanation, split the story across slides instead of cramming cards.

## Title photos

- Photorealistic, CTCT-domain (machines, jobsite, displays, control tech).
- Calm **left** third for white title type; no baked-in text or logos.
- Match the deck topic; do not reuse a generic landscape or the template default photo.

## Phrasing

- Slide titles = the outline sentence (hard rule 14). Do not rewrite the sentence to fit a recipe.
- Meta line: `Programme  |  D Month YYYY` (or audience equivalent).
- Jira keys stay as orange underlined links after draw — do not hide keys in prose without the key form.

## Audience must-haves

### Morning briefing
Copy [examples/morning-briefing.js](examples/morning-briefing.js) **only** for a weekday delivery briefing.
- Snapshot wells match the report’s 🟢/🟡/🔴 counts.
- Takeaway cards once; isometric only when the takeaway names that product.
- Engineering, product, and project-manager figures via `draw()`.
- Asks live on the project-manager figure — no separate Asks slide recipe.

### Unite / programme readout
Story outline first. Prefer named work and decisions over status chrome.
See [examples/WHEN-TO-COPY.md](examples/WHEN-TO-COPY.md) and [examples/programme-readout.js](examples/programme-readout.js).

### Agent-designed layouts
When no recipe matches the sentence, follow [examples/onboarding-waves.js](examples/onboarding-waves.js): own `draw()` figures, kit tokens only.

## Encoded taste (from past critiques)

These already failed in real decks — treat as hard preferences:

1. Do not walk layouts as a menu (wells → panels → chevrons → stacked columns → product grid).
2. Do not copy the morning-briefing spec for a non-briefing use.
3. Do not put Asks on a separate `twoCol`.
4. Do not decorate concepts with the wrong isometric (`EC520`, `WIN10 Display`, `Radio Antenna` as filler).
5. Do not use letter hex chips (`BL`, `QA`) as icons.
6. Do not put collector mechanics on slides (“Jira confirmed”, “via gh”, “Jenkins main”).
7. Do not draw a one-bar “trends over time” slide when history is only today.
8. Do not reuse the same text recipe (`cards` / `rows` / `twoCol` / `bullets`) across slides.
9. Square corners only (`RECTANGLE`) for agent-drawn cards, panels, wells, nodes.

## How to extend this file

After a deck critique, add only **durable** preferences (seen twice or once but severe).
Write commands, not vibes. Log one-offs in [fail-log.md](fail-log.md) until they earn a place here.
