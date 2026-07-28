---
name: travel-roadbook-builder
description: Create research-backed, executable travel roadbooks with route and transport optimization, exact rental pickup and return planning, day-by-day itineraries, booking calendars, hotels, restaurants, safety notes, sources, a shareable single-file HTML, and a rendered and verified color PDF. Use when Codex is asked to plan or revise a multi-day trip, self-drive/high-speed-rail/flight itinerary, detailed travel guide, animated travel webpage, printable PDF roadbook, attraction reservation guide, or destination route comparison.
---

# Travel Roadbook Builder

Create a trip that can actually be booked and followed. Optimize the route before decorating it, verify unstable facts, then deliver both a rich shareable webpage and a print-ready full-color PDF when requested.

## Required workflow

### 1. Establish the trip contract

Read `references/intake-and-research.md`.

Extract or ask only for decisions that materially change the route:

- exact arrival and departure date, time, airport, railway station, or city;
- total calendar days and hotel nights;
- must-see places and explicitly droppable places;
- travelers, ages, health limits, number of drivers, and luggage;
- maximum comfortable driving time and tolerance for early starts;
- hotel and total budget bands;
- food restrictions and special interests;
- desired output: chat plan, HTML, PDF, or all.

Infer low-risk preferences from the conversation. Do not repeat questions the user has already answered. State any assumption that changes transport, nights, or cost.

### 2. Research current facts

Browse the internet for all time-sensitive travel facts. Prefer sources in this order:

1. official attraction, government, transport, railway, airline, and rental-car sources;
2. official hotel or restaurant pages and current map listings;
3. established booking platforms;
4. recent first-hand notes such as Xiaohongshu, Mafengwo, or travel blogs for lived experience only.

Use social posts to find practical details and candidate businesses, not as the sole authority for ticket rules, road openings, safety restrictions, or schedules. Record source URLs and the date checked. Clearly label estimates and facts that remain unconfirmed.

Verify at least:

- opening hours, closed days, reservation method, release window, entry documents, shuttle rules, and refund rules;
- current road restrictions, seasonal closures, construction, border or permit requirements;
- train or flight feasibility and station/airport transfer time;
- rental pickup and return branch, business hours, one-way fee, mileage policy, fuel/charging, insurance, and snow-chain rules;
- hotel operating status, parking, heating or air conditioning, altitude, and room-view conditions;
- restaurant operating status, meal periods, reservation needs, and branch identity.

### 3. Optimize transport before the itinerary

Build a city-by-city transport matrix. Compare rail, flight, private transfer, local taxi, and self-drive by door-to-door time, cost, flexibility, parking burden, fatigue, and disruption risk.

For self-drive, state:

- exact pickup city, branch area, date, and preferred time;
- exact return city, branch area, date, and latest safe time;
- whether the rental is same-city or one-way;
- confirmed fee or a clearly labeled pending quote;
- suitable vehicle class and why;
- realistic driving time including refueling, meals, viewpoints, traffic, and altitude.

Do not disguise an overloaded day by quoting only navigation time. Flag any day above the user's comfort limit and offer:

- the recommended balanced route;
- a relaxed variant with the first sacrifice;
- a weather or disruption fallback.

Protect the final departure with an explicit buffer. Avoid same-day long mountain drives into a fixed flight or train unless the risk is surfaced and accepted.

### 4. Lock the calendar and consistency model

Create one source-of-truth table with:

- D-number;
- date and weekday;
- sleep location;
- transport mode;
- route and distance;
- realistic drive/transfer time;
- major activity;
- hotel night number;
- tickets or reservations due.

Make all later sections derive from this table. Enforce:

- number of day entries equals calendar days;
- number of hotel stays equals nights;
- every attraction booking maps to the correct visit date;
- hotel city matches the end of that day;
- pickup precedes driving and return follows the last drive;
- the departure ticket has enough transfer and check-in buffer.

When the user revises a route, search the whole deliverable for stale cities, distances, dates, ticket notes, hotel counts, and map labels before finalizing.

### 5. Write an executable day-by-day plan

For each day, provide:

- a compact headline with date, route, distance, and realistic time;
- a time-blocked schedule from wake-up or arrival through hotel check-in;
- exact visit order and what to see at each stop;
- recommended entrance, parking lot, shuttle, walking direction, and exit;
- meal area and named current restaurant candidates;
- latest safe departure time and a clear cut-off rule;
- hotel area plus two or three property candidates;
- reservations, weather triggers, driving cautions, and Plan B;
- one “skip this first” item if the day slips.

