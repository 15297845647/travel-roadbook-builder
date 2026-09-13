# Deliverable specification

## Delivery states

Use the planning response to settle the itinerary. When all material choices are accepted, move to Ready and offer the final artifact choices defined in `SKILL.md`. Do not generate files merely because the plan is complete, and do not close the conversation without the offer.

When the Ready-state user selects an artifact set, generate it in the same turn when tools and runtime allow. A request that already names the desired artifacts counts as that selection and must not trigger a redundant artifact-choice question; it does not bypass material-fact resolution or itinerary acceptance.

## Quick mode

Return, in this order:

1. a one-glance trip contract and any assumptions;
2. the ordered route, with draft map links only when they help the current decision;
3. a chronological table with an explicit travel block between locations;
4. opening, reservation, and last-entry constraints;
5. the cut-off, first optional item to remove, and one fallback;
6. source links and the check date for volatile facts.

Do not include the lodging, packing, budget, HTML, or PDF modules unless they matter to the request.

After the user accepts the Quick plan, offer the same final artifact choices as Roadbook mode. Generate and validate the complete navigation-link set only after the plan is Ready. If the user requests links during Planning, provide only clearly labeled draft links for sufficiently defined legs; this does not create a final artifact or bypass the Ready gate.

## Final artifact choices

Offer these choices when the plan becomes Ready and the user has not already chosen:

| Choice | Final output |
|---|---|
| Shareable roadbook (recommended) | Structured plan data, shareable single-file HTML, and complete navigation links inside the roadbook |
| Roadbook plus PDF | The shareable roadbook package plus a print-ready PDF |
| Navigation links only | One ordered link per route leg, with mode and endpoint labels |
| Continue revising | No final artifact yet; return to Planning |

Name the files that were created and provide clickable links at handoff. If a selected artifact cannot be created, say which artifact failed and why; do not replace it silently with prose.

## Master route table

Place one compact source-of-truth table near the top:

| Day/date | Sleep | Transport/segment role | Route | Distance/wheel/elapsed | Core visit | Booking |
|---|---|---|---|---|---|---|

Use realistic elapsed time. Mark long or weather-sensitive days. Keep the same values in route cards, detailed days, budget, and PDF.

Give scenic-drive attractions their own core-visit label rather than hiding them inside “transport.”

When navigation links are selected, make one link for every consecutive accepted travel leg. Its origin, destination, mode, and label must agree with the final master table. A link is a navigation handoff, not proof of traffic, distance, or duration.

## Map and navigation

Include a map/navigation section after the route overview:

- identify whether each duration came from a live query, a verified source, or an estimate;
- provide one ordered route or a numbered link per leg;
- place each link beside its matching travel block and keep its exact origin, destination, and mode in sync;
- keep every stop visible when a provider cannot encode multi-stop routes;
- disambiguate branches and similarly named places;
- warn before exposing private anchors in shareable links.

Do not label a URL formatter as route optimization or live navigation.

## Day-card content

Each day card must contain:

1. date, weekday, route, distance, drive or transfer time;
2. a chronological timeline;
3. exactly how to visit each place;
4. entrances, parking, shuttles, walks, and exit strategy;
5. each restaurant meal’s named primary choice plus 1–2 alternatives, dishes, reasons, route fit, and relevant parking/queue/reservation notes (or explicit evidence/access gaps);
6. hotel zone and property candidates;
7. tickets and action deadlines;
8. weather, altitude, road, and fatigue warnings;
9. latest safe departure or cut-off;
10. first item to skip and Plan B.

Explain “what to play” at each attraction. Examples: viewing platform order, lakeside segment, village loop, museum floor sequence, cable-car combination, sunrise position, or old-town walking direction.

For a scenic road, include navigation waypoints, safe stopping rules, photo-stop versus full-visit durations, expressway fallback, and the cutoff that activates it.

## Booking table

Use:

| Visit date | Product | Action date | Channel | Required data | Refund/change | Plan B | Status |
|---|---|---|---|---|---|---|---|

Status values: confirmed, sales not open, monitor, optional, or pending verification.

