# When to copy which example

Pick **one** starter by use. Do not mix morning-briefing chrome into a programme readout, and do not invent a parallel builder.

| Use | Copy | Notes |
|-----|------|--------|
| Weekday delivery / morning briefing | [morning-briefing.js](morning-briefing.js) | Snapshot wells match 🟢/🟡/🔴; takeaway `cards` once; EM/PM/PjM via `draw()`; no separate Asks `twoCol` |
| Agent-designed figure (handoff, waves, custom sequence) | [onboarding-waves.js](onboarding-waves.js) | Story sentence → own `draw()`; kit tokens only; promote to layouts only after a third similar deck |
| Unite / programme board / named-work readout | [programme-readout.js](programme-readout.js) | Named columns/lanes for named programmes; decision accent; not status-well triplets |
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
- Walking [layouts.md](../layouts.md) top-to-bottom as a menu.
- Adding `qaAllowLabelChips` outside example/self-check decks.
