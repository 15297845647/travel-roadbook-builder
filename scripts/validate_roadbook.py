#!/usr/bin/env python3
"""Validate common consistency and portability requirements for a travel roadbook."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from datetime import date, timedelta
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


PLACEHOLDER_RE = re.compile(r"\{\{[^{}]+\}\}")
ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
TIME_RE = re.compile(r"^(?:[01]\d|2[0-3]):[0-5]\d$")
CSS_URL_RE = re.compile(
    r"url\(\s*(?:['\"](?P<quoted>.*?)['\"]|(?P<bare>[^)\s][^)]*?))\s*\)",
    re.IGNORECASE | re.DOTALL,
)
CSS_IMPORT_RE = re.compile(
    r"@import\s+(?:url\(\s*(?:['\"](?P<url_quoted>.*?)['\"]|(?P<url_bare>[^)\s][^)]*?))\s*\)|['\"](?P<quoted>.*?)['\"])",
    re.IGNORECASE | re.DOTALL,
)
SRCSET_CANDIDATE_RE = re.compile(
    r"(?P<url>data:\S+|[^\s,]+)(?P<descriptor>(?:\s+[^,]+)?)",
    re.IGNORECASE,
)
NO_SLEEP_VALUES = frozenset({"", "none", "home", "no", "无", "不住宿", "返程"})
VALID_DURATION_BASES = frozenset({"live", "verified", "estimated"})
VALID_SOURCE_STATUSES = frozenset({"confirmed", "estimated", "pending"})
VALID_BLOCK_KINDS = frozenset({"buffer", "check-in", "check-out", "meal", "travel", "visit"})
RESOURCE_ATTRS = {
    "audio": ("src",),
    "embed": ("src",),
    "iframe": ("src",),
    "img": ("src",),
    "input": ("src",),
    "link": ("href",),
    "object": ("data",),
    "script": ("src",),
    "source": ("src",),
    "track": ("src",),
    "video": ("src", "poster"),
}


class RoadbookParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.img_sources: list[str] = []
        self.srcset_values: list[str] = []
        self.resource_sources: list[str] = []
        self.day_values: list[str] = []
        self.day_sleeps: list[tuple[str, str | None]] = []
        self.anchor_targets: list[str] = []
        self.link_hrefs: list[str] = []
        self.revisions: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.append(values["id"] or "")
        if tag == "img" and values.get("src"):
            self.img_sources.append(values["src"] or "")
        for attribute in RESOURCE_ATTRS.get(tag, ()):
            if values.get(attribute):
                self.resource_sources.append(values[attribute] or "")
        if values.get("srcset"):
            self.srcset_values.append(values["srcset"] or "")
        if values.get("data-day"):
            day = values["data-day"] or ""
            self.day_values.append(day)
            self.day_sleeps.append((day, values.get("data-sleep")))
        if tag == "a" and values.get("href"):
            href = values.get("href") or ""
            self.link_hrefs.append(href)
            if href.startswith("#"):
                self.anchor_targets.append(href[1:])
        if tag == "html" and values.get("data-roadbook-revision"):
            self.revisions.append(values["data-roadbook-revision"] or "")
        if (
            tag == "meta"
            and (values.get("name") or "").lower() == "roadbook-revision"
            and values.get("content")
        ):
            self.revisions.append(values["content"] or "")


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
    trusted_root = base_dir.resolve()
    resolved = path.resolve() if path.is_absolute() else (trusted_root / path).resolve()
    try:
        resolved.relative_to(trusted_root)
    except ValueError as exc:
        raise ValueError(
            f"asset is outside trusted asset directory: {src} -> {resolved}"
        ) from exc
    return resolved


def asset_sources(text: str, parser: RoadbookParser) -> list[str]:
    """Return image, srcset, and inline-CSS asset URLs in document order."""
    sources = list(parser.resource_sources)
    for srcset in parser.srcset_values:
        sources.extend(
            match.group("url").strip()
            for match in SRCSET_CANDIDATE_RE.finditer(srcset)
        )
    for match in CSS_URL_RE.finditer(text):
        sources.append((match.group("quoted") or match.group("bare") or "").strip())
    for match in CSS_IMPORT_RE.finditer(text):
        sources.append(
            next(
                group
                for group in (
                    match.group("url_quoted"),
                    match.group("url_bare"),
                    match.group("quoted"),
                )
                if group is not None
            ).strip()
        )
    return list(dict.fromkeys(sources))


def check_html(
    path: Path,
    expected_days: int | None,
    expected_nights: int | None,
    expected_revision: str | None,
    errors: list[str],
    warnings: list[str],
) -> tuple[str, RoadbookParser]:
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

    missing_assets: list[str] = []
    for src in asset_sources(text, parser):
        if not is_local_asset(src):
            continue
        try:
            asset_path = local_asset_path(src, path.parent)
        except ValueError as exc:
            errors.append(f"{path.name}: {exc}")
            continue
        if not asset_path.is_file():
            missing_assets.append(f"{src} -> {asset_path}")
    if missing_assets:
        errors.append(f"{path.name}: missing local asset(s): {'; '.join(missing_assets)}")

    unique_days = set(parser.day_values)
    if expected_days is not None and len(unique_days) != expected_days:
        errors.append(
            f"{path.name}: expected {expected_days} unique data-day values, found {len(unique_days)}"
        )
    if expected_days is not None:
        expected_sequence = [f"D{number}" for number in range(1, expected_days + 1)]
        if parser.day_values != expected_sequence:
            errors.append(
                f"{path.name}: expected data-day sequence {expected_sequence!r}, "
                f"found {parser.day_values!r}"
            )
    if not parser.day_values:
        warnings.append(f"{path.name}: no data-day attributes found; day-count check is unavailable")

    if expected_nights is not None:
        if len(parser.day_sleeps) != len(parser.day_values) or any(
            sleep is None for _, sleep in parser.day_sleeps
        ):
            errors.append(f"{path.name}: every data-day element must define data-sleep")
        else:
            nights = sum(
                1
                for _, sleep in parser.day_sleeps
                if (sleep or "").strip().lower() not in NO_SLEEP_VALUES
            )
            if nights != expected_nights:
                errors.append(
                    f"{path.name}: expected {expected_nights} hotel nights from data-sleep, found {nights}"
                )

    revisions = {value for value in parser.revisions if value}
    if len(revisions) > 1:
        errors.append(f"{path.name}: conflicting roadbook revision values: {sorted(revisions)!r}")
    if expected_revision is not None and revisions != {expected_revision}:
        errors.append(
            f"{path.name}: expected roadbook revision {expected_revision!r}, found {sorted(revisions)!r}"
        )
    return text, parser


def check_bundle(path: Path, errors: list[str]) -> None:
    text, parser = parse_html(path)
    local = [src for src in asset_sources(text, parser) if is_local_asset(src)]
    if local:
        errors.append(f"{path.name}: shareable bundle still has local asset URL(s): {', '.join(local[:10])}")
    local_links = [href for href in parser.link_hrefs if is_local_asset(href)]
    if local_links:
        errors.append(
            f"{path.name}: shareable bundle still has local anchor URL(s): {', '.join(local_links[:10])}"
        )


def check_text_tokens(
    path: Path,
    contents: str,
    must_contain: list[str],
    forbid: list[str],
    errors: list[str],
) -> None:
    for token in must_contain:
        if token not in contents:
            errors.append(f"{path.name}: required token not found: {token!r}")
    for token in forbid:
        if token in contents:
            errors.append(f"{path.name}: forbidden stale token found: {token!r}")


def check_pdf(
    path: Path,
    must_contain: list[str],
    forbid: list[str],
    errors: list[str],
    warnings: list[str],
    *,
    strict_pdf_text: bool = False,
) -> None:
    try:
        from pypdf import PdfReader
    except ImportError:
        message = "pypdf is unavailable; skipped PDF structure and text checks"
        (errors if strict_pdf_text else warnings).append(message)
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
        message = f"{path.name}: extracted PDF text is unusually short"
        (errors if strict_pdf_text else warnings).append(message)
    for token in must_contain:
        if token not in extracted:
            message = f"{path.name}: PDF text does not contain required token: {token!r}"
            (errors if strict_pdf_text else warnings).append(message)
    for token in forbid:
        if token in extracted:
            errors.append(f"{path.name}: PDF contains forbidden stale token: {token!r}")


def parse_iso_date(value: object, label: str, errors: list[str]) -> date | None:
    if not isinstance(value, str) or not ISO_DATE_RE.fullmatch(value):
        errors.append(f"{label}: expected an ISO date (YYYY-MM-DD)")
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        errors.append(f"{label}: invalid ISO date: {value!r}")
        return None


def parse_time(value: object, label: str, errors: list[str]) -> int | None:
    if not isinstance(value, str) or not TIME_RE.fullmatch(value):
        errors.append(f"{label}: expected a time in HH:MM format")
        return None
    hours, minutes = value.split(":")
    return int(hours) * 60 + int(minutes)


def require_mapping(value: object, label: str, errors: list[str]) -> dict[str, object] | None:
    if not isinstance(value, dict):
        errors.append(f"{label}: expected an object")
        return None
    return value


def require_non_empty_string(value: object, label: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{label}: expected a non-empty string")


def check_timezone(value: object, label: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{label}: expected a non-empty IANA timezone")
        return
    try:
        ZoneInfo(value)
    except (ZoneInfoNotFoundError, ValueError):
        errors.append(f"{label}: unknown IANA timezone: {value!r}")


def require_positive_int(value: object, label: str, errors: list[str], *, allow_zero: bool = False) -> int | None:
    if isinstance(value, bool) or not isinstance(value, int) or value < (0 if allow_zero else 1):
        minimum = "non-negative" if allow_zero else "positive"
        errors.append(f"{label}: expected a {minimum} integer")
        return None
    return value


def check_plan(path: Path, errors: list[str]) -> None:
    """Check the portable JSON itinerary contract used by the roadbook workflow."""
    try:
        contents = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{path.name}: cannot read JSON plan: {exc}")
        return

    plan = require_mapping(contents, f"{path.name}", errors)
    if plan is None:
        return

    if plan.get("schema_version") != "1.0":
        errors.append(f"{path.name}: schema_version must be '1.0'")

    trip = require_mapping(plan.get("trip"), f"{path.name}.trip", errors)
    days_value = plan.get("days")
    if not isinstance(days_value, list):
        errors.append(f"{path.name}.days: expected an array")
        days: list[object] = []
    else:
        days = days_value
    sources_value = plan.get("sources")
    if not isinstance(sources_value, list):
        errors.append(f"{path.name}.sources: expected an array")
        sources: list[object] = []
    else:
        sources = sources_value

    start_date: date | None = None
    end_date: date | None = None
    expected_days: int | None = None
    expected_nights: int | None = None
    if trip is not None:
        require_non_empty_string(trip.get("title"), f"{path.name}.trip.title", errors)
        check_timezone(trip.get("timezone"), f"{path.name}.trip.timezone", errors)
        start_date = parse_iso_date(trip.get("start_date"), f"{path.name}.trip.start_date", errors)
        end_date = parse_iso_date(trip.get("end_date"), f"{path.name}.trip.end_date", errors)
        expected_days = require_positive_int(trip.get("expected_days"), f"{path.name}.trip.expected_days", errors)
        expected_nights = require_positive_int(
            trip.get("expected_nights"), f"{path.name}.trip.expected_nights", errors, allow_zero=True
        )
        if start_date is not None and end_date is not None:
            if end_date < start_date:
                errors.append(f"{path.name}.trip: end_date is before start_date")
            elif expected_days is not None:
                calendar_days = (end_date - start_date).days + 1
                if expected_days != calendar_days:
                    errors.append(
                        f"{path.name}.trip.expected_days: expected {calendar_days} from the trip dates, found {expected_days}"
                    )

    if expected_days is not None and len(days) != expected_days:
        errors.append(f"{path.name}.days: expected {expected_days} day entries, found {len(days)}")

    sleep_city_count = 0
    for index, day_value in enumerate(days, start=1):
        label = f"{path.name}.days[{index - 1}]"
        day = require_mapping(day_value, label, errors)
        if day is None:
            continue

        day_number = require_positive_int(day.get("day"), f"{label}.day", errors)
        if day_number is not None and day_number != index:
            errors.append(f"{label}.day: expected D{index}, found D{day_number}")
        actual_date = parse_iso_date(day.get("date"), f"{label}.date", errors)
        if start_date is not None and actual_date is not None:
            required_date = start_date + timedelta(days=index - 1)
            if actual_date != required_date:
                errors.append(
                    f"{label}.date: expected consecutive date {required_date.isoformat()}, found {actual_date.isoformat()}"
                )

        sleep_city = day.get("sleep_city")
        if isinstance(sleep_city, str) and sleep_city.strip():
            sleep_city_count += 1
        elif sleep_city is not None:
            errors.append(f"{label}.sleep_city: expected null or a non-empty string")

        window = require_mapping(day.get("window"), f"{label}.window", errors)
        window_start: int | None = None
        window_end: int | None = None
        if window is not None:
            window_start = parse_time(window.get("start"), f"{label}.window.start", errors)
            window_end = parse_time(window.get("end"), f"{label}.window.end", errors)
            if window_start is not None and window_end is not None and window_start >= window_end:
                errors.append(f"{label}.window: start must be before end")

        blocks_value = day.get("blocks")
        if not isinstance(blocks_value, list):
            errors.append(f"{label}.blocks: expected an array")
            continue
        intervals: list[tuple[int, int, int]] = []
        for block_index, block_value in enumerate(blocks_value):
            block_label = f"{label}.blocks[{block_index}]"
            block = require_mapping(block_value, block_label, errors)
            if block is None:
                continue
            kind = block.get("kind")
            if kind not in VALID_BLOCK_KINDS:
                errors.append(
                    f"{block_label}.kind: expected one of {', '.join(sorted(VALID_BLOCK_KINDS))}"
                )
            require_non_empty_string(block.get("label"), f"{block_label}.label", errors)
            if kind == "travel":
                duration_basis = block.get("duration_basis")
                if duration_basis not in VALID_DURATION_BASES:
                    errors.append(
                        f"{block_label}.duration_basis: expected one of "
                        f"{', '.join(sorted(VALID_DURATION_BASES))}"
                    )
            block_start = parse_time(block.get("start"), f"{block_label}.start", errors)
            block_end = parse_time(block.get("end"), f"{block_label}.end", errors)
            if block_start is None or block_end is None:
                continue
            if block_start >= block_end:
                errors.append(f"{block_label}: start must be before end")
                continue
            if window_start is not None and window_end is not None:
                if block_start < window_start or block_end > window_end:
                    errors.append(f"{block_label}: time block is outside its day window")
            intervals.append((block_start, block_end, block_index))

        intervals.sort()
        for previous, current in zip(intervals, intervals[1:]):
            if current[0] < previous[1]:
                errors.append(
                    f"{label}.blocks[{current[2]}]: overlap with blocks[{previous[2]}]"
                )

    if expected_nights is not None and sleep_city_count != expected_nights:
        errors.append(
            f"{path.name}: expected {expected_nights} nights, found {sleep_city_count} non-null sleep_city entries"
        )

    for index, source_value in enumerate(sources):
        label = f"{path.name}.sources[{index}]"
        source = require_mapping(source_value, label, errors)
        if source is None:
            continue
        require_non_empty_string(source.get("claim"), f"{label}.claim", errors)
        url = source.get("url")
        if not isinstance(url, str) or urlparse(url).scheme not in {"http", "https"} or not urlparse(url).netloc:
            errors.append(f"{label}.url: expected an absolute HTTP(S) URL")
        parse_iso_date(source.get("checked_on"), f"{label}.checked_on", errors)
        applies_on = parse_iso_date(source.get("applies_on"), f"{label}.applies_on", errors)
        if (
            applies_on is not None
            and start_date is not None
            and end_date is not None
            and not start_date <= applies_on <= end_date
        ):
            errors.append(f"{label}.applies_on: date is outside the trip")
        status = source.get("status")
        if status not in VALID_SOURCE_STATUSES:
            errors.append(
                f"{label}.status: expected one of {', '.join(sorted(VALID_SOURCE_STATUSES))}"
            )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--html", type=Path, help="Editable/source HTML")
    parser.add_argument("--plan", type=Path, help="Portable JSON itinerary plan")
    parser.add_argument("--bundle", type=Path, help="Shareable single-file HTML")
    parser.add_argument("--pdf", type=Path, help="Rendered PDF")
    parser.add_argument("--expected-days", type=int)
    parser.add_argument("--expected-nights", type=int)
    parser.add_argument("--expected-revision")
    parser.add_argument("--must-contain", action="append", default=[])
    parser.add_argument("--forbid", action="append", default=[])
    parser.add_argument(
        "--strict-pdf-text",
        action="store_true",
        help="Treat missing or unextractable PDF text as errors instead of warnings",
    )
    args = parser.parse_args()

    if not any((args.html, args.plan, args.bundle, args.pdf)):
        parser.error("at least one input is required: --html, --plan, --bundle, or --pdf")

    errors: list[str] = []
    warnings: list[str] = []
    text = ""
    source_parser: RoadbookParser | None = None

    if args.html:
        html = args.html.resolve()
        if not html.is_file():
            errors.append(f"Source HTML not found: {html}")
        else:
            text, source_parser = check_html(
                html,
                args.expected_days,
                args.expected_nights,
                args.expected_revision,
                errors,
                warnings,
            )
            check_text_tokens(html, text, args.must_contain, args.forbid, errors)

    if args.plan:
        plan = args.plan.resolve()
        if not plan.is_file():
            errors.append(f"Plan JSON not found: {plan}")
        else:
            check_plan(plan, errors)

    if args.bundle:
        bundle = args.bundle.resolve()
        if not bundle.is_file():
            errors.append(f"Shareable bundle not found: {bundle}")
        else:
            bundle_text, bundle_parser = check_html(
                bundle,
                args.expected_days,
                args.expected_nights,
                args.expected_revision,
                errors,
                warnings,
            )
            check_bundle(bundle, errors)
            check_text_tokens(bundle, bundle_text, args.must_contain, args.forbid, errors)
            source_revisions = {value for value in (source_parser.revisions if source_parser else []) if value}
            bundle_revisions = {value for value in bundle_parser.revisions if value}
            if source_revisions and bundle_revisions and source_revisions != bundle_revisions:
                errors.append(
                    "source/bundle roadbook revisions differ: "
                    f"{sorted(source_revisions)!r} vs {sorted(bundle_revisions)!r}"
                )

    if args.pdf:
        pdf = args.pdf.resolve()
        if not pdf.is_file():
            errors.append(f"PDF not found: {pdf}")
        else:
            check_pdf(
                pdf,
                args.must_contain,
                args.forbid,
                errors,
                warnings,
                strict_pdf_text=args.strict_pdf_text,
            )

    result = {"ok": not errors, "errors": errors, "warnings": warnings}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
