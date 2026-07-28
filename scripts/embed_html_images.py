#!/usr/bin/env python3
"""Embed local <img src> files as data URLs in an HTML document."""

from __future__ import annotations

import argparse
import base64
import mimetypes
import re
from pathlib import Path
from urllib.parse import unquote, urlparse


IMG_SRC_RE = re.compile(
    r"(?P<prefix><img\b[^>]*?\bsrc\s*=\s*)(?P<quote>['\"])(?P<src>.*?)(?P=quote)",
    re.IGNORECASE | re.DOTALL,
)


def is_external(src: str) -> bool:
    parsed = urlparse(src)
    return parsed.scheme in {"http", "https", "data", "blob", "mailto", "tel"} or src.startswith("//")


def resolve_local(src: str, base_dir: Path) -> Path:
    clean = unquote(urlparse(src).path)
    path = Path(clean)
    if path.is_absolute():
        return path
    return (base_dir / path).resolve()


def encode_file(path: Path) -> str:
    mime, _ = mimetypes.guess_type(path.name)
    mime = mime or "application/octet-stream"
    payload = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{payload}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Source HTML")
    parser.add_argument("output", type=Path, help="Shareable output HTML")
    parser.add_argument(
        "--base-dir",
        type=Path,
        help="Base directory for local image paths; defaults to the source directory",
    )
    args = parser.parse_args()

    source = args.source.resolve()
    output = args.output.resolve()
    base_dir = (args.base_dir or source.parent).resolve()
    html = source.read_text(encoding="utf-8")
    embedded = 0
    missing: list[str] = []

    def replace(match: re.Match[str]) -> str:
        nonlocal embedded
        src = match.group("src").strip()
        if not src or src.startswith("#") or is_external(src):
            return match.group(0)
        local_path = resolve_local(src, base_dir)
        if not local_path.is_file():
            missing.append(f"{src} -> {local_path}")
            return match.group(0)
        embedded += 1
        return f"{match.group('prefix')}{match.group('quote')}{encode_file(local_path)}{match.group('quote')}"

    bundled = IMG_SRC_RE.sub(replace, html)
    if missing:
        details = "\n".join(f"- {item}" for item in missing)
        raise SystemExit(f"Missing local image files:\n{details}")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(bundled, encoding="utf-8")
    print(f"Embedded {embedded} local image(s): {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
