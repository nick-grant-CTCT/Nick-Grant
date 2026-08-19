# Layout design

Finish the per-slide outline in [SKILL.md](SKILL.md) and check [preferences.md](preferences.md) **before** using anything below. Patterns are a **vocabulary**, not a menu.

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
| Change over time | Columns per period; lines only for continuous measures |
| Split of a whole | One 100% bar per measure |
| A few options side by side | Colour-headed panels — only if the sentence is a comparison |
| A sequence of stages | Chevron rail — only if the sentence is a sequence |
| Components and connections | System/flow diagram |
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
| Programme board + decision | See programme-readout.js |

Do **not** walk this file top to bottom and pour the story into every recipe.
