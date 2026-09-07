# Revision and route audit

Read this file whenever the user changes a route, questions drive time or distance, restores a previously removed experience, or asks to update existing HTML/PDF artifacts.

## 1. Preserve the accepted trip contract

Maintain this ledger:

| Class | Examples | Revision rule |
|---|---|---|
| Fixed anchor | dates, 8 days/7 nights, arrival, departure flight | Change only when the user explicitly changes it |
| Must-have | destination, scenic road, sunrise, food experience | Preserve unless a conflict is surfaced and traded explicitly |
| Preference | two nights in one city, rail in cities, short drives | Optimize around it and state compromises |
| Rejected | route or attraction the user disliked | Do not resurface as the default |
| Pending | unpublished ticket rule, rental fee, road opening | Keep labeled; schedule a recheck |

After a major revision, summarize the new accepted state in one compact block:

- dated sleep sequence;
- transport sequence;
- pickup and return;
- must-haves retained;
- longest day and realistic elapsed time;
- first sacrifice if the route slips.

## 2. Decide whether a road is transport or an attraction

Ask of every road segment:

1. Is the user choosing it for scenery or driving experience?
2. Does it contain named viewpoints, villages, passes, or short walks?
3. Would taking the expressway remove the reason for driving?

If yes, classify it as a scenic-drive attraction. Plan it like a major sight:

- specify navigation waypoints so routing software cannot silently choose the expressway;
- separate safe photo stops from full visits;
- state parking or official pullout behavior;
- budget wheel time, stops, meals, fuel, and buffer separately;
- define a weather/single-driver fallback;
- remove lower-value city attractions before removing the road itself.

Do not use a landscape from an unrelated attraction as if it depicts the road. Label representative imagery honestly or find route-specific licensed media.

## 3. Normalize disputed distance and time

When the user says another itinerary reports a different number, build this comparison:

| Variable | Current route | Compared route |
|---|---|---|
| Start/end | exact hotel, city edge, station, or attraction | exact equivalent |
| Waypoints | every mandatory stop | every mandatory stop |
| Road class | expressway, national road, scenic old road | same |
| Detours | parking, viewpoint, town entry | same |
| Distance | navigation estimate and check date | same |
| Wheel time | without visits | same |
| Stop time | visits, food, fuel, photos | same |
| Realistic elapsed | door to door | same |

Explain the delta before updating the route. Typical causes:

- a city name was used instead of a distant attraction or hotel;
- a return leg or optional loop was counted twice;
- the fast route and scenic route used different waypoints;
- one figure is wheel time while another includes sightseeing;
- a map selected a remote gate or wrong branch.

## 4. Rebuild from the master table

Do not patch prose first. Apply revisions in this order:

1. Update the constraint ledger.
2. Recompute dated sleeps and hotel-night count.
3. Recompute transport, route, distance, wheel time, and realistic elapsed time.
4. Recompute rental pickup/return and fixed-departure buffers.
5. Recompute attraction visits and booking states.
6. Update the source-of-truth calendar.
7. Regenerate all derived sections and artifacts.

## 5. Propagate every change

Search and update:

- title, metadata, hero, metrics, decision summary, and route diagram;
- master table and every detailed day;
- booking calendar and reservation explanations;
- hotels, restaurants, packing, risk, and budget;
- images, captions, alt text, and credits;
- source list and check date;
- footer, filename, shareable bundle;
- PDF cover, section summaries, page headers, and closing card;
- README/example artifacts when the skill project itself is being updated.

Build a regression list with distinctive stale tokens, such as the removed city, old distance, old departure time, or old phrase. Pass every token through `--forbid`.

## 6. Audit fatigue honestly

For each driving day, show:

`realistic elapsed = wheel time + visits + meals + fuel/rest + parking/queues + disruption buffer`

If scenic driving and a second mountain leg share one day:

- state that it is the hardest day;
- give single-driver and two-driver guidance;
- establish hard cutoffs;
- name the exact stops removed at each missed cutoff;
- prohibit night driving from becoming the hidden recovery plan.

If the user keeps all fixed nights and all must-haves, present the resulting long day plainly. Do not manufacture a “relaxed” label.

## 7. Keep artifacts on one revision

Use one content model wherever possible. Add a revision identifier to source HTML and the bundled HTML. Make the PDF read from the same model or source HTML.

After generation:

1. validate day and night counts;
2. require new route tokens;
3. forbid stale route tokens in source, bundle, and PDF;
4. confirm the bundled HTML has no local image or CSS asset path;
5. render every PDF page and inspect it;
6. check that route-specific images and captions still match the revised itinerary.
