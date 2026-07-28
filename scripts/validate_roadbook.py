#!/usr/bin/env python3
"""Validate common consistency and portability requirements for a travel roadbook."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse


PLACEHOLDER_RE = re.compile(r"\{\{[^{}]+\}\}")


class RoadbookParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.img_sources: list[str] = []
        self.day_values: list[str] = []
        self.anchor_targets: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.append(values["id"] or "")
        if tag == "img" and values.get("src"):
            self.img_sources.append(values["src"] or "")
        if values.get("data-day"):
            self.day_values.append(values["data-day"] or "")
        if tag == "a" and (values.get("href") or "").startswith("#"):
            self.anchor_targets.append((values.get("href") or "")[1:])


def parse_html(path: Path) -> tuple[str, RoadbookParser]:
    text = path.read_text(encoding="utf-8")
    parser = RoadbookParser()
    parser.feed(text)
    return text, parser


def is_local_asset(src: str) -> bool:
    parsed = urlparse(src)
    return bool(src) and not (
        parsed.scheme in {"http", "https", "data", "blob", "mailto", "tel"}
        or src.startswith("//")
        or src.startswith("#")
    )


def local_asset_path(src: str, base_dir: Path) -> Path:
    clean = unquote(urlparse(src).path)
    path = Path(clean)
    return path if path.is_absolute() else (base_dir / path).resolve()


def check_html(path: Path, expected_days: int | None, errors: list[str], warnings: list[str]) -> tuple[str, RoadbookParser]:
    text, parser = parse_html(path)
    duplicates = sorted(key for key, count in Counter(parser.ids).items() if count > 1)
    if duplicates:
        errors.append(f"{path.name}: duplicate HTML id(s): {', '.join(duplicates)}")

    missing_targets = sorted(target for target in parser.anchor_targets if target and target not in parser.ids)
    if missing_targets:
        errors.append(f"{path.name}: unresolved anchor target(s): {', '.join(missing_targets)}")

    placeholders = sorted(set(PLACEHOLDER_RE.findall(text)))
    if placeholders:
        errors.append(f"{path.name}: unresolved placeholder(s): {', '.join(placeholders[:10])}")

    missing_assets = [
        f"{src} -> {local_asset_path(src, path.parent)}"
        for src in parser.img_sources
        if is_local_asset(src) and not local_asset_path(src, path.parent).is_file()
    ]
    if missing_assets:
        errors.append(f"{path.name}: missing image asset(s): {'; '.join(missing_assets)}")

    unique_days = set(parser.day_values)
    if expected_days is not None and len(unique_days) != expected_days:
        errors.append(
            f"{path.name}: expected {expected_days} unique data-day values, found {len(unique_days)}"
        )
    if not parser.day_values:
        warnings.append(f"{path.name}: no data-day attributes found; day-count check is unavailable")
    return text, parser


def check_bundle(path: Path, errors: list[str]) -> None:
    _, parser = parse_html(path)
    local = [src for src in parser.img_sources if is_local_asset(src)]
    if local:
        errors.append(f"{path.name}: shareable bundle still has local image src(s): {', '.join(local[:10])}")


def check_pdf(path: Path, must_contain: list[str], errors: list[str], warnings: list[str]) -> None:
    try:
        from pypdf import PdfReader
    except ImportError:
        warnings.append("pypdf is unavailable; skipped PDF structure and text checks")
        return

    try:
        reader = PdfReader(str(path))
    except Exception as exc:
        errors.append(f"{path.name}: cannot open PDF: {exc}")
        return
    if reader.is_encrypted:
        errors.append(f"{path.name}: PDF is encrypted")
        return
    if not reader.pages:
        errors.append(f"{path.name}: PDF has zero pages")
        return
    extracted = "\n".join((page.extract_text() or "") for page in reader.pages)
    if len(extracted.strip()) < 100:
        warnings.append(f"{path.name}: extracted PDF text is unusually short")
    for token in must_contain:
        if token not in extracted:
            warnings.append(f"{path.name}: PDF text does not contain required token: {token!r}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--html", type=Path, required=True, help="Editable/source HTML")
    parser.add_argument("--bundle", type=Path, help="Shareable single-file HTML")
    parser.add_argument("--pdf", type=Path, help="Rendered PDF")
    parser.add_argument("--expected-days", type=int)
    parser.add_argument("--must-contain", action="append", default=[])
    parser.add_argument("--forbid", action="append", default=[])
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []
    html = args.html.resolve()
    if not html.is_file():
        errors.append(f"Source HTML not found: {html}")
        text = ""
    else:
        text, _ = check_html(html, args.expected_days, errors, warnings)

    for token in args.must_contain:
        if token not in text:
            errors.append(f"{html.name}: required token not found: {token!r}")
    for token in args.forbid:
        if token in text:
            errors.append(f"{html.name}: forbidden stale token found: {token!r}")

    if args.bundle:
        bundle = args.bundle.resolve()
        if not bundle.is_file():
            errors.append(f"Shareable bundle not found: {bundle}")
        else:
            check_html(bundle, args.expected_days, errors, warnings)
            check_bundle(bundle, errors)

    if args.pdf:
        pdf = args.pdf.resolve()
        if not pdf.is_file():
            errors.append(f"PDF not found: {pdf}")
        else:
            check_pdf(pdf, args.must_contain, errors, warnings)

    result = {"ok": not errors, "errors": errors, "warnings": warnings}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
