# Maps and transport capability

Use maps and transport data according to what is actually connected. Never describe a fallback URL as a routing engine.

## Capability ladder

| Available capability | Action | Evidence label |
|---|---|---|
| Places plus routing/traffic tool | Resolve each stop, query each leg for the intended date and mode, retain provider and query time | live query |
| Official rail, airline, road, rental, or attraction source | Verify the published service and transfer assumptions | verified source |
| Current map listing or established booking platform | Use for operational cross-checks and candidates | current listing |
| No structured route source | Estimate conservatively and create map-opening links | estimate |

Do not infer that a tool exists from prose. Inspect the callable tools in the current session. If a useful tool is missing, continue with a transparent fallback; do not install a dependency or request credentials unless the user asks.

## Route-link fallback

Run the bundled helper with an explicit region:

```bash
python3 scripts/build_route_links.py \
  --region china \
  --city 上海 \
  --mode transit \
  --stops 人民广场 "上海博物馆东馆" 武康路
```

Provide at least two named stops. Supported generic modes are `walking`, `transit`, `driving`, and `bicycling`. The helper translates `bicycling` to Baidu's `riding` parameter. A China bundle requires a city because Baidu uses it to disambiguate named places.

The helper follows public provider URL formats and performs no network request:

- International routes use Google Maps. Long routes are split into mobile-safe chunks while preserving the handoff stop.
- Mainland-China routes use one Baidu directions link per consecutive leg, so no stop disappears. They also include an Amap keyword-search link for each stop.
- Region is explicit. Never guess mainland-China status from a city string.
- Place names are handed to the provider for resolution. Check ambiguous branches before delivery.

Build the complete final link set after the route is accepted and the user selects a roadbook or navigation-link artifact. Draft links may be used earlier when they help resolve a route decision, but they are not the final link set. Each final link's origin and destination must exactly match the chronological travel block it accompanies. For mixed modes, generate separate same-mode sequences or one link per leg. After any stop change, regenerate affected links and compare every link label and encoded endpoint against the timetable; never reuse a convenient but stale anchor.

Provider documentation:

- Google Maps URLs: https://developers.google.com/maps/documentation/urls/get-started
- Amap search URI: https://lbs.amap.com/api/uri-api/guide/search/search
- Baidu web direction URI: https://lbsyun.baidu.com/docs/webapi?title=mapadjustment%2Furi%2Fweb

Map URLs reveal the encoded stop names to the chosen provider. Warn before including a private home address, a precise hotel room location, or a full future itinerary in a publicly shared page.

## Time and route evidence

For every travel leg record:

- origin and destination;
- mode;
- planned start and end;
- realistic minutes;
- basis: `live`, `verified`, or `estimated`;
- provider/source and checked time when available;
- buffer and the risk it covers.

Link generation does not supply any of these measurements. When only a link exists, calculate a conservative estimate separately and label it `estimated`.

## Intercity transport

For rail, flight, coach, ferry, and private transfers, compare the complete chain: accommodation checkout, terminal access, security or boarding buffer, service time, baggage, arrival transfer, and check-in.

If an approved query-only rail or flight tool is connected, return a concrete service number, departure, arrival, duration, price status, availability timestamp, and official purchase channel. If not, link the official search channel and mark the service `pending`.

Do not claim that an MCP can purchase a ticket unless its documented, user-approved scope explicitly includes that action. This skill's default boundary is query and handoff only.

## Self-drive

Record branch-level pickup and return details, opening hours, vehicle and luggage fit, one-way fee status, deposit/payment requirements, mileage, fuel or charging, insurance exclusions, second driver, roadside support, tires/chains, tolls, parking, and the final safe return time.

Navigation time is the lower bound. Add paperwork, fuel, meals, viewpoints, congestion, parking search, checkpoints, weather, darkness, altitude, and recovery time.

## Complete maps and importing

When requested, follow `navigation-and-import.md`. The existing route-link helper is a formatter, not an importer or complete map renderer. Supply all-day diagram plus geographic/road detail at the available evidence level, and disclose cross-city name-resolution limitations.
