---
name: product-strategy
description: >
  Build or revise a product strategy in any order and turn the confirmed
  parts into a product report-out slide deck. Use when the user wants to
  work a product strategy, vision, mission, direction, where we play, how
  we win, customer needs, SWOT, must-haves, stop list, resource allocation,
  initiatives, roadmap, or a strategy readout deck. Sections can be skipped,
  parked, or jumped to, and the deck can be rendered before every section
  is done.
---

# Product strategy

Facilitate a product strategy and, when asked, render a report-out deck. The framework order is the suggested path. It is not a waterfall. An empty or skipped section never blocks another section and never blocks the deck.

Write only what the user confirms. Never invent customers, metrics, evidence, markets, or initiatives to fill a gap.

The fixture at `fixtures/partial-strategy.yml` is only for checking the renderer. Never use it as starter content for a real strategy.

## Files

| Path | Role |
| --- | --- |
| `templates/strategy.yml` | Schema. Copy it on the first session. |
| `references/bands.md` | Questions, done bar, and failure modes. Read a section only when that section is open. |
| `scripts/render_deck.py` | Builds the PowerPoint. |
| `strategy/<slug>.yml` | The live strategy, in the workspace root (not inside this skill). |

`schema_version` stays `1`. Fill values. Do not add keys.

## Section keys

Use these keys in the file and in the status map. Accept the aliases in conversation.

| Key | Name | Aliases |
| --- | --- | --- |
| `frame` | Frame | frame, setup, audience |
| `vision` | Vision, mission, direction | vision, mission, direction |
| `where_we_play` | Where we play | where we play, markets, segments |
| `needs` | Customer needs and problems | needs, problems, customer needs |
| `how_we_win` | How we win | how we win, products, value proposition, UVP |
| `pillars` | Outcome pillars | pillars, goals, metrics, grow, interoperability, innovation |
| `swot` | SWOT | swot, strengths, weaknesses, opportunities, threats |
| `filters` | Decision filters | must haves, stop list, won't do, resources, resource allocation |
| `initiatives` | Initiatives and operational work | initiatives, bets, operational, projects |
| `roadmap` | Roadmap | roadmap, now next later |

Suggested order, used only to propose a next step: frame, vision, where_we_play, needs, how_we_win, pillars, swot, filters, initiatives, roadmap.

## Status

Each section has `status` and an optional `skip_reason`.

- `empty` — not started. This is the template default.
- `draft` — a draft is written, or the user wants to move on before the done bar is met.
- `confirmed` — the user accepted it and the done bar in `references/bands.md` is met.
- `skipped` — the user explicitly skipped it. Store a one-line `skip_reason` when they give one.

Park means leave the section `draft` or `empty` and move on. Do not mark a thin section `confirmed`. If the user says to lock it anyway, keep `draft`, name the unmet bar in one line, and move on.

Set `confirmed` only after the user accepts a draft that meets the bar.

## Start of a session

1. If `strategy/*.yml` exists, ask which file to resume when more than one exists. Otherwise open the only one.
2. If none exists, copy `templates/strategy.yml` to `strategy/<slug>.yml`. Derive `<slug>` from the product name when you know it, or use `strategy/draft.yml` until you do, then rename once.
3. Show a status map, one line per section: name, status, skip reason if any.
4. Ask where to work. Suggest the next `empty` section in suggested order. Accept a skip, a jump, or "build the deck" immediately.

## While a section is open

1. Read that section in `references/bands.md`. Do not read ahead and do not ask questions from other sections.
2. Ask a few questions at a time, not the whole list.
3. If an upstream section is `empty` or `skipped`, name that missing link once. Then continue. Leave the link blank, or store a working assumption the user actually states.
4. A working assumption is the user's words. Put those words in the link field and set `assumption` on that item to a one-line note. Do not invent the assumption.
5. Write the draft into the YAML and set `status: draft`. Show the draft in prose, not as raw YAML.
6. The user edits or accepts. Set `confirmed` only when they accept and the done bar is met.

Omit empty fields rather than writing placeholders. Empty lists stay `[]`.

## Moves the user can make at any time

After each section, offer four moves: next suggested section, jump, skip, or render. Also accept these whenever they are said.

- **Skip** ("skip SWOT"): set that section to `skipped`, keep `skip_reason` when given, and ask where to go next. Do not ask that section's questions.
- **Park**: leave status as it is (`empty` or `draft`) and move.
- **Jump** ("do the roadmap now"): open that section.
- **Return**: reopen a `skipped`, `draft`, or `confirmed` section. Replacing a skip clears `skip_reason` once new content is saved.
- **Render** ("build the deck"): render from the file as it stands. Do not require every section to be confirmed, and do not pause to fill gaps first.

If the user pastes an existing strategy, map it into the template, leave untouched sections `empty`, show the status map, and start where they point. Flag contradictions in one or two lines, then keep going.

## Rendering the deck

Run from the workspace root:

```bash
python3 .cursor/skills/product-strategy/scripts/render_deck.py strategy/<slug>.yml -o strategy/<slug>.pptx
```

The script depends on `python-pptx` and `PyYAML` (`scripts/requirements.txt`). Install them if the command fails on a missing module.

Check the renderer without using a real strategy:

```bash
python3 .cursor/skills/product-strategy/scripts/render_deck.py --self-check
```

The deck includes a title slide, one content slide per `draft` or `confirmed` section that has something to show, and a coverage slide. Initiatives render as up to two slides (product, then operational) when each list has items. `empty` and `skipped` sections are left out of the body and listed on the coverage slide. Blank links are listed there too. Draft slides are marked Draft.

Do not hand-edit the PowerPoint to add strategy the file does not contain.

Upload the deck to Google Drive only when the user asks.

## Done bar, short form

The full bar is in `references/bands.md`. Use it only for the open section.

- **Frame.** Product, horizon, audience, and the decision this strategy must unlock.
- **Vision.** Three different sentences. Vision has no features. Direction is a shift from X to Y that a team could choose against.
- **Where we play.** Markets, segments, and who is out. Each included market earns its place from the direction when a direction exists.
- **Needs.** Who, how often, cost of the status quo, and real evidence. Each need is owned or only acknowledged.
- **How we win.** Each product names a need when needs exist; otherwise the link stays blank. One value proposition per primary segment, naming the alternative.
- **Pillars.** One or two metrics per pillar, each with baseline, target, and owner, chosen from that pillar's menu.
- **SWOT.** About three items per quadrant. Each item names what it affects when that upstream section exists.
- **Filters.** Must-haves, stops that name what they protect, and a resource split across the three pillars that sums to 100.
- **Initiatives.** Each product initiative names the need, pillar metric, and must-have when those sections exist. Missing links stay blank.
- **Roadmap.** Now / next / later. Each item names the initiative or operational action it traces to when those exist, plus dependencies and the assumption that would reorder the plan.
