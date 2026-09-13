---
name: travel-roadbook-builder
description: Use when Codex plans or revises a single-day or multi-day trip, compares routes or transport, handles self-drive, rail, or flight logistics, prepares reservations, or creates a travel roadbook, shareable HTML, navigation links, or PDF.
---

# Travel Roadbook Builder

Create a trip that can actually be booked and followed. Resolve and confirm the itinerary before making final files; optimize the route before decorating it, and verify unstable facts before presenting them as reliable.

## Required workflow

### 1. Choose the planning and delivery state

Use the lightest planning depth that keeps the result safe:

| Mode | Appropriate scope | Minimum result |
|---|---|---|
| Quick mode | One day, a short city visit, a route sketch, or chat-only advice | Compact contract, ordered stops, time blocks, cut-off, and fallback |
| Roadbook mode | Multiple days or cities, self-drive, fixed departures, reservations, lodging, or generated files | Structured plan, transport decision, dated calendar, detailed days, and applicable booking modules |

Planning depth and final-file selection are separate. Move through these states in order:

1. **Planning** — resolve the contract, evidence, route, schedule, and material dependencies.
2. **Ready** — all material facts and choices are internally consistent and the user has accepted the itinerary.
3. **Generating** — create only the final artifacts the user selected.

When the plan is Ready and the user has not selected artifacts, say plainly that the itinerary is confirmed and offer these choices in the user's language:

1. shareable single-file roadbook with complete navigation links (recommended);
2. roadbook, PDF, and navigation links;
3. navigation links only;
4. continue revising without generating files.

Do not imply that final files already exist before this choice. When the user explicitly requested an artifact set, that request selects the product only: it never removes the need to settle material facts or obtain itinerary acceptance. Once facts are accepted, enter Generating without repeating the product-choice question. Build final links only from the accepted timetable, never an earlier draft.

### 2. Establish the trip contract

Read `references/intake-and-research.md`.

Extract or ask only for decisions that materially change the route:

- exact arrival and departure date, time, airport, railway station, or city;
- total calendar days and hotel nights;
- must-see places and explicitly droppable places;
- travelers, ages, health limits, number of drivers, and luggage;
- maximum comfortable driving time and tolerance for early starts;
- hotel and total budget bands;
- food restrictions and special interests;
- desired output, if already known: chat plan, shareable roadbook with links, roadbook plus PDF and links, or links only.

Infer low-risk preferences from the conversation. Do not repeat questions the user has already answered. State any assumption that changes transport, nights, or cost.

Maintain a compact constraint ledger throughout the thread:

- fixed anchors: arrival, departure, calendar days, hotel nights, and booked tickets;
- must-haves, including scenic roads and experiences rather than only named attractions;
- preferences and comfort ceilings;
- explicitly rejected or replaced options;
- pending facts that still require verification.

Treat the latest message as a change to this ledger, not permission to forget earlier accepted constraints. After a major revision, restate the resulting nights, must-haves, rental segment, and longest day before rebuilding artifacts.

### 3. Research current facts

Browse the internet for all time-sensitive travel facts. For food and travel recommendations, default to combining recent first-hand Xiaohongshu content with authoritative checks. Read `references/xiaohongshu-travel-and-food.md` for capability discovery, searches, evidence grading, and destination-specific research. Prefer sources in this order:

1. official and real-time information: government, attraction/operator, transport, weather, railway, airline, rental-car, hotel, and restaurant sources;
2. current maps/navigation for branch identity, location, route, and live traffic;
3. recent first-hand Xiaohongshu notes and substantive comments for lived experience;
4. other guides, traveler reports, and established booking platforms as supplementary discovery sources.

Apply this hierarchy by claim: live booking inventory and exact transaction terms come from the operator or booking system, never from social popularity. Closures, weather, and opening rules require official/current evidence. If Xiaohongshu access is unavailable, disclose the limitation and use the reference's fallback; never imply unread notes or comments were verified.

Use social posts to find practical details and candidate businesses, not as the sole authority for ticket rules, road openings, safety restrictions, or schedules. Record source URLs and the date checked. Clearly label estimates and facts that remain unconfirmed.

For every planned attraction, including free viewpoints and road stops, assign one booking state: confirmed rule, sales not open, monitor, optional/no ticket, or pending verification. Do not omit a stop merely because it may not require a ticket.

Verify at least:

