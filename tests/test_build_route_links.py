from __future__ import annotations

import sys
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlparse


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_route_links  # noqa: E402


class RouteLinkTests(unittest.TestCase):
    def test_international_route_chunks_for_mobile_waypoint_limit(self) -> None:
        stops = [f"Stop {number}, Kyoto" for number in range(1, 8)]

        bundle = build_route_links.build_route_bundle(
            stops=stops,
            region="international",
            mode="walking",
            city="Kyoto",
        )

        routes = [link for link in bundle["links"] if link["kind"] == "directions"]
        self.assertEqual([link["provider"] for link in routes], ["google", "google"])
        self.assertEqual(routes[0]["from"], stops[0])
        self.assertEqual(routes[0]["to"], stops[4])
        self.assertEqual(routes[1]["from"], stops[4])
        self.assertEqual(routes[1]["to"], stops[6])

        first_query = parse_qs(urlparse(routes[0]["url"]).query)
        self.assertEqual(first_query["waypoints"][0].split("|"), stops[1:4])

    def test_china_route_covers_every_leg_and_adds_amap_searches(self) -> None:
        stops = ["人民广场", "A&B 咖啡", "武康路"]

        bundle = build_route_links.build_route_bundle(
            stops=stops,
            region="china",
            mode="transit",
            city="上海",
        )

        routes = [link for link in bundle["links"] if link["kind"] == "directions"]
        searches = [link for link in bundle["links"] if link["kind"] == "search"]
        self.assertEqual(len(routes), 2)
        self.assertEqual(len(searches), 3)
        self.assertTrue(all(link["provider"] == "baidu" for link in routes))
        self.assertTrue(all(link["provider"] == "amap" for link in searches))
        self.assertEqual([(link["from"], link["to"]) for link in routes], list(zip(stops, stops[1:])))
        self.assertNotIn("&B ", searches[1]["url"])

        amap_url = urlparse(searches[1]["url"])
        amap_query = parse_qs(amap_url.query)
        self.assertEqual(amap_url.netloc, "uri.amap.com")
        self.assertEqual(amap_url.path, "/search")
        self.assertEqual(amap_query["keyword"], [stops[1]])
        self.assertNotIn("query", amap_query)

        baidu_query = parse_qs(urlparse(routes[0]["url"]).query)
        self.assertEqual(baidu_query["src"], ["webapp.openai.travelroadbook"])
        self.assertEqual(baidu_query["output"], ["html"])

    def test_region_is_explicit(self) -> None:
        with self.assertRaisesRegex(ValueError, "region"):
            build_route_links.build_route_bundle(
                stops=["A", "B"],
                region="auto",
                mode="walking",
                city="Test",
            )

    def test_rejects_unsupported_mode(self) -> None:
        with self.assertRaisesRegex(ValueError, "mode"):
            build_route_links.build_route_bundle(
                stops=["A", "B"],
                region="international",
                mode="hovercraft",
                city="Test",
            )

    def test_china_requires_city_and_maps_bicycle_mode(self) -> None:
        with self.assertRaisesRegex(ValueError, "city"):
            build_route_links.build_route_bundle(
                stops=["人民广场", "武康路"],
                region="china",
                mode="walking",
                city="",
            )

        bundle = build_route_links.build_route_bundle(
            stops=["人民广场", "武康路"],
            region="china",
            mode="bicycling",
            city="上海",
        )
        route = next(link for link in bundle["links"] if link["kind"] == "directions")
        self.assertEqual(parse_qs(urlparse(route["url"]).query)["mode"], ["riding"])

    def test_route_requires_two_stops(self) -> None:
        with self.assertRaisesRegex(ValueError, "at least two"):
            build_route_links.build_route_bundle(
                stops=["Only stop"],
                region="international",
                mode="walking",
                city="Test",
            )


if __name__ == "__main__":
    unittest.main()
