# Quality checklist

## Planning state and delivery choice

- [ ] Quick or Roadbook mode matches the trip complexity.
- [ ] Planning resolves every material fact, conflict, and dependency before final-file generation.
- [ ] The itinerary is internally consistent and accepted before it enters Ready.
- [ ] With no selected product, Ready offers roadbook with links, roadbook plus PDF and links, links only, or continued revision.
- [ ] An explicit artifact request skips only that product-choice prompt; it does not skip fact resolution or acceptance.
- [ ] Final navigation links use the accepted timetable, not a draft.

## Route and calendar

- [ ] Arrival and departure use exact local dates, times, and terminals.
- [ ] Fixed anchors, must-haves, preferences, rejected options, and pending facts are recorded.
- [ ] D1 through DN are consecutive and match inclusive calendar days.
- [ ] Sleep entries equal hotel nights.
- [ ] Every declared must-have remains present, including scenic roads and experiences.
- [ ] Rejected routes are not resurfaced as the default.
- [ ] Every day's hotel city matches the route endpoint.
- [ ] All distances and times use the intended waypoints and correct endpoints.
- [ ] Compared distances use normalized endpoints, waypoints, and road classes.
- [ ] Long days show realistic elapsed time, cut-off, and first sacrifice.
- [ ] Scenic-drive days separate wheel time, visit time, stops, and total elapsed time.
- [ ] Single-driver and two-driver assumptions are explicit.
- [ ] The final departure has a stated buffer and fallback.
- [ ] No deleted destination survives in titles, maps, bookings, food, hotels, or budget.

## Transport and rental

- [ ] Every intercity leg has a chosen mode and reason.
- [ ] Train/flight times are current or clearly labeled pending.
- [ ] Pickup and return city, branch area, date, and time are explicit.
- [ ] One-way fee is confirmed or clearly pending.
- [ ] Rental opening hours work with the itinerary.
- [ ] Vehicle, luggage, insurance, mileage, fuel/charge, and winter equipment are addressed.
- [ ] Each selected navigation link has the same origin, destination, mode, and ordering as its accepted travel block.

## Attractions and reservations

- [ ] Each major attraction explains how to visit, not only what it is.
- [ ] Entry, parking, shuttle, walk, and exit order are usable.
- [ ] Opening days and seasonal access are checked.
- [ ] Booking channel, release window, required IDs, refund, and Plan B are present.
- [ ] Claims that no booking is needed are qualified and sourced.
- [ ] Every planned attraction/road stop has an explicit booking status, including free or pending stops.

## Hotels and food

- [ ] Hotel area logic is explained.
- [ ] Named hotels are current and have one disclosed tradeoff.
- [ ] View, parking, heating, oxygen, and breakfast claims are not exaggerated.
- [ ] Named restaurants use the correct branch and current operating evidence, or disclose a non-critical verification gap; no unresolved sole food-supply dependency is treated as ready.
- [ ] Every key restaurant meal has a backup, or an explicit evidence shortage that does not leave a critical food-supply dependency unresolved.
- [ ] Dietary and altitude-related food cautions are included when relevant.

## Sources and media

- [ ] Critical claims link to authoritative sources.
- [ ] Social posts are supplementary and recent.
- [ ] Source-check date is shown.
- [ ] Images have usable provenance, alt text, and credits.
- [ ] Shareable HTML contains no local absolute paths or unresolved relative images.

## HTML

- [ ] No duplicate IDs.
- [ ] No unresolved `{{PLACEHOLDER}}` tokens.
- [ ] All local images exist in source HTML.
- [ ] Single-file edition embeds all local images.
- [ ] Hero and CSS background images are embedded; no local `url(...)` remains.
- [ ] Source and bundled HTML use the same revision identifier.
- [ ] Every day card has `data-day` and `data-sleep`; counts match the contract.
- [ ] Inline JavaScript compiles.
- [ ] Navigation anchors resolve.
- [ ] Countdown uses the correct local start date.
- [ ] Page remains useful without animation.
- [ ] Mobile width has no horizontal overflow.
- [ ] Reduced-motion and accessible labels are present.

## PDF

- [ ] PDF opens and is not encrypted.
- [ ] Page count is plausible and text is extractable.
- [ ] Every page has been rendered to an image and inspected.
- [ ] Backgrounds and photographs are visible.
- [ ] All day cards are expanded.
- [ ] No clipping, blank pages, broken fonts, orphan headings, or tiny tables.
- [ ] Important links and source labels remain readable.
- [ ] PDF contains the new route tokens and none of the forbidden stale tokens.
- [ ] PDF cover, footer, metrics, and day images match the same revision as the HTML.

## Final handoff

- [ ] Only selected artifacts are presented as final, and each selected file is clearly named and linked.
- [ ] Every selected navigation-link leg is present or has a leg-specific explanation of what cannot yet be supplied.
- [ ] A change-impact search covered summaries, route diagram, days, bookings, stays, food, budget, images, sources, footer, and PDF-only text.
- [ ] Final facts-to-reconfirm list is concise and actionable.
- [ ] Assumptions are disclosed.
- [ ] Files are in the requested output location.

## Xiaohongshu travel and food review

These are semantic review checks; the existing HTML/PDF validator does not verify live sources or these evidence fields.

- [ ] Food/travel research attempted available Xiaohongshu search/detail capabilities, or explicitly disclosed the access gap and fallback.
- [ ] Full notes/comments and search snippets are distinguished; no invented popularity, source URLs, dates, or read claims.
- [ ] Primary experience recommendations use independent cross-checks; marketing, duplicates, stale posts, and material contradictions affect confidence.
- [ ] Each restaurant meal has a concrete branch, dishes, reasons, route fit, and 1–2 alternatives, or an explicit shortage of evidence; hotel/packed/onboard meals are identified.
- [ ] Parking, queues, reservation and opening details are sourced or pending; waiting and detours fit the schedule and diet.
- [ ] Attractions cover visit method, pitfalls, photo spots, timing, parking, and recent experience where relevant.
- [ ] Self-drive covers recent experience, road surface, scenery, safe parking, fuel, sedan suitability, and darkness; official restrictions prevail.
- [ ] Research covers the actual planned destinations and experiences without imposing a fixed regional list; weather-dependent experiences have current checks and a fallback.
- [ ] Weather outside forecast range remains pending with a recheck date; old sunshine photos do not establish a forecast.
- [ ] Experience confidence is separate from verified operating facts, with source links and check dates retained in the master plan and relevant outputs.
- [ ] Meal revisions propagate through travel blocks, alternatives, navigation, budgets, HTML and PDF without changing accepted anchors or artifact-selection gates.
