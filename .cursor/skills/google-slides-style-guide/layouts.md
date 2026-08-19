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
| Near-term roadmap with parallel workstreams | Swimlane timeline (spikes / builds / UX / UA) |
| Cost or effort multiplier | Big metric callouts on their own slide; keep the prose argument on the prior slide |
| Change over time | Columns per period; lines only for continuous measures |
| Split of a whole / machine mix | One 100% bar or labelled % composition (Major Program data slide) |
| A few options side by side | Colour-headed panels — only if the sentence is a comparison |
| A sequence of stages | Chevron rail or phase timeline — only if the sentence is a sequence |
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
| Programme board + decision | See programme-readout.js + Major Program reference deck |
| GEM value / UX / roadmap narrative | `draw()` matching Draft GEM patterns in reference-decks.md |

Do **not** walk this file top to bottom and pour the story into every recipe.
