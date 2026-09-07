from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_roadbook.py"
sys.path.insert(0, str(ROOT / "scripts"))

import validate_roadbook  # noqa: E402


def valid_plan() -> dict:
    return {
        "schema_version": "1.0",
        "trip": {
            "title": "Test trip",
            "timezone": "Asia/Shanghai",
            "start_date": "2026-10-10",
            "end_date": "2026-10-11",
            "expected_days": 2,
            "expected_nights": 1,
        },
        "days": [
            {
                "day": 1,
                "date": "2026-10-10",
                "sleep_city": "上海",
                "window": {"start": "09:00", "end": "18:00"},
                "blocks": [
                    {
                        "start": "09:00",
                        "end": "09:30",
                        "kind": "travel",
                        "label": "酒店到博物馆",
                        "duration_basis": "verified",
                    },
                    {
                        "start": "09:30",
                        "end": "11:30",
                        "kind": "visit",
                        "label": "博物馆",
                    },
                ],
            },
            {
                "day": 2,
                "date": "2026-10-11",
                "sleep_city": None,
                "window": {"start": "09:00", "end": "17:00"},
                "blocks": [],
            },
        ],
        "sources": [
            {
                "claim": "博物馆营业时间",
                "url": "https://example.com/official",
                "checked_on": "2026-09-07",
                "applies_on": "2026-10-10",
                "status": "confirmed",
            }
        ],
    }


