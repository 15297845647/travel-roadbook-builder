# Route maps, navigation handoff, and importing

Read for requested route maps, Amap/Baidu support, importing, or revisions to navigation deliverables. Preserve the accepted timetable and artifact selection; a map upgrade alone does not reopen itinerary approval.

## Distinguish the products

| Product | What it proves | What it does not prove |
|---|---|---|
| Complete itinerary diagram | Every accepted day/stop/transport leg is represented | Geographic scale, road alignment, drive time |
| Geographic waypoint overview | Locations with sourced coordinates are placed geographically | Straight connections are not roads |
| Provider road geometry | A named provider returned the specified ordered road route at the check time | Future road opening or unchanged navigation |
| Map-opening link | Named endpoints/mode are handed to a provider | Saved route, successful import, or verified location match |
| KML/GPX visualization import | The target accepts and displays geometry | Turn-by-turn navigation or mobile cloud sync |
| Account-saved route | The target UI confirms saved stops and order | Public sharing or permission to upload other private data |

When the user requests a complete route map, produce a trip-wide view and day-level details from the same plan. Include flights/rail as distinct transport, repeated hotel returns, optional branches and scenic waypoints. Never present a link list alone as a route map. If road geometry is unavailable, still finish the diagram, label schematic lines prominently, and explain the specific missing capability for road-following navigation.

## Data contract and export

Keep stable stop IDs, day/sequence, full locality/branch, travel mode and optional status. Coordinates require source, coordinate system and precision; a town centre is not a hotel/parking entrance. Resolve ambiguous search hits using locality, not first-result order. Do not force all cross-city searches into the origin city.

Use `scripts/navigation_export.py --plan PLAN.json --output ROUTE.kml` only after adding evidenced `route_geometry` entries:

```json
{"name":"D2 ordered scenic segment", "geometry_kind":"schematic_waypoint_connection", "crs":"WGS84", "coordinates":[[121.0,31.0],[121.1,31.1]], "source_urls":["https://example.org/actual-coordinate-source"], "description":"Illustrative connections; not navigable road geometry"}
```

The example is schema-only, not a usable itinerary. `provider_road_geometry` requires an actual provider route response, preserved request/order and check time. The exporter rejects unknown coordinate systems or absent sources; it does not geocode, calculate roads, create accounts, upload or save routes.

KML/GPX use WGS84. Amap GCJ-02 and Baidu BD-09 cannot be relabeled as WGS84. Record any genuine conversion and its uncertainty. Never fabricate elevation, timestamps, GPS recording history or an estimated road polyline by joining town points. Do not infer road distance from schematic lines. Offer per-day files if a target merges multi-record files or its point limits would lose stops; when a single whole-trip import is required, splitting is a scope change requiring user acceptance.

## Mobile-only receiving and saving

When the user requires phone-only import, do not substitute PC KML visualization, PC Excel upload, or a link that merely opens navigation. Prefer a provider-generated route share that the recipient can copy/save inside the phone app. Do not require recipients to log in on a computer. A provider-native share is not generic file import.

Amap iPhone UI was tested on 2026-09-14 with a two-place route: creator opens Favorites → Routes → Created → Create route → Add places → Share → Copy link; recipient opens that generated link on the phone, allows opening Amap, then uses **图中提及 → 复制行程 → 保存并预览**. The result was an editable saved route. **添加至收藏夹** was also visible, but its separate behavior was not tested. Same-device/account copy was tested; different-account receiving remains a separate test. App version was not captured; inspect current labels rather than assuming the flow exists everywhere.

The copy unexpectedly defaulted to public; inspect **编辑 → 设置权限** after saving and preserve the user's intended visibility (private for personal trip drafts). Never equate the creator's private setting with the copied route's setting. A generated share can show creator attribution and itinerary places; avoid adding medical details or other unnecessary personal information.

Generate genuine shares from actual saved provider routes. Do not synthesize undocumented collection IDs, change opaque share parameters, or label URI endpoint links as saved-route imports. For full itineraries, populate and verify all accepted day/stop groups before calling the map complete; a two-place trial proves only that trial. Preserve rail/flight modes and scenic waypoints; a multi-day collection must not be represented as one continuous driving navigation. Check waypoint order after copy; do not infer that one-click navigation preserves all route choices without inspection.

Baidu must have its own current receiving/save test; success with Amap does not establish Baidu import compatibility. When the user accepts either provider, one verified provider can satisfy platform compatibility, but the requested trip content must still be completed.

## Whole-trip import with day groups

When the user requests one import of the entire trip with days distinguished, the deliverable contract is **one provider-native trip/map collection, one receiving link or QR code, one recipient save/copy flow, with D1–Dn day groups inside**. Derive n and dates from the accepted plan; never hardcode a destination or trip length.

