# Section guide

Read only the section that is open. Ask a few questions at a time. The done bar applies when the user wants that section confirmed. Skipping a section skips its bar.

A missing upstream section is named once, then the link stays blank or holds a working assumption the user stated. Do not send the user back up the cascade.

Metric menus are closed. A metric from outside the menu keeps the pillars section in `draft`.

## Frame

**Purpose.** Name the product, the horizon, who the readout is for, and the decision this strategy must unlock.

**Questions.**

- What product or portfolio is this for?
- What time horizon does it cover?
- Who will read the report-out?
- What decision must this strategy unlock?

**Done when.** All four answers are specific. The decision is something a room can accept or reject (fund a bet, adopt a focus, stop a line of work).

**Failure modes.**

- The decision is "align the team" or "share an update", with nothing to decide.
- The horizon is missing, so later targets have nothing to land in.

**Write.** `sections.frame`: `product`, `horizon`, `audience`, `decision`.

## Vision, mission, direction

**Purpose.** Separate the future state, the ongoing job, and this horizon's bet.

**Questions.**

- If this works, what is true for customers that is not true now? Keep features out of the sentence.
- Who do we exist to serve, and what do we exist to do on an ongoing basis?
- What is the shift this horizon, stated as from X to Y?
- Could a reasonable team choose a different direction and still fit that sentence?

**Done when.** The three sentences do different jobs. Vision has no product features. Direction is choosable: a team could pursue a different bet. If two reasonable strategies both fit the direction, it is not done.

**Failure modes.**

- Vision, mission, and direction are the same sentence rewritten.
- Direction lists a bundle of initiatives.
- Vision names a feature, a release, or a metric target.

**Write.** `sections.vision`: `vision`, `mission`, `direction`.

## Where we play

**Purpose.** Choose the regions, markets, and customer cohorts that are in, and name who is out.

**Questions.**

- Which regions and markets are in for this horizon?
- Which customer segments and cohorts are in? Name the buyer and the user when they differ.
- Who is explicitly out?
- For each included market, why does the direction require it? Ask this only when a direction exists. Otherwise leave the reason blank.

**Done when.** At least one market and one segment are in, and at least one exclusion is named. Every included market has a reason tied to the direction when a direction exists.

**Failure modes.**

- The market is "everyone" or an industry with no boundary.
- Segments are company names only, with no cohort.
- "Who is out" is empty, so the choice is not a choice.

**Write.** `sections.where_we_play`: `regions_and_markets`, `segments_and_cohorts`, `who_is_out`. Each entry is `{ name, why }`. `why` may be empty when direction is not available.

## Customer needs and problems

**Purpose.** State the problems we will own, in the customer's situation, before any solution.

**Questions.**

- What is the problem, in the customer's words?
- Who feels it, and how often?
- What does the status quo cost them?
- What evidence do we actually have (a quote, a count, a win, a loss)?
- Will we own this need, or only acknowledge it?

**Done when.** Each need has who, frequency, cost, and evidence the user actually has. Each need is `own` or `acknowledge`. At least one need is `own`. A need that sits outside a chosen segment is dropped or moved to acknowledge when segments exist. No solutions in this section.

**Failure modes.**

- The "need" is a feature request ("they need our API").
- Evidence is a hunch written as a fact.
- Every need is owned, including ones with no evidence.

**Write.** `sections.needs.items[]`: `name`, `who`, `frequency`, `cost_of_status_quo`, `evidence`, `stance` (`own` or `acknowledge`).

## How we win

**Purpose.** Map what we offer to owned needs, and say why a chosen customer picks us over the alternative they use today.

**Questions.**

- Which products or solutions are in play this horizon, existing and planned?
- Which owned need does each one serve? Leave `need` blank when needs are not decided, or when the user has not named the link.
- For each primary segment, why do they pick us, and what do they use today instead?

**Done when.** Each product has a name. Each product's `need` is either an owned need or blank. There is one value proposition per primary segment that exists in Where we play (or one, if segments are not decided). Each value proposition names the alternative.

**Failure modes.**

- The value proposition could be claimed by the alternative without changing a word.
- A product is listed with no customer job, and the user treats the blank link as if it were filled.
- Solutions appear that the user never named.

**Write.** `sections.how_we_win.products[]`: `name`, `need`, optional `assumption`. `value_propositions[]`: `segment`, `statement`, `alternative`.

## Outcome pillars

**Purpose.** Set the scoreboard for the horizon. Pillars are not a project list.

Pick one or two metrics per pillar, from that pillar's menu only.

- **Grow the business:** market share, product adoption, revenue, profitability / product ROI.
- **Establish interoperability:** API usage, integration success, retention, support and quality.
- **Lead industry innovation:** unique new features, patents / trade secret applications, attributable revenue, time to market, employee innovation hours.