class PlanValidationTests(unittest.TestCase):
    def run_validator(self, plan: dict) -> tuple[int, dict]:
        with tempfile.TemporaryDirectory() as directory:
            plan_path = Path(directory) / "plan.json"
            plan_path.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, str(SCRIPT), "--plan", str(plan_path)],
                check=False,
                capture_output=True,
                text=True,
            )
            payload = json.loads(completed.stdout) if completed.stdout.strip().startswith("{") else {}
            return completed.returncode, payload

    def test_accepts_consistent_plan_without_html(self) -> None:
        returncode, payload = self.run_validator(valid_plan())
        self.assertEqual(returncode, 0, payload)
        self.assertTrue(payload["ok"])

    def test_rejects_overlapping_time_blocks(self) -> None:
        plan = copy.deepcopy(valid_plan())
        plan["days"][0]["blocks"][1]["start"] = "09:20"

        returncode, payload = self.run_validator(plan)

        self.assertEqual(returncode, 1)
        self.assertTrue(any("overlap" in error.lower() for error in payload["errors"]))

    def test_rejects_hotel_night_mismatch(self) -> None:
        plan = copy.deepcopy(valid_plan())
        plan["trip"]["expected_nights"] = 2

        returncode, payload = self.run_validator(plan)

        self.assertEqual(returncode, 1)
        self.assertTrue(any("night" in error.lower() for error in payload["errors"]))

    def test_rejects_unknown_duration_basis(self) -> None:
        plan = copy.deepcopy(valid_plan())
        plan["days"][0]["blocks"][0]["duration_basis"] = "guessed"

        returncode, payload = self.run_validator(plan)

        self.assertEqual(returncode, 1)
        self.assertTrue(any("duration_basis" in error for error in payload["errors"]))

    def test_rejects_unknown_source_status(self) -> None:
        plan = copy.deepcopy(valid_plan())
        plan["sources"][0]["status"] = "fresh"

        returncode, payload = self.run_validator(plan)

        self.assertEqual(returncode, 1)
        self.assertTrue(any("status" in error for error in payload["errors"]))

    def test_rejects_non_iana_timezone(self) -> None:
        plan = copy.deepcopy(valid_plan())
        plan["trip"]["timezone"] = "Shanghai"

        returncode, payload = self.run_validator(plan)

        self.assertEqual(returncode, 1)
        self.assertTrue(any("timezone" in error for error in payload["errors"]))

    def test_bundle_rejects_local_css_and_srcset_assets(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            bundle = Path(directory) / "bundle.html"
            bundle.write_text(
                '<style>.hero{background:url("hero.png")}</style>'
                '<picture><source srcset="small.png 1x, large.png 2x"></picture>',
                encoding="utf-8",
            )
            completed = subprocess.run(
                [sys.executable, str(SCRIPT), "--bundle", str(bundle)],
                check=False,
                capture_output=True,
                text=True,
            )
            payload = json.loads(completed.stdout)

        self.assertEqual(completed.returncode, 1)
        joined = "\n".join(payload["errors"])
        self.assertIn("hero.png", joined)
        self.assertIn("small.png", joined)
        self.assertIn("large.png", joined)

    def test_bundle_rejects_existing_local_script_and_stylesheet(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            (base / "app.js").write_text("console.log('x')", encoding="utf-8")
            (base / "style.css").write_text("body{}", encoding="utf-8")
            bundle = base / "bundle.html"
            bundle.write_text(
                '<link rel="stylesheet" href="style.css"><script src="app.js"></script>',
                encoding="utf-8",
            )
            completed = subprocess.run(
                [sys.executable, str(SCRIPT), "--bundle", str(bundle)],
                check=False,
                capture_output=True,
                text=True,
            )
            payload = json.loads(completed.stdout)

        self.assertEqual(completed.returncode, 1)
        joined = "\n".join(payload["errors"])
        self.assertIn("style.css", joined)
        self.assertIn("app.js", joined)

    def test_rejects_invalid_sleep_city_block_kind_and_missing_label(self) -> None:
        plan = copy.deepcopy(valid_plan())
        plan["days"][0]["sleep_city"] = 42
        plan["days"][0]["blocks"][1].pop("label")
        plan["days"][0]["blocks"][1]["kind"] = "teleport"

        returncode, payload = self.run_validator(plan)

        self.assertEqual(returncode, 1)
        joined = "\n".join(payload["errors"])
        self.assertIn("sleep_city", joined)
        self.assertIn("label", joined)
        self.assertIn("kind", joined)

    def test_accepts_checkout_block_kind(self) -> None:
        plan = copy.deepcopy(valid_plan())
        plan["days"][1]["blocks"] = [
            {
                "start": "09:00",
                "end": "09:20",
                "kind": "check-out",
                "label": "退房并取行李",
            }
        ]

        returncode, payload = self.run_validator(plan)

        self.assertEqual(returncode, 0, payload)

    def test_source_requires_applicable_trip_date(self) -> None:
        plan = copy.deepcopy(valid_plan())
        plan["sources"][0].pop("applies_on")

        returncode, payload = self.run_validator(plan)

        self.assertEqual(returncode, 1)
        self.assertTrue(any("applies_on" in error for error in payload["errors"]))

    def test_bundle_only_honors_content_assertions(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            bundle = Path(directory) / "bundle.html"
            bundle.write_text("<p>stale city</p>", encoding="utf-8")
            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--bundle",
                    str(bundle),
                    "--must-contain",
                    "required city",
                    "--forbid",
                    "stale city",
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            payload = json.loads(completed.stdout)

        self.assertEqual(completed.returncode, 1)
        self.assertEqual(2, len([error for error in payload["errors"] if "token" in error]))

    def test_pdf_honors_required_and_forbidden_content_assertions(self) -> None:
        class FakePage:
            def extract_text(self) -> str:
                return "old city " * 30

        class FakeReader:
            is_encrypted = False
            pages = [FakePage()]

        errors: list[str] = []
        warnings: list[str] = []
        fake_module = SimpleNamespace(PdfReader=lambda _: FakeReader())
        with mock.patch.dict(sys.modules, {"pypdf": fake_module}):
            validate_roadbook.check_pdf(
                Path("guide.pdf"),
                ["required city"],
                ["old city"],
                errors,
                warnings,
                strict_pdf_text=True,
            )

        self.assertTrue(any("required token" in error for error in errors))
        self.assertTrue(any("forbidden stale token" in error for error in errors))

    def test_bundle_rejects_local_anchor_links(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            bundle = Path(directory) / "bundle.html"
            bundle.write_text(
                '<div id="overview"></div><a href="#overview">内部锚点</a>'
                '<a href="guide.pdf">相对文件</a>'
                '<a href="file:///Users/example/private.pdf">本地文件</a>',
                encoding="utf-8",
            )
            completed = subprocess.run(
                [sys.executable, str(SCRIPT), "--bundle", str(bundle)],
                check=False,
                capture_output=True,
                text=True,
            )
            payload = json.loads(completed.stdout)

        self.assertEqual(completed.returncode, 1)
        joined = "\n".join(payload["errors"])
        self.assertIn("guide.pdf", joined)
        self.assertIn("file:///Users/example/private.pdf", joined)
        self.assertNotIn("#overview", joined)

    def test_html_rejects_assets_outside_trusted_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base = root / "trip"
            base.mkdir()
            secret = root / "secret.png"
            secret.write_bytes(b"private")
            (base / "leak.png").symlink_to(secret)

            for reference in ("../secret.png", str(secret), "leak.png"):
                with self.subTest(reference=reference):
                    source = base / "source.html"
                    source.write_text(f'<img src="{reference}" alt="bad">', encoding="utf-8")
                    completed = subprocess.run(
                        [sys.executable, str(SCRIPT), "--html", str(source)],
                        check=False,
                        capture_output=True,
                        text=True,
                    )
                    payload = json.loads(completed.stdout)
                    self.assertEqual(completed.returncode, 1, payload)
                    self.assertTrue(
                        any("outside trusted asset directory" in error for error in payload["errors"])
                    )

    def test_legacy_html_night_count_uses_data_sleep(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source.html"
            source.write_text(
                '<details data-day="D1" data-sleep="上海"></details>'
                '<details data-day="D2" data-sleep="返程"></details>',
                encoding="utf-8",
            )
            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--html",
                    str(source),
                    "--expected-nights",
                    "1",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

        payload = json.loads(completed.stdout)
        self.assertEqual(completed.returncode, 0, payload)
        self.assertTrue(payload["ok"])

    def test_html_rejects_nonconsecutive_day_values(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source.html"
            source.write_text(
                '<details data-day="D1" data-sleep="上海"></details>'
                '<details data-day="D3" data-sleep="返程"></details>',
                encoding="utf-8",
            )
            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--html",
                    str(source),
                    "--expected-days",
                    "2",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

        payload = json.loads(completed.stdout)
        self.assertEqual(completed.returncode, 1, payload)
        self.assertTrue(any("data-day sequence" in error for error in payload["errors"]))

    def test_legacy_revision_checks_expected_value_and_bundle_equality(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            source = base / "source.html"
            bundle = base / "bundle.html"
            source.write_text(
                '<html data-roadbook-revision="r2"><meta name="roadbook-revision" content="r2"></html>',
                encoding="utf-8",
            )
            bundle.write_text(
                '<html data-roadbook-revision="r3"><meta name="roadbook-revision" content="r3"></html>',
                encoding="utf-8",
            )
            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--html",
                    str(source),
                    "--bundle",
                    str(bundle),
                    "--expected-revision",
                    "r2",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

        payload = json.loads(completed.stdout)
        self.assertEqual(completed.returncode, 1, payload)
        self.assertTrue(any("expected roadbook revision 'r2'" in error for error in payload["errors"]))
        self.assertTrue(any("source/bundle roadbook revisions differ" in error for error in payload["errors"]))

    def test_legacy_strict_pdf_text_escalates_missing_tokens(self) -> None:
        class FakePage:
            def extract_text(self) -> str:
                return "available text " * 20

        class FakeReader:
            is_encrypted = False
            pages = [FakePage()]

        fake_module = SimpleNamespace(PdfReader=lambda _: FakeReader())
        warnings: list[str] = []
        errors: list[str] = []
        with mock.patch.dict(sys.modules, {"pypdf": fake_module}):
            validate_roadbook.check_pdf(
                Path("guide.pdf"), ["missing"], [], errors, warnings, strict_pdf_text=False
            )
        self.assertFalse(errors)
        self.assertTrue(any("required token" in warning for warning in warnings))

        warnings = []
        errors = []
        with mock.patch.dict(sys.modules, {"pypdf": fake_module}):
            validate_roadbook.check_pdf(
                Path("guide.pdf"), ["missing"], [], errors, warnings, strict_pdf_text=True
            )
        self.assertTrue(any("required token" in error for error in errors))
        self.assertFalse(warnings)


if __name__ == "__main__":
    unittest.main()
