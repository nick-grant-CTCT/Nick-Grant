# When to copy which example

Pick **one** starter by use. Do not mix morning-briefing chrome into a programme readout, and do not invent a parallel builder.

| Use | Copy | Notes |
|-----|------|--------|
| Weekday delivery / morning briefing | [morning-briefing.js](morning-briefing.js) | Snapshot wells match 🟢/🟡/🔴; takeaway `cards` once; EM/PM/PjM via `draw()`; no separate Asks `twoCol` |
| Feature / product roadmap (single delivery path) | [feature-roadmap-road.js](feature-roadmap-road.js) | Winding road + pins; CTCT tokens; not swimlanes, not chevrons |
| Agent-designed figure (handoff, waves, custom sequence) | [onboarding-waves.js](onboarding-waves.js) | Story sentence → own `draw()`; kit tokens only; promote to layouts only after a third similar deck |
| Unite / programme board / named-work readout | [programme-readout.js](programme-readout.js) + Major Program live deck in [reference-decks.md](reference-decks.md) | Named columns/lanes; split prose vs metrics; owner line on title; not status-well triplets |
| GEM / exec value narrative (V3 Unite) | Live **Draft GEM slides** in [reference-decks.md](reference-decks.md) | Now→Next → value bars → numbered Change+Why → roadmap swimlanes; compose with `draw()`, do not clone the file |
| Brand layout gallery / chrome | Live **CTCT - Slide Template** in [reference-decks.md](reference-decks.md) | Type, section dividers, big stats, icon libraries — tokens still win |
| Recipe-only demos / skill self-check | [skill-deck.json](skill-deck.json) | May set `qaAllowLabelChips` for chip demos — do not copy that flag into real decks |
| Simple flow / system diagram | [flow-diagram.json](flow-diagram.json) | Only when the outline sentence is already a flow |
| Licensing / Unite R1 style recipe deck | [unite-r1-licensing.json](unite-r1-licensing.json) | Recipe fit only; rewrite outline if recipes fight the story |
| V3 supportability narrative | [v3-supportability.json](v3-supportability.json) | Topic reference; still story-first before recipes |

## Promotion rule

1. Ship the figure in the deck’s own `draw()` first.
2. If a **second** deck needs the same shape, keep copying the prior spec’s `draw()`.
3. Only on a **third** similar use: add a short note to [layouts.md](../layouts.md) and optionally a kit helper in `scripts/deck.js`.

## Anti-patterns

- Copying `morning-briefing.js` because you need “status” (use programme-readout or a custom `draw()`).
- Copying GEM swimlanes or chevrons because the user said “roadmap” (if it is one feature path, copy [feature-roadmap-road.js](feature-roadmap-road.js)).
- Walking [layouts.md](../layouts.md) top-to-bottom as a menu.
- Adding `qaAllowLabelChips` outside example/self-check decks.