**Questions.** Ask one pillar at a time.

- Which one or two menu metrics define this pillar for the horizon?
- What is the baseline, the target, and the owner?

**Done when.** Each pillar that the user wants on the slide has one or two menu metrics. Each metric has baseline, target, and owner. A pillar the user leaves unset stays an empty list, and the section can still be confirmed if every metric that is present is complete. At least one metric exists somewhere in the section.

**Failure modes.**

- The metric is a slogan ("be the leader") with no baseline.
- A project name is recorded as a metric.
- A metric from outside the menu is marked confirmed.

**Write.** `sections.pillars.grow`, `.interoperability`, `.innovation`. Each item: `metric`, `baseline`, `target`, `owner`.

## SWOT

**Purpose.** Name the few strengths, weaknesses, opportunities, and threats that bear on this strategy. Cap each quadrant at about three.

**Questions.** Ask one quadrant at a time.

- What strength helps us win an owned need? Which need?
- What weakness threatens a pillar or the value proposition? Which one?
- What external opportunity advances a pillar? Which pillar?
- What external threat breaks a market choice or the value proposition? Which one?

When the upstream section does not exist, store the item and leave `affects` blank.

**Done when.** Each quadrant has at least one item and no more than about three. Each item names what it affects when that upstream section exists.

**Failure modes.**

- A generic company SWOT with no link to a need, pillar, or market choice, even though those sections exist.
- More than a handful of items, so the quadrant is a brainstorm rather than a decision.

**Write.** `sections.swot.strengths`, `.weaknesses`, `.opportunities`, `.threats`. Each item: `item`, `affects`.

## Decision filters

**Purpose.** Fix the rules for what gets funded, what stops, and how capacity splits.

**Questions.**

- What conditions must an initiative meet before it can be funded?
- What markets, customers, features, or work will we refuse or end, and what does each stop protect?
- How does capacity split across grow, interoperability, and innovation? What gets less?

**Done when.** There is at least one must-have and one stop. Each stop names what it protects. The three resource percentages are present and sum to 100.

**Failure modes.**

- The stop list is a list of complaints with nothing protected.
- The split leaves a pillar out, or the percentages do not sum to 100.
- Must-haves are restated initiatives.

**Write.** `sections.filters.must_haves[]` as strings. `stop_list[]`: `item`, `protects`. `resources[]`: `pillar` (`grow`, `interoperability`, or `innovation`), `percent`.

## Initiatives and operational work

**Purpose.** Name the customer-facing bets and the internal work those bets need.

**Questions.**

- What is the product initiative, which owned need does it serve, which pillar metric does it move, and which must-have does it satisfy?
- What will be true if it lands this horizon?
- What operational action does that bet need, and which initiative or weakness does it support?

Leave `need`, `pillar_metric`, or `must_have` blank when that upstream section is empty or skipped, unless the user states a working assumption. An item that the user says fails a must-have or hits the stop list is left out of the file.

**Done when.** Each product initiative has a name and an outcome. Links that can be made are made. Links that cannot be made are blank. Each operational action names the initiative or other work it supports, or the link is blank on purpose.

**Failure modes.**

- An initiative is a task list ("hold a workshop") with no customer outcome.
- A link field is filled with a guess the user did not state.
- Operational work is mixed into the product list with no customer-facing bet.

**Write.** `sections.initiatives.product[]`: `name`, `need`, `pillar_metric`, `must_have`, `outcome`, optional `assumption`. `operational[]`: `name`, `supports`, optional `assumption`.

## Roadmap

**Purpose.** Sequence delivery inside the horizon. Now / next / later, not a backlog.

**Questions.**

- What is in now, next, and later?
- Which initiative or operational action does each item deliver?
- What does this sequence depend on?
- What single assumption, if wrong, would reorder the roadmap?
- What does "delivered" mean at the end of the horizon?

**Done when.** Each column that the user uses has named items. Each item's `traces_to` is an initiative or operational action when those exist, otherwise blank. Dependencies, the reorder assumption, and what delivered means are filled when the user knows them. They may be left empty without blocking, and the section stays `draft` until the three sequence columns the user cares about are filled and each known trace is either linked or deliberately blank.

**Failure modes.**

- The roadmap is a flat backlog with no sequence.
- Items appear that do not trace to any initiative or operational action, and the user treats the blank as a link.
- "Delivered" is a restatement of the vision with no horizon outcome.

**Write.** `sections.roadmap.now`, `.next`, `.later`. Each item: `name`, `traces_to`, optional `assumption`. Also `dependencies`, `reorder_assumption`, `delivered_means`.
