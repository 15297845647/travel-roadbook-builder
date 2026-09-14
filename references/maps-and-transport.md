# Maps and transport capability

Use maps and transport data according to what is actually connected. Label unverified distances and durations as estimates.

## Capability ladder

| Available capability | Action | Evidence label |
|---|---|---|
| Places plus routing/traffic tool | Resolve each stop, query each leg for the intended date and mode, retain provider and query time | live query |
| Official rail, airline, road, rental, or attraction source | Verify the published service and transfer assumptions | verified source |
| Current map listing or established booking platform | Use for operational cross-checks and candidates | current listing |
| No structured route source | Estimate conservatively and provide ordered place names | estimate |

Do not infer that a tool exists from prose. Inspect the callable tools in the current session. If a useful tool is missing, continue with a transparent fallback; do not install a dependency or request credentials unless the user asks.

## Route consistency

Each leg's origin, destination and mode must exactly match the chronological travel block. For mixed modes, keep each segment separate. After a stop changes, reconcile the route description with the accepted timetable. Resolve ambiguous branches before finalizing the plan.

## Time and route evidence

For every travel leg record:

- origin and destination;
- mode;
- planned start and end;
- realistic minutes;
- basis: `live`, `verified`, or `estimated`;
- provider/source and checked time when available;
- buffer and the risk it covers.

When route measurements are unavailable, calculate a conservative estimate and label it `estimated`.

## Intercity transport

For rail, flight, coach, ferry, and private transfers, compare the complete chain: accommodation checkout, terminal access, security or boarding buffer, service time, baggage, arrival transfer, and check-in.

If an approved query-only rail or flight tool is connected, return a concrete service number, departure, arrival, duration, price status, availability timestamp, and official purchase channel. If not, link the official search channel and mark the service `pending`.

Do not claim that an MCP can purchase a ticket unless its documented, user-approved scope explicitly includes that action. This skill's default boundary is query and handoff only.

## Self-drive

Record branch-level pickup and return details, opening hours, vehicle and luggage fit, one-way fee status, deposit/payment requirements, mileage, fuel or charging, insurance exclusions, second driver, roadside support, tires/chains, tolls, parking, and the final safe return time.

Navigation time is the lower bound. Add paperwork, fuel, meals, viewpoints, congestion, parking search, checkpoints, weather, darkness, altitude, and recovery time.
