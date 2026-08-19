# Builder scripts

This skill expects:

| File | Role |
|------|------|
| `deck.js` | Kit + recipes + draw helpers |
| `new-deck.js` | Spec runner + automated QA |
| `test-story-shapes.js` | Story-shape checks before draw |
| `isometrics.json` | Product isometric index (if used by kit) |

If these files are missing, copy them from your existing personal install at
`~/.cursor/skills/google-slides-style-guide/scripts/` (Windows:
`%USERPROFILE%\.cursor\skills\google-slides-style-guide\scripts\`) into this
folder before running builds. Do not invent a second builder.
