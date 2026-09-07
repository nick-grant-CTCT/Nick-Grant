# Template and builder

## Empty Slide (builder source)

Every new deck is a Drive **copy** of Empty Slide:

`1Bl1tpH-fqY_vUW8_B2vBcAPkJbVOsMMUlIB5l7u-QYs`

- Update slide 1 (title) and slide 2 (first content); duplicate slide 2 for more pages.
- Never delete the two starter slides.
- Never edit Empty Slide itself.

## CTCT Slide Template (52-slide master — read only)

Brand / Image Assets / Icon Library gallery:

`1KXJnuCfkHnIekoKv_mU5F87n-eTOJvjWQ2rPH3qVfoM`

Never edit this master. Copy Empty Slide to build; open the gallery only to match Image Assets, icons, and type.

## Chrome (do not redraw)

Slide numbers, CONFIDENTIAL badge, cube logo, honeycomb, title scrim, and orange rule come from the layout.

## Title photo

1. Generate a photorealistic CTCT-domain image (≥800×450), no baked-in text, calm left side.
2. Replace the **layout** photo with `replaceImage` + `CENTER_CROP`.
3. Follow [preferences.md](preferences.md) title-photo direction.

## Builder

```bash
node scripts/new-deck.js spec.js
node scripts/new-deck.js spec.json
```

Prefer `.js` when any slide needs `draw(r, page, ctx)` and `ctx.kit`.
Set `presentationId` on the spec to rebuild an existing URL in place.

If `scripts/deck.js` / `new-deck.js` are missing from this install, copy them from the full skill package before building — documentation alone cannot create slides.

## Kit

`draw()` compositions use `ctx.kit` helpers from `scripts/deck.js`. Copy primitives from [examples/feature-roadmap-road.js](examples/feature-roadmap-road.js) (winding-road roadmap) or [examples/onboarding-waves.js](examples/onboarding-waves.js) (other invented figures). Content band ≈ `y` 2.0–5.05 in.
