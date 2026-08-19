# Deck fail log

Capture critique after each deck. Encode a row into [preferences.md](preferences.md), [SKILL.md](SKILL.md) **Do not**, or [qa.md](qa.md) when the same miss appears twice (or once if severe).

## How to log

After thumbnails + V1–V9:

```
### YYYY-MM-DD — <deck title or presentationId>
- Slide / intent: …
- What looked wrong: …
- Miss type: token | story-format | hierarchy | icon | recipe-menu | audience | other
- Encode to: preferences | SKILL Do not | qa V-note | examples | (hold)
- Fix applied: …
```

## Miss → encode map

| Miss type | Encode into |
|-----------|-------------|
| Brand token / type / corners | [tokens.md](tokens.md) or **Hard rule** / **Do not** in SKILL.md |
| Wrong figure for the sentence | Story first / hard rule 14; anti-pattern under **Do not** |
| Visual hierarchy / whitespace / icons | Concrete V-check or fail example in [qa.md](qa.md) |
| Recurring composition that worked | Keep in deck `draw()`; promote to layouts/examples only after a **third** similar use |
| New use case | New file under `examples/` + WHEN-TO-COPY row |
| Durable taste (density, phrasing, audience) | [preferences.md](preferences.md) |

Write **commands**, not vibes: “Do not put Asks on a separate `twoCol`” beats “prefer cleaner briefings.”

## Already encoded (seed from past critiques)

These failures are already in preferences / SKILL / QA — do not re-log unless a regression appears:

| Failure | Encoded in |
|---------|------------|
| Recipe menu-picking (wells→panels→chevrons→grid) | SKILL hard rule 7, preferences encoded taste #1 |
| Morning-briefing spec reused for other uses | SKILL Do not, preferences audience table |
| Separate Asks `twoCol` on briefing | SKILL Do not, preferences #3, qa §4 |
| Wrong isometric decoration (EC520 / display / radio) | SKILL hard rule 12 / Do not, preferences #4, qa V5–V6 |
| Letter hex chips as icons | SKILL Do not, preferences #5, automated visual presence |
| Collector mechanics on slides | SKILL Do not, preferences #6 |
| One-bar trend with only today | SKILL Do not, preferences #7 |
| Same text recipe reused across slides | SKILL hard rule 7, preferences #8, story-shape checks |
| `ROUND_RECTANGLE` on agent-drawn shapes | SKILL hard rule 9, preferences #9, automated square-corners |

## Open log

<!-- Append new entries below. Move to “Already encoded” after editing skill files. -->

_None yet — append after the next deck critique._
