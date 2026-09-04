/**
 * Site Contractor — Refreshed Roadmap
 *
 * Story outline (written before picking a recipe):
 *   1. Title — Site Contractor refreshed feature path
 *   2. Features we deliver on the Site Contractor path, 2025–2028
 *      → winding-road draw() (single delivery path, not GEM swimlanes)
 *
 * Delivery order follows the source slide (MMP3 before MMP2).
 * MMP1 is the accent (next / in-flight). Dates past MMP1 are indicative.
 *
 * Copy of Empty Slide this spec targets (chrome; run new-deck.js locally):
 *   https://docs.google.com/presentation/d/1U1_2Xo_ScxdLMtuOKfHXt7occPvMkE5enK_aeJVpLCM/edit
 *   presentationId 1U1_2Xo_ScxdLMtuOKfHXt7occPvMkE5enK_aeJVpLCM
 *
 * Visual Google Slides (16:9 winding-road figure, converted from the spec render):
 *   https://docs.google.com/presentation/d/1SZrbE-tU36qSXoPXlBjZDuOQTD4gG1rFhoORFlG9OYo/edit
 *
 * Run: node scripts/new-deck.js examples/site-contractor-roadmap.js
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

/** Source order. Titles from Nick’s slide; bullets are short talk-track glosses. */
const MILESTONES = [
  {
    year: '2025',
    code: 'MMP0',
    title: 'Shareable Infield Designs',
    bullets: ['Share designs on site', 'Handoff without back-office'],
  },
  {
    year: '2026',
    code: 'MMP1',
    title: 'Geolocated Digital Image Overlay for Reference',
    bullets: ['Reference overlay on machine', 'Site-relative context'],
  },
  {
    year: '2027',
    code: 'MMP3',
    title: 'On/Off Machine Infield Mesh Surface Design Creation',
    bullets: ['On/off machine creation', 'Mesh surfaces on site'],
  },
  {
    year: '2028',
    code: 'MMP2',
    title: 'On/Off Machine Application-based Design Creation',
    bullets: ['On/off machine apps', 'Guided design workflows'],
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
  // 4 pins: 1.5 periods → peak / valley / peak / valley (layouts.md 4π is the 5-pin default).
  const y = yMid - Math.cos(t * 3 * Math.PI) * amp;
  return { x, y, t };
}

function drawWindingRoad(r, page, ctx) {
  const n = MILESTONES.length;
  const x0 = 0.42;
  const x1 = 9.58;
  const yMid = 3.82;
  const amp = 0.34;
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
    const cardW = 2.12;
    const cardH = 1.32;
    const cardX = Math.min(Math.max(p.x - cardW / 2, 0.32), 10 - cardW - 0.32);
    const peak = Math.cos(t * 3 * Math.PI) > 0;
    const cardY = peak ? 2.00 : 2.06;

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
      x: cardX + 0.16,
      y: cardY + 0.06,
      w: cardW - 0.24,
      h: 0.2,
      text: m.year,
      fontFamily: 'Inter',
      fontSize: 9,
      color: T.ink,
    });
    kitText(r, page, ctx, {
      x: cardX + 0.16,
      y: cardY + 0.24,
      w: cardW - 0.24,
      h: 0.28,
      text: m.code,
      fontFamily: 'Proxima Nova',
      fontSize: 14,
      bold: true,
      color: accent === T.road ? T.ink : accent,
    });
    kitText(r, page, ctx, {
      x: cardX + 0.16,
      y: cardY + 0.52,
      w: cardW - 0.24,
      h: 0.36,
      text: m.title,
      fontFamily: 'Inter',
      fontSize: 9,
      color: T.ink,
    });
    kitText(r, page, ctx, {
      x: cardX + 0.16,
      y: cardY + 0.88,
      w: cardW - 0.24,
      h: 0.4,
      text: (m.bullets || []).map((b) => `• ${b}`).join('\n'),
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
  title: 'Site Contractor — Refreshed Roadmap',
  deckTitle: 'Site Contractor',
  meta: 'Site Contractor  |  3 September 2026',
  presentationId: '1U1_2Xo_ScxdLMtuOKfHXt7occPvMkE5enK_aeJVpLCM',
  background: 'site-contractor-title-photo.png',
  slides: [
    {
      kind: 'draw',
      title: 'Features we deliver on the Site Contractor path',
      summary: '2025–2028. Fidelity of dates and requirements degrades beyond MMP1.',
      notes:
        'Walk MMP0 → MMP1 → MMP3 → MMP2. MMP numbering is not chronological; delivery order is. DISCLAIMER: Fidelity of dates and requirements degrades beyond MMP1.',
      milestones: MILESTONES,
      draw(r, page, ctx) {
        drawWindingRoad(r, page, ctx);
      },
    },
  ],
};