- opening hours, closed days, reservation method, release window, entry documents, shuttle rules, and refund rules;
- current road restrictions, seasonal closures, construction, border or permit requirements;
- train or flight feasibility and station/airport transfer time;
- rental pickup and return branch, business hours, one-way fee, mileage policy, fuel/charging, insurance, and snow-chain rules;
- hotel operating status, parking, heating or air conditioning, altitude, and room-view conditions;
- restaurant operating status, meal periods, reservation needs, and branch identity.

### 4. Optimize transport before the itinerary

Read `references/maps-and-transport.md`. Use the highest available live or authoritative transport capability, and label estimates and map-opening links honestly.

Build a city-by-city transport matrix. Compare rail, flight, private transfer, local taxi, and self-drive by door-to-door time, cost, flexibility, parking burden, fatigue, and disruption risk.

Classify every intercity road segment before optimizing it:

- utility transfer;
- scenic-drive attraction;
- access road to a major attraction;
- urban segment where a car is a burden;
- protected departure leg.

If the user values a scenic road, treat the road and its viewpoints as a must-see attraction. Do not silently replace it with a faster expressway or delete it merely to shorten the day. First remove duplicative city sightseeing, low-value detours, or optional stops; if the remaining day is still unsafe, surface the conflict and offer a specific sacrifice.

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

When the user questions a distance or drive time, normalize both routes before answering: exact start/end points, waypoints, road class, detours, pure wheel time, stops, and realistic elapsed time. Show which difference creates the delta. Do not defend an old number or rewrite the artifact until the discrepancy is understood.

### 5. Lock the calendar and consistency model

For Roadbook mode, for generated roadbooks, and for revisions with cross-day dependencies, read `references/plan-data-model.md`. Keep one structured plan as the authoritative record. The displayed master table, day cards, booking calendar, navigation links, HTML, and PDF must be derived from it rather than maintained as competing calendars.

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

When the user revises a route, read `references/revision-and-route-audit.md`. Recompute the master table first, then propagate the change through every summary, route diagram, day card, booking item, hotel, food, budget, image, source, PDF cover, and footer. Search for stale cities, distances, dates, ticket notes, hotel counts, map labels, and rejected wording before finalizing.

### 6. Write an executable day-by-day plan

For each day, provide:

- a compact headline with date, route, distance, and realistic time;
- a time-blocked schedule from wake-up or arrival through hotel check-in;
- exact visit order and what to see at each stop;
- recommended entrance, parking lot, shuttle, walking direction, and exit;
- meals with one named primary restaurant and 1–2 nearby alternatives, recommended dishes, evidence-based reasons, relation to the day’s route, and applicable parking/queue/reservation notes; label unresolved details and evidence gaps rather than inventing shops;
- latest safe departure time and a clear cut-off rule;
- hotel area plus two or three property candidates;
- reservations, weather triggers, driving cautions, and Plan B;
- one “skip this first” item if the day slips.

Do not list attractions without explaining how to visit them. Distinguish photo stops from full visits.

For any long scenic-drive day, separate:

- route-only wheel time;
- planned attraction and photo-stop time;
- meals, refueling, parking, and recovery buffer;
- total realistic elapsed time;
- driver load for one driver versus two;
- the exact time or condition that triggers the faster fallback.

### 7. Add booking, lodging, food, packing, and risk modules

Read `references/deliverable-spec.md` and include all applicable modules.

Create a booking calendar with “when to act,” exact channel, identity documents, release time, cancellation rule, and backup. If official sale dates are not yet published, give a monitoring date and avoid fabricating a precise time.

Recommend lodging by area first, then property. Explain tradeoffs such as walking convenience, parking, early departure, view, heating, oxygen, noise, and price volatility.

Recommend food by city and meal occasion using `references/xiaohongshu-travel-and-food.md`. Prioritize recent independent notes, meaningful comments, repeated mentions, and saves over raw popularity; screen obvious marketing and fit the accepted route and diet. Verify the correct branch, operating status, signature dishes, queue pattern, parking, and reservation need. Give one primary choice plus 1–2 alternatives per planned restaurant meal, with confidence and source links; never present a candidate as booked or guaranteed.

Include compact packing and safety checklists tailored to season, altitude, road type, children or older adults, and transport mode.

### 8. Build the rich HTML

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

