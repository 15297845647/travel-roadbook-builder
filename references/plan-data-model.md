# Structured trip plan

Use one structured plan for Roadbook mode, generated roadbooks, and any revision that changes several dependent days. It is the authoritative record; tables, prose, links, HTML, and PDF are derived views. Store local dates and times with an IANA timezone such as `Asia/Shanghai`.

## Minimum fields

```json
{
  "schema_version": "1.0",
  "trip": {
    "title": "示例行程",
    "timezone": "Asia/Shanghai",
    "start_date": "2026-10-10",
    "end_date": "2026-10-11",
    "expected_days": 2,
    "expected_nights": 1
  },
  "days": [
    {
      "day": 1,
      "date": "2026-10-10",
      "sleep_city": "上海",
      "window": {"start": "09:00", "end": "18:00"},
      "blocks": [
        {
          "kind": "travel",
          "start": "09:00",
          "end": "09:30",
          "label": "酒店至博物馆",
          "duration_basis": "verified"
        }
      ]
    },
    {
      "day": 2,
      "date": "2026-10-11",
      "sleep_city": null,
      "window": {"start": "09:00", "end": "17:00"},
      "blocks": []
    }
  ],
  "sources": [
    {
      "claim": "博物馆开放时间",
      "url": "https://example.org/official",
      "checked_on": "2026-09-07",
      "applies_on": "2026-10-10",
      "status": "confirmed"
    }
  ]
}
```

Add optional fields for transport alternatives, fixed departures, rental events, bookings, lodging, budget, route descriptions, and media credits. Keep them within this one plan rather than creating a second calendar.

## Invariants

- The inclusive date range equals `expected_days`; `days` has one consecutive record per date and `day` numbering begins at 1.
- The number of non-null `sleep_city` values equals `expected_nights`.
- Every block has a label, a supported kind (`visit`, `travel`, `meal`, `check-in`, `check-out`, or `buffer`), valid `HH:MM` times, positive duration, no overlap, and stays inside its daily window.
- Each travel block states whether its duration is `live`, `verified`, or `estimated`.
- Each volatile material claim records a URL, check date, applicable trip date, and status (`confirmed`, `estimated`, or `pending`).
- Rental pickup is before the first rental drive; return is after the last one. Fixed departures include transfer and check-in buffer.

## Revision rule

Change the relevant plan object first, recompute affected downstream blocks, then regenerate every dependent representation. A Markdown table, a link list, or an HTML day card is never the source of truth.

## Food and experience evidence extension

For days with restaurant recommendations, add `meals` to the existing day object. Each meal records `occasion`, `primary`, `alternatives` (1–2 when evidence allows), and any `coverage_gap`. A hotel breakfast, packed meal, or onboard meal may instead record its explicit `meal_type`; do not invent a restaurant to fill a slot.

Each restaurant candidate records name, branch, map query/location, recommended dishes, recommendation reason, route fit (preceding/following stop and walking/detour time with basis), opening status, parking, queue/cut-off, reservation, dietary fit, experience confidence, and source IDs. Unknown values are marked pending rather than guessed. Alternatives are choices, not extra scheduled stops; only the selected meal affects travel blocks and navigation.

Extend the existing `sources` entries for social experience with a stable ID, platform, note URL/ID, author when visible, publication/update date, reported visit date when available, checked date, topic/place/branch, extracted claim, visible save/comment counts (or unknown), comment observations, marketing/duplication flags, access depth (full note/comments, note only, or snippet), independence group, and experience confidence. Keep publication time distinct from visit time. Never infer unpublished counts or dates. Follow `xiaohongshu-travel-and-food.md` for grading.

Keep factual `status` (confirmed/estimated/pending) separate from experience confidence (high/medium/low). Conflicting evidence retains both source IDs and a resolution or pending action. Route revisions recompute meal fit, backups, timings, sources, and every dependent output from this same plan.

For road restrictions and weather claims, extend their existing source entries with `published_at`, `location_or_segment`, `effective_from`, `effective_until` (unknown when unpublished), `forecast_coverage` where relevant, `checked_at`, `recheck_on`, and a reference to the affected day/route and fallback. Keep these source-specific fields in the same plan; never infer a reopening date from a missing end date.