Include one row for every planned attraction or scenic-road stop. For a free/open viewpoint, use `optional/no ticket` only when supported; otherwise use `pending verification`. Never let an omitted row imply that no action is required.

## Hotel recommendations

Recommend the correct area before specific hotels. For each candidate include:

- convenient for which day;
- driving/parking or station access;
- realistic view conditions;
- breakfast and early checkout;
- heating/air-conditioning and hot-water reliability where relevant;
- oxygen or humidifier availability where relevant;
- approximate price band with date checked;
- free cancellation deadline;
- one tradeoff.

Avoid claiming a room guarantees sunrise, mountain, or lake views unless the exact room type and orientation are verified.

## Food recommendations

Organize by city and meal:

- local dishes to try;
- one named primary shop plus 1–2 alternatives per restaurant meal, chosen using `xiaohongshu-travel-and-food.md`;
- correct branch and map search term;
- signature order for party size;
- meal-period opening status;
- queue/reservation pattern;
- parking or walking access;
- price band and dietary warnings;
- backup nearby;
- why this shop: recent independent experience, substantive comments, marketing caveats, and evidence confidence;
- relation to the preceding/following stop, walking or detour time with its basis, and a queue cut-off that protects the day;
- source links and check date, with unavailable Xiaohongshu details disclosed.

Clearly distinguish a researched candidate from a booked or guaranteed venue.

## Packing and safety

Tailor the list:

- identity, license, payment, reservation screenshots, offline maps;
- layered clothing, waterproof shell, sun protection, footwear;
- chargers, car adapter, power bank, camera storage;
- medications, motion-sickness support, high-altitude precautions;
- snacks, water, tissue, trash bags;
- child/older-adult equipment;
- vehicle inspection, tire pressure, chains, fuel/charge planning.

Do not present medication as personalized medical advice. Encourage professional advice for high-risk travelers.

## Budget

Show transparent assumptions and ranges for:

- intercity tickets;
- rental, one-way fee, insurance, fuel/charging, tolls, parking;
- hotels by night;
- attraction and internal transport tickets;
- meals;
- contingency.

Separate confirmed prices from estimates and volatile holiday pricing.

## HTML experience

Required sections:

- hero;
- route overview;
- transport decision;
- day-by-day schedule;
- reservations;
- lodging;
- food;
- packing;
- safety and fallback;
- budget;
- sources and check date.

Add `data-roadbook-revision` to the document and `data-day` plus `data-sleep` to each dated day card. Keep the revision value identical in source and bundled HTML.

Recommended interaction:

- sticky navigation;
- reading progress;
- countdown based on local trip date;
- expandable day cards;
- subtle reveal motion;
- “expand all” and “collapse all” controls;
- print button;
- reduced-motion support.

Keep content available when JavaScript is disabled. Avoid horizontal overflow on phones.

## Image policy

Use:

- user-provided images with permission;
- official destination press images where reuse is permitted;
- openly licensed or public-domain images;
- generated decorative visuals when clearly appropriate.

Provide descriptive alt text, caption, creator/source, and license link when required. Do not hotlink brittle image URLs in a shareable artifact. Download permitted images locally, then embed them in the single-file edition. Embed hero and CSS background images too, not only ordinary `<img>` tags. After a route revision, verify that each image still depicts the correct place or is clearly labeled as representative.

## Print and PDF contract

The PDF must preserve the whole guide:

- full background colors and images;
- all day details expanded;
- readable tables;
- no sticky controls or animations;
- page-break protection for cards and headings;
- URLs printed or clickable;
- CJK-capable fonts;
- reasonable margins and page numbers.

Use CSS similar to:

```css
@media print {
  * { -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
  nav, .screen-only { display: none !important; }
  details > * { display: block !important; }
  .card, table, figure { break-inside: avoid; }
  a { color: inherit; text-decoration: none; }
}
```

Do not trust the first export. Render and inspect every page.

Derive PDF facts from the same master model or HTML. If a generator contains manually written cover metrics, footer summaries, or day-image mappings, include them in the revision audit and stale-token search.
