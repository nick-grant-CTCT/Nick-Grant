/**
 * Single-path feature / product roadmap — winding road + delivery pins.
 *
 * Copy ONLY when the outline is features we ship along one path.
 * Do NOT use for GEM parallel workstreams → swimlanes in reference-decks.md
 * Do NOT use chevrons, pastel stock palettes, or ROUND_RECTANGLE cards.
 *
 * Story outline this spec encodes:
 *   1. Title (template) — photorealistic CTCT jobsite photo, not an orange intro filter
 *   2. Named features on one delivery road → winding-road draw()
 *
 * Kit: ctx.kit from scripts/deck.js. Helpers used below: shape/rect/ellipse/text.
 * If names differ in your install, map to the same inches. Content band y 2.0–5.05.
 *
 * Run: node scripts/new-deck.js examples/feature-roadmap-road.js
 * See WHEN-TO-COPY.md and layouts.md (Winding-road feature roadmap).
 */

const T = {
  orange: '#FF8B00',
  orangeDeep: '#DE6120',
  ink: '#595959',
  card: '#F2F2F2',
  road: '#555555',
  white: '#FFFFFF',
  blue: '#00A3D6',
  green: '#6AA84F',
  purple: '#A64D79',
};

const PIN_CYCLE = [T.blue, T.orange, T.green, T.purple, T.road];

/** Replace these with the live outline. 4–6 milestones. ≤3 bullets each. */
const MILESTONES = [
  {
    title: 'Shareable designs',
    bullets: ['MMP0 infield share', 'Site file handoff', 'Dealer-ready package'],
  },
  {
    title: 'Image overlay',
    bullets: ['MMP1 geolocated image', 'Reference on machine', 'Unconnected fallback'],
  },
  {
    title: 'App-based design',
    bullets: ['MMP2 create/edit', 'On and off machine', 'Guided workflow'],
  },
  {
    title: 'Mesh surfaces',
    bullets: ['MMP3 infield mesh', 'Site-relative model', 'QA against design'],
  },
  {
    title: 'Site-relative RTK',
    bullets: ['This-site accuracy', 'SC job conditions', 'Low dealer reliance'],
  },
];

function kitShape(r, page, ctx, opts) {
  const k = ctx.kit;
  if (!k) {
    throw new Error('ctx.kit missing — copy scripts/deck.js from the skill install; do not add a second builder');
  }
  if (typeof k.shape === 'function') return k.shape(r, page, opts);
  if (opts.type === 'ELLIPSE' && typeof k.ellipse === 'function') {
    return k.ellipse(r, page, opts);
  }
  if (opts.type === 'TRIANGLE' && typeof k.triangle === 'function') {
    return k.triangle(r, page, opts);
  }
  if (typeof k.rect === 'function' && (opts.type === 'RECTANGLE' || !opts.type)) {
    return k.rect(r, page, opts);
  }
  if (typeof k.addShape === 'function') return k.addShape(r, page, opts);
  throw new Error('ctx.kit has no shape helper — use the existing new-deck.js kit');
}

function kitText(r, page, ctx, opts) {
  const k = ctx.kit;
  if (typeof k.text === 'function') return k.text(r, page, opts);
  if (typeof k.addText === 'function') return k.addText(r, page, opts);
  throw new Error('ctx.kit has no text helper — use the existing new-deck.js kit');
}

function roadPoint(t, x0, x1, yMid, amp) {
  const x = x0 + t * (x1 - x0);
  const y = yMid - Math.cos(t * 4 * Math.PI) * amp;
  return { x, y, t };
}

