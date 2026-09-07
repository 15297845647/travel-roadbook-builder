from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "embed_html_images.py"


class EmbedHtmlAssetsTests(unittest.TestCase):
    def test_embeds_css_background_and_srcset_images(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            (base / "hero.png").write_bytes(b"\x89PNG\r\n\x1a\nhero")
            (base / "small.png").write_bytes(b"\x89PNG\r\n\x1a\nsmall")
            source = base / "source.html"
            output = base / "bundle.html"
            source.write_text(
                '<style>.hero{background-image:url("hero.png")}</style>'
                '<picture><source srcset="small.png 1x, hero.png 2x">'
                '<img src="small.png" alt="示例"></picture>',
                encoding="utf-8",
            )

            completed = subprocess.run(
                [sys.executable, str(SCRIPT), str(source), str(output)],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            bundled = output.read_text(encoding="utf-8")
            self.assertIn('background-image:url("data:image/png;base64,', bundled)
            self.assertIn('srcset="data:image/png;base64,', bundled)
            self.assertNotIn('url("hero.png")', bundled)
            self.assertNotIn('srcset="small.png', bundled)

    def test_rejects_unsupported_local_script_stylesheet_and_css_import(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            (base / "app.js").write_text("console.log('x')", encoding="utf-8")
            (base / "style.css").write_text("body{}", encoding="utf-8")
            (base / "extra.css").write_text("p{}", encoding="utf-8")
            source = base / "source.html"
            output = base / "bundle.html"
            source.write_text(
                '<link rel="stylesheet" href="style.css">'
                '<style>@import "extra.css";</style>'
                '<script src="app.js"></script>',
                encoding="utf-8",
            )

            completed = subprocess.run(
                [sys.executable, str(SCRIPT), str(source), str(output)],
                check=False,
                capture_output=True,
                text=True,
            )

        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("style.css", completed.stderr)
        self.assertIn("extra.css", completed.stderr)
        self.assertIn("app.js", completed.stderr)

    def test_rejects_parent_directory_asset_escape(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base = root / "trip"
            base.mkdir()
            (root / "secret.txt").write_text("private", encoding="utf-8")
            source = base / "source.html"
            output = base / "bundle.html"
            source.write_text('<img src="../secret.txt" alt="bad">', encoding="utf-8")

            completed = subprocess.run(
                [sys.executable, str(SCRIPT), str(source), str(output)],
                check=False,
                capture_output=True,
                text=True,
            )

        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("outside trusted base directory", completed.stderr)

    def test_rejects_absolute_asset_outside_base_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base = root / "trip"
            base.mkdir()
            secret = root / "secret.txt"
            secret.write_text("private", encoding="utf-8")
            source = base / "source.html"
            output = base / "bundle.html"
            source.write_text(f'<img src="{secret}" alt="bad">', encoding="utf-8")

            completed = subprocess.run(
                [sys.executable, str(SCRIPT), str(source), str(output)],
                check=False,
                capture_output=True,
                text=True,
            )

        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("outside trusted base directory", completed.stderr)

    def test_rejects_symlink_asset_escape(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base = root / "trip"
            base.mkdir()
            secret = root / "secret.txt"
            secret.write_text("private", encoding="utf-8")
            (base / "leak.txt").symlink_to(secret)
            source = base / "source.html"
            output = base / "bundle.html"
            source.write_text('<img src="leak.txt" alt="bad">', encoding="utf-8")

            completed = subprocess.run(
                [sys.executable, str(SCRIPT), str(source), str(output)],
                check=False,
                capture_output=True,
                text=True,
            )

        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("outside trusted base directory", completed.stderr)


if __name__ == "__main__":
    unittest.main()