Do not list attractions without explaining how to visit them. Distinguish photo stops from full visits.

### 6. Add booking, lodging, food, packing, and risk modules

Read `references/deliverable-spec.md` and include all applicable modules.

Create a booking calendar with “when to act,” exact channel, identity documents, release time, cancellation rule, and backup. If official sale dates are not yet published, give a monitoring date and avoid fabricating a precise time.

Recommend lodging by area first, then property. Explain tradeoffs such as walking convenience, parking, early departure, view, heating, oxygen, noise, and price volatility.

Recommend food by city and meal occasion. Verify the correct branch, operating status, signature dishes, queue pattern, parking, and reservation need. Give alternatives instead of presenting one shop as guaranteed.

Include compact packing and safety checklists tailored to season, altitude, road type, children or older adults, and transport mode.

### 7. Build the rich HTML

Copy `assets/roadbook-template.html` as a structural starting point when an HTML deliverable is requested. Replace every `{{PLACEHOLDER}}`; duplicate the example day card as needed and remove sample instructions.

The page should include:

- an image-led hero with trip dates, route, duration, transport summary, and countdown;
- sticky navigation and reading progress;
- route overview and transport decision table;
- the master calendar;
- expandable day cards with timeline, visit method, food, hotel, booking, and fallback;
- booking calendar, lodging, food, packing, risk, budget, and sources;
- real destination and food images with captions and credits;
- restrained motion that respects `prefers-reduced-motion`;
- responsive mobile layout and a usable no-JavaScript state.

Use semantic HTML, unique IDs, accessible labels, useful alt text, strong contrast, and no essential information that exists only in animation.

For a file the user will send to others, produce a single-file version with local images embedded as data URLs:

```bash
python3 scripts/embed_html_images.py SOURCE.html SHAREABLE.html
```

Keep remote links clickable, but do not depend on local relative image paths, local fonts, or local scripts in the shareable file.

### 8. Produce the full-color PDF

When a PDF is requested, use the available PDF skill or a browser print engine. Preserve the complete guide rather than creating a reduced text-only version.

Before export:

- enable background graphics;
- use the template's print CSS;
- force expandable sections open in print;
- avoid splitting critical cards, tables, and day headers;
- add page numbers if they do not obscure content;
- ensure URLs and source labels remain readable.

Render every PDF page to images and inspect them. Fix clipping, blank pages, missing backgrounds, tiny text, broken CJK fonts, orphan headings, and hidden collapsed content before delivery.

### 9. Validate and hand off

Read `references/quality-checklist.md`.

Run the generic checks:

```bash
python3 scripts/validate_roadbook.py \
  --html SOURCE.html \
  --bundle SHAREABLE.html \
  --pdf GUIDE.pdf \
  --expected-days 8 \
  --must-contain "关键目的地"
```

Also compile or parse inline JavaScript with an available JS runtime. Treat warnings as work to resolve or disclose, not as decoration.

Deliver:

- the editable/source HTML;
- the shareable single-file HTML;
- the verified color PDF;
- a brief list of assumptions and facts that must be reconfirmed near departure;
- the source-check date.

Save user-facing artifacts in the designated output directory. Copy to Desktop only when the user asks and permission permits it.

## Non-negotiable rules

- Never invent a timetable, ticket rule, road opening, hotel amenity, restaurant status, or one-way rental fee.
- Never claim “no reservation needed” without a current source or clear qualification.
- Never let visual polish conceal route fatigue, altitude risk, or a missed-departure risk.
- Never use an image without a usable source, license basis, or explicit user ownership.
- Never deliver a “single-file” HTML that still depends on local file paths.
- Never finalize a PDF without rendering and visually checking all pages.

## Resource map

- `references/intake-and-research.md`: intake, evidence, route, and transport decisions.
- `references/deliverable-spec.md`: required content and HTML/PDF presentation contract.
- `references/quality-checklist.md`: final consistency and file validation checklist.
- `assets/roadbook-template.html`: reusable responsive, animated, print-aware skeleton.
- `scripts/embed_html_images.py`: embed local image files into a shareable HTML.
- `scripts/validate_roadbook.py`: detect duplicate IDs, missing images, unbundled assets, day-count errors, forbidden stale text, and basic PDF faults.