- Preserve each day's date, ordered stops, hotels, meal venues, transport modes and required scenic waypoints. Mark alternatives/optional stops separately so they are not silently inserted into the main route. Retain repeated visits and hotel returns in their correct days rather than globally deduplicating them.
- Keep day groups inside the imported collection. Day prefixes on a flat list are not proof of native grouping. An HTML landing page containing separate daily import links also does not satisfy one whole-trip import.
- A trip collection is not one continuous driving route: flights, rail transfers, walking, overnight breaks and optional branches must remain distinguishable. Start driving guidance for the selected day's applicable segment.
- Verify separately that the target supports the total point count, day groups, whole-collection sharing and preservation of groups/order on receipt. A successful two-place copy test establishes none of those full-trip properties.
- Before calling delivery complete, compare the saved/imported collection against the accepted plan: day count/dates, per-day stop counts/order, group labels, repeated stops and required waypoints. Confirm the real receiving link targets the full collection, not a trial or one day.
- If access or platform limits prevent this result, state the exact unmet property and keep the whole-trip import status incomplete. Do not silently substitute many leg links, daily files, a schematic KML, or require desktop login by the recipient. Offer a changed scope only as an explicit tradeoff for the user to accept.
- Respect the user's chosen test boundary. If they will test on their phone or prohibit mirroring, do not connect to or operate the phone; record their feedback as user-reported evidence, separately from agent verification. Do not change account visibility or publish a collection merely to make a link work without the applicable authorization.

## Platform capability snapshot — verify again when used

Checked 2026-09-14; distinguish documentation support from the current user's working UI.

**Amap:** Official PC help documents KML/GPX track visualization, local-browser history and no automatic sharing/cloud sync. Its importer describes WGS84 conversion and a 10MB limit. Use the actual tool at `https://www.amap.com/track-import`; if it opens the legacy map or login surface, report that state instead of claiming a tested import. Verify the current UI and any upgrade/login requirement.

- https://www.amap.com/ssr/doc/track-import
- https://www.amap.com/ssr/doc/route-plan

For real navigation, use an ordered multi-waypoint route, inspect the chosen roads, then the supported save/share/send-to-phone control if available. Do not confuse SDK limits with web/app limits. PC route help currently describes 16 intermediate points; split without dropping the overlap node when necessary. Test the result on the available surface; label phone behavior untested if no phone is connected.

Amap map mini-program Excel import is a separate point-import path: download and preserve the **actual current template**, its sheets and headers. Fill verified coordinates or sufficiently detailed addresses. A custom CSV/XLSX with guessed headers is only staging data, never an import-ready file. Without template access, finish the staging data and guide, state the blocker, and do not request repeated logins without new evidence. Its route optimization can reorder scenic points; use manual accepted order and inspect it before saving.

- https://lbs.amap.com/api/wia/tutorial/content/import
- https://lbs.amap.com/api/wia/tutorial/route/plan_route

**Baidu:** Official URI API supports place/route handoff without an API key. Provide tested named endpoint links and a current UI guide for adding waypoints/saving where available. Do not promise general KML/GPX import in the consumer app unless a current official source or successful target UI test establishes it. Developer LBS cloud bulk-data services are not consumer route import.

- https://api.map.baidu.com/lbsapi/cloud/uri.htm
- https://lbsyun.baidu.com/docs/webapi?title=mapadjustment%2Furi%2Fweb

## Put the guide inside every selected roadbook format

Include the provider/client, capability and test date; exact supplied filenames; step-by-step open/import/save/send instructions; expected success state; and these fallbacks:

- Link does not launch the app: open in system browser, or copy exact locality/branch into the map search.
- Point matches wrong branch: verify listing/address; unresolved points remain clearly pending.
- Waypoint cap: split navigation segments at a shared node, preserving order and mode; this does not relax a separately requested single-collection import requirement.
- Automatic optimization changes a scenic route: restore required waypoints; never force travel through a closure.
- No importer/template/login access: supply the complete local map and staged data with a disclosed limitation; do not call it imported.

State what is local versus sent to the provider and whether a link/map is public. Generate requested files autonomously; get task-specific authorization before account upload/publishing where not already authorized. Avoid including health notes, credentials or unnecessary private identifiers in import data.

## Validation and delivery

Check day/stop/leg counts, IDs and ordering against the accepted plan; parse KML/GPX; check coordinate ranges/CRS/source; inspect the full diagram and printed PDF; verify links encode their labels. Test importer on the target where available and authorized; document `generated`, `schema_checked`, `target_tested`, `saved` independently.

Propagate a revision through map, navigation, import file, instructions, HTML, PDF and package. Use absolute clickable local paths at handoff and verify each file exists. Opening a tab queued by the app is not evidence the file rendered successfully.
