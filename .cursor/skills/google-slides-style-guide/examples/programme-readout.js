/**
 * Programme / Unite readout — third worked pattern (named work + decision).
 *
 * Copy ONLY for Unite / programme-board / named-work readouts.
 * Do NOT use for weekday delivery briefings → see morning-briefing.js
 * Do NOT invent status-well triplets when the outline lists programmes by name.
 *
 * Story outline this spec encodes:
 *   1. Title (template) — programme board for the period
 *   2. Named programmes and how far each got → comparison panels (names, not wells)
 *   3. The one decision we need from this room → single accent panel
 *
 * If `panels` fights the sentence (e.g. lanes/timeline), switch those slides to
 * draw() and copy kit usage from onboarding-waves.js.
 *
 * Run: node scripts/new-deck.js examples/programme-readout.js
 * See WHEN-TO-COPY.md.
 */

module.exports = {
  title: 'Programme readout — TEMPLATE',
  deckTitle: 'Programme readout',
  meta: 'Unite  |  D Month YYYY',
  // folderId: 'target-Drive-folder-id',
  // presentationId: 'existing-file-id',
  background: 'generated-title-photo.png',
  slides: [
    {
      kind: 'panels',
      title: 'Named programmes this period',
      summary: 'Register of named work — not a status-well substitute.',
      // Replace headers/body with the real outline. Accent the programme that matters.
      panels: [
        {
          header: 'Programme A',
          body: 'On track — outcome one-liner',
          pill: 'On track',
        },
        {
          header: 'Programme B',
          body: 'Watch — outcome one-liner',
          pill: 'Watch',
        },
        {
          header: 'Programme C',
          body: 'Blocked — outcome one-liner',
          pill: 'Blocked',
          accent: true,
        },
      ],
    },
    {
      kind: 'panels',
      title: 'Decision needed',
      summary: 'One ask. One accent. Everything else is context.',
      panels: [
        {
          header: 'Ask',
          body:
            'Replace with the single decision sentence from the outline. Keep supporting context short — split slides rather than cram.',
          pill: 'Decide',
          accent: true,
        },
      ],
    },
  ],
};
