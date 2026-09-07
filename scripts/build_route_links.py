#!/usr/bin/env python3
"""Build shareable map links from named stops.

The links delegate route calculation to the map provider.  This module only
formats URLs; it does not calculate routes, distances, or arrival times.
"""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from typing import Any
from urllib.parse import urlencode


GOOGLE_DIRECTIONS_URL = "https://www.google.com/maps/dir/"
BAIDU_DIRECTIONS_URL = "https://api.map.baidu.com/direction"
AMAP_SEARCH_URL = "https://uri.amap.com/search"
_VALID_REGIONS = frozenset({"china", "international"})
_VALID_MODES = frozenset({"bicycling", "driving", "transit", "walking"})
_BAIDU_MODE = {
    "bicycling": "riding",
    "driving": "driving",
    "transit": "transit",
    "walking": "walking",
}
_GOOGLE_MAX_STOPS = 5


def _query_url(base: str, params: dict[str, str]) -> str:
    """Return *base* with query values safely encoded."""
    return f"{base}?{urlencode(params)}"


def _normalise_stops(stops: Sequence[str]) -> list[str]:
    """Return a validated, JSON-friendly copy of the supplied stop names."""
    if isinstance(stops, (str, bytes)):
        raise TypeError("stops must be a sequence of stop names, not a string")

    result = list(stops)
    if not all(isinstance(stop, str) and stop.strip() for stop in result):
        raise ValueError("every stop must be a non-empty string")
    return [stop.strip() for stop in result]


def _google_route_url(chunk: list[str], mode: str) -> str:
    params = {
        "api": "1",
        "origin": chunk[0],
        "destination": chunk[-1],
        "travelmode": mode,
    }
    if len(chunk) > 2:
        params["waypoints"] = "|".join(chunk[1:-1])
    return _query_url(GOOGLE_DIRECTIONS_URL, params)


def _google_direction_links(stops: list[str], mode: str) -> list[dict[str, Any]]:
    """Split a route into overlapping, five-stop Google Maps chunks."""
    links: list[dict[str, Any]] = []
    start = 0
    while start < len(stops) - 1:
        chunk = stops[start : start + _GOOGLE_MAX_STOPS]
        links.append(
            {
                "kind": "directions",
                "provider": "google",
                "from": chunk[0],
                "to": chunk[-1],
                "stops": chunk,
                "url": _google_route_url(chunk, mode),
            }
        )
        if start + len(chunk) == len(stops):
            break
        start += _GOOGLE_MAX_STOPS - 1
    return links


def _baidu_direction_links(
    stops: list[str], mode: str, city: str
) -> list[dict[str, Any]]:
    """Create a named-place Baidu directions link for each adjacent pair."""
    return [
        {
            "kind": "directions",
            "provider": "baidu",
            "from": origin,
            "to": destination,
            "url": _query_url(
                BAIDU_DIRECTIONS_URL,
                {
                    "origin": origin,
                    "destination": destination,
                    "mode": _BAIDU_MODE[mode],
                    "region": city,
                    "output": "html",
                    "src": "webapp.openai.travelroadbook",
                },
            ),
        }
        for origin, destination in zip(stops, stops[1:])
    ]


def _amap_search_links(stops: list[str], city: str) -> list[dict[str, Any]]:
    """Create an Amap keyword-search link for each named stop."""
    return [
        {
            "kind": "search",
            "provider": "amap",
            "stop": stop,
            "url": _query_url(
                AMAP_SEARCH_URL,
                {"keyword": stop, "city": city, "view": "map", "src": "travel-roadbook-builder"},
            ),
        }
        for stop in stops
    ]


def build_route_bundle(
    *, stops: Sequence[str], region: str, mode: str, city: str
) -> dict[str, Any]:
    """Return JSON-serialisable provider links for an explicit geographic region.

    ``region`` must be either ``"china"`` (Baidu per-leg links plus Amap
    searches) or ``"international"`` (overlapping Google Maps route chunks).
    """
    if region not in _VALID_REGIONS:
        raise ValueError("region must be either 'china' or 'international'")
    if mode not in _VALID_MODES:
        raise ValueError(f"mode must be one of: {', '.join(sorted(_VALID_MODES))}")
    if not isinstance(city, str):
        raise TypeError("city must be a string")
    city = city.strip()
    if region == "china" and not city:
        raise ValueError("city is required for China map links")

    names = _normalise_stops(stops)
    if len(names) < 2:
        raise ValueError("at least two stops are required to build a route")
    links = (
        _baidu_direction_links(names, mode, city) + _amap_search_links(names, city)
        if region == "china"
        else _google_direction_links(names, mode)
    )
    return {
        "region": region,
        "mode": mode,
        "city": city,
        "stops": names,
        "links": links,
    }


def _text_output(bundle: dict[str, Any]) -> str:
    lines = [f"{bundle['region']} map links"]
    for link in bundle["links"]:
        if link["kind"] == "directions":
            lines.append(f"{link['provider']}: {link['from']} -> {link['to']}\n  {link['url']}")
        else:
            lines.append(f"{link['provider']}: {link['stop']}\n  {link['url']}")
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build provider map links from named stops.")
    parser.add_argument("--region", choices=sorted(_VALID_REGIONS), required=True)
    parser.add_argument("--mode", default="walking")
    parser.add_argument("--city", default="")
    parser.add_argument("--stops", nargs="+", required=True, metavar="STOP")
    parser.add_argument("--text", action="store_true", help="print readable text instead of JSON")
    args = parser.parse_args(argv)

    bundle = build_route_bundle(
        stops=args.stops, region=args.region, mode=args.mode, city=args.city
    )
    print(_text_output(bundle) if args.text else json.dumps(bundle, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
