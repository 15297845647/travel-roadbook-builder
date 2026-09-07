from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class EndToEndTests(unittest.TestCase):
    def test_template_plan_bundle_and_validator_work_together(self) -> None:
        replacements = {
            "ROADBOOK_REVISION": "test-r1",
            "HERO_IMAGE": "hero.png",
            "TRIP_TITLE": "上海一日步行计划",
            "TRIP_DATES": "2026-10-10",
            "DURATION": "1 天",
            "TRIP_SUBTITLE": "可执行测试路书",
            "ROUTE_SUMMARY": "人民广场 → 武康路",
            "TRANSPORT_SUMMARY": "步行与地铁",
            "START_ISO": "2026-10-10T09:00:00",
            "TRIP_TIMEZONE": "Asia/Shanghai",
            "OVERVIEW_TEXT": "一份用于整包验证的上海示例。",
            "MASTER_ROUTE_ROWS": "<tr><td>D1 · 2026-10-10</td><td>无</td><td>步行</td><td>人民广场 → 武康路</td><td>8 km / 8 h</td><td>街区漫步</td><td>无</td></tr>",
            "TOTAL_DISTANCE": "8 km",
            "HOTEL_NIGHTS": "0",
            "LONGEST_DAY": "30 min",
            "MAP_CONTENT": '<p><a href="https://example.com/map">打开地图</a></p>',
            "TRANSPORT_ROWS": "<tr><td>09:00</td><td>人民广场</td><td>武康路</td></tr>",
            "DAY1_DATE": "2026-10-10",
            "DAY1_SLEEP": "返程",
            "DAY1_ROUTE": "人民广场 → 武康路",
            "DAY1_TIME_DISTANCE": "09:00–17:00 · 8 km",
            "DAY1_TIMELINE": "<p>09:00 出发</p>",
            "DAY1_CUTOFF": "16:00",
            "DAY1_PLAY_METHOD": "按街区顺序步行。",
            "DAY1_FOOD_STAY_BOOKING": "午餐预留一小时。",
            "DAY1_SKIP_FIRST": "延误时先取消咖啡休息。",
            "BOOKING_TABLE": "<tr><td>无强制预约</td></tr>",
            "STAY_CARDS": "<article class=\"card\">无需住宿</article>",
            "FOOD_CARDS": "<article class=\"card\">午餐</article>",
            "PACKING_CARDS": "<article class=\"card\">雨伞</article>",
            "RISK_CARDS": "<article class=\"card\">雨天改室内</article>",
            "BUDGET_TABLE": "<tr><td>交通</td><td>估算</td></tr>",
            "SOURCE_CHECK_DATE": "2026-09-07",
            "SOURCE_LIST": '<ul><li><a href="https://example.com/official">示例来源</a></li></ul>',
            "FOOTER_NOTE": "整包验证样例",
        }

        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            template = (ROOT / "assets" / "roadbook-template.html").read_text(encoding="utf-8")
            for key, value in replacements.items():
                template = template.replace("{{" + key + "}}", value)

            source = base / "source.html"
            bundle = base / "bundle.html"
            plan = base / "plan.json"
            source.write_text(template, encoding="utf-8")
            (base / "hero.png").write_bytes(b"\x89PNG\r\n\x1a\nfixture")
            plan.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "trip": {
                            "title": "上海一日步行计划",
                            "timezone": "Asia/Shanghai",
                            "start_date": "2026-10-10",
                            "end_date": "2026-10-10",
                            "expected_days": 1,
                            "expected_nights": 0,
                        },
                        "days": [
                            {
                                "day": 1,
                                "date": "2026-10-10",
                                "sleep_city": None,
                                "window": {"start": "09:00", "end": "17:00"},
                                "blocks": [
                                    {
                                        "start": "09:00",
                                        "end": "09:30",
                                        "kind": "travel",
                                        "label": "人民广场到武康路",
                                        "duration_basis": "estimated",
                                    }
                                ],
                            }
                        ],
                        "sources": [
                            {
                                "claim": "示例运营信息",
                                "url": "https://example.com/official",
                                "checked_on": "2026-09-07",
                                "applies_on": "2026-10-10",
                                "status": "estimated",
                            }
                        ],
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            embedded = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "embed_html_images.py"),
                    str(source),
                    str(bundle),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(embedded.returncode, 0, embedded.stderr)

            validated = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "validate_roadbook.py"),
                    "--plan",
                    str(plan),
                    "--html",
                    str(source),
                    "--bundle",
                    str(bundle),
                    "--expected-days",
                    "1",
                    "--expected-nights",
                    "0",
                    "--expected-revision",
                    "test-r1",
                    "--must-contain",
                    "上海",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

        self.assertEqual(validated.returncode, 0, validated.stdout + validated.stderr)
        self.assertTrue(json.loads(validated.stdout)["ok"])


if __name__ == "__main__":
    unittest.main()
