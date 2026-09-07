# CTCT Google Slides Style Skill

Cursor Agent skill that applies the CTCT 2024 visual system to Google Slides — brand tokens, layout recipes, Nick preferences, functional-area colour coding, and Drive asset libraries — so decks stay on-brand without manual restyling.

## Install

Copy this entire folder (all files together):

| Scope | Destination |
|-------|-------------|
| Personal (all projects) | `~/.cursor/skills/google-slides-style-guide/` |
| One repo (shared with teammates via git) | `.cursor/skills/google-slides-style-guide/` |

On Windows, personal skills live at:

`%USERPROFILE%\.cursor\skills\google-slides-style-guide\`

Required files:

- `SKILL.md`
- `preferences.md` (Nick judgment layer)
- `fail-log.md` (critique → encode log)
- `template.md`
- `tokens.md`
- `functional-areas.md`
- `layouts.md`
- `assets.md`
- `qa.md`
- `README.md` (this file)
- `scripts/` (`deck.js`, `new-deck.js`, `test-story-shapes.js`) — required to build decks
- `examples/` (worked specs + [WHEN-TO-COPY.md](examples/WHEN-TO-COPY.md))

If you already have a personal install with `scripts/` and older examples, merge this folder on top and keep your working `scripts/` and any local example photos.

Open a **new** Cursor chat after installing so the agent can discover the skill.

## Prerequisites

1. **Cursor** with Agent Skills available
2. **`gws` CLI** on your PATH, authenticated to Google Workspace (`gws auth login`)
3. **Drive access** to the CTCT logo, icon, and product libraries listed in `assets.md`
4. Optional: `gws-slides` / `gws-drive` agent skills — if missing, use `gws slides` and `gws drive` directly

## 60-second usage

In Cursor Agent chat, ask for example:

> Create a CTCT slide deck about Program X with a title slide, a status update, and a feature roadmap (winding road).

Or:

> Restyle this deck to CTCT 2024: [presentation URL or ID]

The agent copies the CTCT `Empty Slide` template (or rebuilds `presentationId`
in place), updates its preserved title and first content slides, duplicates the
content slide for additional pages, generates a topic-specific title photo,
composes figures with `draw()` when recipes do not fit, applies
[preferences.md](preferences.md), runs fail-closed automated QA, and verifies
every thumbnail.

For a scripted build, write a spec and run:

```bash
node scripts/new-deck.js examples/morning-briefing.js   # briefing only
node scripts/new-deck.js examples/feature-roadmap-road.js  # single-path feature roadmap
node scripts/new-deck.js examples/onboarding-waves.js   # agent-designed layout
node scripts/new-deck.js examples/programme-readout.js  # Unite / named-work board
node scripts/new-deck.js examples/skill-deck.json       # recipe-driven (qaAllowLabelChips)
```

Pick the starter with [examples/WHEN-TO-COPY.md](examples/WHEN-TO-COPY.md).

## What’s in the skill

| File | Role |
|------|------|
| `SKILL.md` | When to use the skill, hard rules, build workflow |
| `preferences.md` | Nick taste: audiences, density, phrasing (not tokens) |
| `fail-log.md` | Critique log + already-encoded failures |
| `template.md` | Brand template deck, empty layouts, deck builder + background pipeline |
| `tokens.md` | Canvas, palette, type, footer, motifs |
| `layouts.md` | How to design a layout for the story + recipes, diagrams, icons |
| `functional-areas.md` | Mandatory org-area colours |
| `assets.md` | Drive libraries + icon selection playbook |
| `qa.md` | Automated + visual pass/fail gate (+ encoded fail notes) |
| `scripts/` | `deck.js` engine + `new-deck.js` runner + `test-story-shapes.js` |
| `examples/` | Worked specs + when-to-copy index + [reference-decks.md](examples/reference-decks.md) live style references |

## Skill improvement (critique → encode)

Skills are not model fine-tunes. The agent gets better at *your* style when you feed judgment back into these files after real decks.

```text
outline → new-deck.js → automated QA → read thumbnails (V1–V9)
       → your critique → encode into skill files → next similar deck
```

### After every deck

1. Complete QA ([qa.md](qa.md)). On any visual miss, append a row to [fail-log.md](fail-log.md).
2. Classify the miss (token / story-format / hierarchy / icon / recipe-menu / audience).
3. Encode **durable** corrections only (seen twice, or once if severe):

| Miss type | Encode into |
|-----------|-------------|
| Brand / type / corners | `tokens.md` or SKILL hard rule / Do not |
| Wrong figure for the sentence | Story first / hard rule 14; Do not anti-pattern |
| Hierarchy / whitespace / icons | Concrete V-note in `qa.md` |
| Recurring composition that worked | Keep in deck `draw()`; promote on **third** use |
| New use case | New `examples/` file + WHEN-TO-COPY row |
| Taste (density, phrasing, audience) | `preferences.md` |

4. Write **commands**, not vibes (“Do not put Asks on a separate `twoCol`”).
5. Regression-check by rebuilding a known good type (e.g. morning briefing).

### Cadence

- After the next 2–3 decks: keep the fail log hot.
- Encode repeats once into preferences + Do not + QA notes.
- Monthly: cull contradictory guidance; fewer sharper rules beat a long essay.
- Do not expand `SKILL.md` past ~500 lines — push detail into companions.

### Personalize without breaking brand

Keep CTCT-2024 tokens and Empty Slide non-negotiable. Personalize judgment in `preferences.md` and examples only. Optional Cursor user rule for routing:

> For CTCT/Unite Google Slides, always use the google-slides-style-guide skill and preferences.md.

## Limits

- Style skill ≠ Aha / Jira / Confluence connectors (those are separate)
- Do **not** edit Empty Slide, the 52-slide CTCT Slide Template master, or example decks in place — the builder copies Empty Slide
- Do **not** add a second skill folder or a Python/PPTX builder — keep `scripts/new-deck.js`
- Needs working `gws` auth, Drive permissions, and `scripts/` to build real slides
- A non-CTCT personal presentation voice should be a **separate** skill folder, not overlays on tokens here