Keep remote links clickable, but do not depend on local relative image paths, CSS background-image files, local fonts, or local scripts in the shareable file. Prefer semantic `<img>` elements for hero photography so the bundler and accessibility checks can see them.

### 9. Produce the full-color PDF

When a PDF is requested, use the available PDF skill or a browser print engine. Preserve the complete guide rather than creating a reduced text-only version.

Generate PDF narrative, metrics, and day data from the same source model or HTML. Avoid manually duplicating route facts in a second generator. If hardcoded cover or footer text is unavoidable, add its distinctive old wording to the validator's forbidden-token regression list after every revision.

Before export:

- enable background graphics;
- use the template's print CSS;
- force expandable sections open in print;
- avoid splitting critical cards, tables, and day headers;
- add page numbers if they do not obscure content;
- ensure URLs and source labels remain readable.

Render every PDF page to images and inspect them. Fix clipping, blank pages, missing backgrounds, tiny text, broken CJK fonts, orphan headings, and hidden collapsed content before delivery.

### 10. Validate and hand off

Read `references/quality-checklist.md`.

Run the generic checks:

```bash
python3 scripts/validate_roadbook.py \
  --html SOURCE.html \
  --bundle SHAREABLE.html \
  --pdf GUIDE.pdf \
  --expected-days 8 \
  --expected-nights 7 \
  --expected-revision "YOUR-REVISION-ID" \
  --must-contain "关键目的地" \
  --forbid "已删除的旧路线措辞" \
  --strict-pdf-text
```

Use a revision token in both source and bundled HTML when practical, and pass `--expected-revision`. Also compile or parse inline JavaScript with an available JS runtime. Treat warnings as work to resolve or disclose, not as decoration.

Deliver only the selected artifacts:

- the editable/source HTML when requested;
- the shareable single-file HTML when requested;
- the verified color PDF when requested;
- complete route-navigation links when selected, one per consecutive accepted route leg unless a leg-specific limitation is stated;
- a brief list of assumptions and facts that must be reconfirmed near departure;
- the source-check date.

Verify that every selected file exists before handoff and provide clickable file links. Save user-facing artifacts in the designated output directory. Copy to Desktop only when the user asks and permission permits it.

## Non-negotiable rules

- Never invent a timetable, ticket rule, road opening, hotel amenity, restaurant status, or one-way rental fee.
- Never claim “no reservation needed” without a current source or clear qualification.
- Never drop or downgrade a declared must-have, including a scenic road, without naming the conflict and obtaining an explicit tradeoff.
- Never compare route distances that use different endpoints or waypoints without showing the normalization.
- Never let visual polish conceal route fatigue, altitude risk, or a missed-departure risk.
- Never use an image without a usable source, license basis, or explicit user ownership.
- Never deliver a “single-file” HTML that still depends on local file paths.
- Never finalize a PDF without rendering and visually checking all pages.
- Never patch only the visible day card; propagate every accepted revision across HTML, bundled HTML, PDF, and their manually duplicated summaries.
- Never generate final artifacts before material itinerary facts are resolved and the user accepts the plan.
- Never create final navigation links from a superseded timetable.

## Resource map

- `references/intake-and-research.md`: intake, evidence, route, and transport decisions.
- `references/xiaohongshu-travel-and-food.md`: default Xiaohongshu search/detail capability routing, food/attraction/driving queries, confidence grading, daily meals, and weather-aware experience research.
- `references/maps-and-transport.md`: routing capability ladder, navigation-link fallback, exact leg reconciliation, and privacy boundary.
- `references/revision-and-route-audit.md`: constraint ledger, scenic-road decisions, route discrepancy analysis, and revision propagation.
- `references/plan-data-model.md`: structured source-of-truth plan and consistency invariants.
- `references/deliverable-spec.md`: required content and HTML/PDF presentation contract.
- `references/quality-checklist.md`: final consistency and file validation checklist.
- `references/provenance.md`: rules for adding third-party materials and recording their provenance.
- `assets/roadbook-template.html`: reusable responsive, animated, print-aware skeleton.
- `scripts/embed_html_images.py`: embed local image files into a shareable HTML.
- `scripts/build_route_links.py`: generate provider handoff links without claiming live routing or traffic data.
- `scripts/validate_roadbook.py`: detect duplicate IDs, missing images, unbundled assets, day-count errors, forbidden stale text, and basic PDF faults.
