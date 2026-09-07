#!/usr/bin/env python3
"""Embed local HTML and CSS resources as data URLs in an HTML document."""

from __future__ import annotations

import argparse
import base64
import mimetypes
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse


IMG_SRC_RE = re.compile(
    r"(?P<prefix><img\b[^>]*?\bsrc\s*=\s*)(?P<quote>['\"])(?P<src>.*?)(?P=quote)",
    re.IGNORECASE | re.DOTALL,
)
SRCSET_RE = re.compile(
    r"(?P<prefix>\bsrcset\s*=\s*)(?P<quote>['\"])(?P<srcset>.*?)(?P=quote)",
    re.IGNORECASE | re.DOTALL,
)
SRCSET_CANDIDATE_RE = re.compile(
    r"(?P<url>data:\S+|[^\s,]+)(?P<descriptor>(?:\s+[^,]+)?)",
    re.IGNORECASE,
)
CSS_URL_RE = re.compile(
    r"(?P<prefix>url\(\s*)(?:(?P<quote>['\"])(?P<quoted>.*?)(?P=quote)|(?P<bare>[^)\s][^)]*?))(?P<suffix>\s*\))",
    re.IGNORECASE | re.DOTALL,
)
CSS_IMPORT_RE = re.compile(
    r"@import\s+(?:url\(\s*(?:['\"](?P<url_quoted>.*?)['\"]|(?P<url_bare>[^)\s][^)]*?))\s*\)|['\"](?P<quoted>.*?)['\"])",
    re.IGNORECASE | re.DOTALL,
)
UNSUPPORTED_RESOURCE_ATTRS = {
    "audio": ("src",),
    "embed": ("src",),
    "iframe": ("src",),
    "input": ("src",),
    "link": ("href",),
    "object": ("data",),
    "script": ("src",),
    "source": ("src",),
    "track": ("src",),
    "video": ("src", "poster"),
}


class DependencyParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.dependencies: list[tuple[str, str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        for attribute in UNSUPPORTED_RESOURCE_ATTRS.get(tag, ()):
            value = values.get(attribute)
            if value:
                self.dependencies.append((tag, attribute, value))


def is_external(src: str) -> bool:
    parsed = urlparse(src)
    return parsed.scheme not in {"", "file"} or src.startswith("//")


def resolve_local(src: str, base_dir: Path) -> Path:
    clean = unquote(urlparse(src).path)
    path = Path(clean)
    trusted_root = base_dir.resolve()
    resolved = path.resolve() if path.is_absolute() else (trusted_root / path).resolve()
    try:
        resolved.relative_to(trusted_root)
    except ValueError as exc:
        raise ValueError(
            f"Local asset is outside trusted base directory: {src} -> {resolved}"
        ) from exc
    return resolved


def encode_file(path: Path) -> str:
    mime, _ = mimetypes.guess_type(path.name)
    mime = mime or "application/octet-stream"
    payload = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{payload}"


def unsupported_local_dependencies(html: str) -> list[str]:
    parser = DependencyParser()
    parser.feed(html)
    dependencies = [
        f"<{tag} {attribute}=\"{value}\">"
        for tag, attribute, value in parser.dependencies
        if not value.startswith("#") and not is_external(value)
    ]
    for match in CSS_IMPORT_RE.finditer(html):
        value = next(
            group for group in (match.group("url_quoted"), match.group("url_bare"), match.group("quoted"))
            if group is not None
        ).strip()
        if value and not value.startswith("#") and not is_external(value):
            dependencies.append(f"CSS @import {value}")
    return list(dict.fromkeys(dependencies))


def embed_url(src: str, base_dir: Path, missing: list[str]) -> tuple[str, bool]:
    """Return an embeddable URL and whether it replaced a local resource."""
    src = src.strip()
    if not src or src.startswith("#") or is_external(src):
        return src, False

    parsed = urlparse(src)
    try:
        local_path = resolve_local(src, base_dir)
    except ValueError as exc:
        raise SystemExit(str(exc)) from None
    if not local_path.is_file():
        missing.append(f"{src} -> {local_path}")
        return src, False

    embedded = encode_file(local_path)
    if parsed.fragment:
        embedded = f"{embedded}#{parsed.fragment}"
    return embedded, True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Source HTML")
    parser.add_argument("output", type=Path, help="Shareable output HTML")
    parser.add_argument(
        "--base-dir",
        type=Path,
        help="Base directory for local asset paths; defaults to the source directory",
    )
    args = parser.parse_args()

    source = args.source.resolve()
    output = args.output.resolve()
    base_dir = (args.base_dir or source.parent).resolve()
    html = source.read_text(encoding="utf-8")
    unsupported = unsupported_local_dependencies(html)
    if unsupported:
        details = "\n".join(f"- {item}" for item in unsupported)
        raise SystemExit(
            "Unsupported local dependencies must be inlined or removed before bundling:\n"
            f"{details}"
        )
    embedded = 0
    missing: list[str] = []

    def replace_img_src(match: re.Match[str]) -> str:
        nonlocal embedded
        src, was_embedded = embed_url(match.group("src"), base_dir, missing)
        if not was_embedded:
            return match.group(0)
        embedded += 1
        return f"{match.group('prefix')}{match.group('quote')}{src}{match.group('quote')}"

    def replace_srcset(match: re.Match[str]) -> str:
        nonlocal embedded

        def replace_candidate(candidate: re.Match[str]) -> str:
            nonlocal embedded
            src, was_embedded = embed_url(candidate.group("url"), base_dir, missing)
            if was_embedded:
                embedded += 1
            return f"{src}{candidate.group('descriptor')}"

        srcset = SRCSET_CANDIDATE_RE.sub(replace_candidate, match.group("srcset"))
        return f"{match.group('prefix')}{match.group('quote')}{srcset}{match.group('quote')}"

    def replace_css_url(match: re.Match[str]) -> str:
        nonlocal embedded
        original = match.group("quoted") if match.group("quote") else match.group("bare")
        src, was_embedded = embed_url(original, base_dir, missing)
        if not was_embedded:
            return match.group(0)
        embedded += 1
        quote = match.group("quote") or ""
        return f"{match.group('prefix')}{quote}{src}{quote}{match.group('suffix')}"

    bundled = IMG_SRC_RE.sub(replace_img_src, html)
    bundled = SRCSET_RE.sub(replace_srcset, bundled)
    bundled = CSS_URL_RE.sub(replace_css_url, bundled)
    if missing:
        details = "\n".join(f"- {item}" for item in missing)
        raise SystemExit(f"Missing local asset files:\n{details}")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(bundled, encoding="utf-8")
    print(f"Embedded {embedded} local asset reference(s): {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