function drawWindingRoad(r, page, ctx) {
  const n = MILESTONES.length;
  const x0 = 0.42;
  const x1 = 9.58;
  const yMid = 3.72;
  const amp = 0.38;
  const segments = 36;

  for (let i = 0; i < segments; i++) {
    const t = i / (segments - 1);
    const p = roadPoint(t, x0, x1, yMid, amp);
    kitShape(r, page, ctx, {
      type: 'ELLIPSE',
      x: p.x - 0.28,
      y: p.y - 0.16,
      w: 0.56,
      h: 0.32,
      fill: T.orange,
    });
  }
  for (let i = 0; i < segments; i++) {
    const t = i / (segments - 1);
    const p = roadPoint(t, x0, x1, yMid, amp);
    kitShape(r, page, ctx, {
      type: 'ELLIPSE',
      x: p.x - 0.24,
      y: p.y - 0.12,
      w: 0.48,
      h: 0.24,
      fill: T.road,
    });
  }
  for (let i = 0; i < segments; i += 2) {
    const t = i / (segments - 1);
    const p = roadPoint(t, x0, x1, yMid, amp);
    kitShape(r, page, ctx, {
      type: 'RECTANGLE',
      x: p.x - 0.07,
      y: p.y - 0.015,
      w: 0.14,
      h: 0.03,
      fill: T.white,
    });
  }

  MILESTONES.forEach((m, i) => {
    const t = n === 1 ? 0.5 : i / (n - 1);
    const p = roadPoint(t, x0, x1, yMid, amp);
    const accent = PIN_CYCLE[i % PIN_CYCLE.length];
    const cardW = 1.72;
    const cardH = 1.05;
    const cardX = Math.min(Math.max(p.x - cardW / 2, 0.35), 10 - cardW - 0.35);
    const peak = Math.cos(t * 4 * Math.PI) > 0;
    const cardY = peak ? 2.05 : 2.12;

    kitShape(r, page, ctx, {
      type: 'RECTANGLE',
      x: cardX,
      y: cardY,
      w: cardW,
      h: cardH,
      fill: T.card,
    });
    kitShape(r, page, ctx, {
      type: 'RECTANGLE',
      x: cardX,
      y: cardY,
      w: 0.08,
      h: cardH,
      fill: accent,
    });
    kitText(r, page, ctx, {
      x: cardX + 0.14,
      y: cardY + 0.06,
      w: cardW - 0.2,
      h: 0.28,
      text: m.title,
      fontFamily: 'Proxima Nova',
      fontSize: 11,
      bold: true,
      color: accent === T.road ? T.ink : accent,
    });
    kitText(r, page, ctx, {
      x: cardX + 0.14,
      y: cardY + 0.34,
      w: cardW - 0.2,
      h: 0.66,
      text: m.bullets.map((b) => `• ${b}`).join('\n'),
      fontFamily: 'Inter',
      fontSize: 8,
      color: T.ink,
    });

    const stemH = Math.max(p.y - (cardY + cardH) - 0.12, 0.08);
    kitShape(r, page, ctx, {
      type: 'RECTANGLE',
      x: p.x - 0.025,
      y: cardY + cardH,
      w: 0.05,
      h: stemH,
      fill: accent,
    });
    kitShape(r, page, ctx, {
      type: 'ELLIPSE',
      x: p.x - 0.11,
      y: p.y - 0.22,
      w: 0.22,
      h: 0.22,
      fill: accent,
    });
    kitShape(r, page, ctx, {
      type: 'TRIANGLE',
      x: p.x - 0.07,
      y: p.y - 0.04,
      w: 0.14,
      h: 0.14,
      fill: accent,
    });
  });
}

module.exports = {
  title: 'Feature roadmap — TEMPLATE',
  deckTitle: 'Feature delivery roadmap',
  meta: 'Programme  |  D Month YYYY',
  // folderId: 'target-Drive-folder-id',
  // presentationId: 'existing-file-id',
  background: 'generated-title-photo.png',
  slides: [
    {
      kind: 'draw',
      title: 'Features we deliver on this path',
      summary: 'One road. Named pins. Left to right is delivery order.',
      notes:
        'Talk track: walk the pins in order. Do not add a second text recipe beside this figure.',
      draw(r, page, ctx) {
        drawWindingRoad(r, page, ctx);
      },
    },
  ],
};
