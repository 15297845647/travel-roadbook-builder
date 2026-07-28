# Deliverable specification

## Master route table

Place one compact source-of-truth table near the top:

| Day/date | Sleep | Transport | Route | Distance/time | Core visit | Booking |
|---|---|---|---|---|---|---|

Use realistic elapsed time. Mark long or weather-sensitive days. Keep the same values in route cards, detailed days, budget, and PDF.

## Day-card content

Each day card must contain:

1. date, weekday, route, distance, drive or transfer time;
2. a chronological timeline;
3. exactly how to visit each place;
4. entrances, parking, shuttles, walks, and exit strategy;
5. meal area and named restaurant candidates;
6. hotel zone and property candidates;
7. tickets and action deadlines;
8. weather, altitude, road, and fatigue warnings;
9. latest safe departure or cut-off;
10. first item to skip and Plan B.

Explain “what to play” at each attraction. Examples: viewing platform order, lakeside segment, village loop, museum floor sequence, cable-car combination, sunrise position, or old-town walking direction.

## Booking table

Use:

| Visit date | Product | Action date | Channel | Required data | Refund/change | Plan B | Status |
|---|---|---|---|---|---|---|---|

Status values: confirmed, sales not open, monitor, optional, or pending verification.

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
- two or three named current shops;
- correct branch and map search term;
- signature order for party size;
- meal-period opening status;
- queue/reservation pattern;
- parking or walking access;
- price band and dietary warnings;
- backup nearby.

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

Provide descriptive alt text, caption, creator/source, and license link when required. Do not hotlink brittle image URLs in a shareable artifact. Download permitted images locally, then embed them in the single-file edition.

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
