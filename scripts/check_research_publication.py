#!/usr/bin/env python3
"""Check canonical SpaceЖ Markdown and on-site study readers agree.

Uses Python standard library only. Verifies publication paths, Git blob
fingerprints, local links, graph presence, and safety disclaimers.
Not a substitute for browser visual checks or scientific validation.
"""
from __future__ import annotations

import hashlib
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUGS = (
    "001-leo-contact",
    "002-independent-early-warning",
    "003-observation-gap",
    "004-claim-validation",
)


class LinksAndIds(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.links: list[str] = []
        self.scripts: list[str] = []
        self.meta: dict[str, str] = {}
        self.math_count = 0
        self.svg_count = 0

    def handle_starttag(self, tag, attrs):
        fields = dict(attrs)
        if fields.get("id"):
            self.ids.add(fields["id"])
        if tag in {"a", "link", "img", "script"}:
            url = fields.get("href") or fields.get("src")
            if url:
                self.links.append(url)
        if tag == "script":
            self.scripts.append(fields.get("src", "inline script"))
        if tag == "meta" and fields.get("name"):
            self.meta[fields["name"]] = fields.get("content", "")
        if tag == "math":
            self.math_count += 1
        if tag == "svg":
            self.svg_count += 1


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def check_reader(slug: str) -> list[str]:
    errors = []
    md_path = ROOT / "research" / slug / "README.md"
    html_path = ROOT / "public" / "research" / slug / "index.html"
    if not md_path.exists() or not html_path.exists():
        return [f"{slug}: missing source or reading page"]
    source = md_path.read_bytes()
    html = html_path.read_text(encoding="utf-8")
    parser = LinksAndIds()
    parser.feed(html)
    expected_sha = git_blob_sha(source)
    if parser.meta.get("research-source-path") != f"research/{slug}/README.md":
        errors.append(f"{slug}: wrong source path metadata")
    if parser.meta.get("research-source-blob") != expected_sha:
        errors.append(f"{slug}: source Markdown changed without regenerating its reader")
    if parser.svg_count != 1:
        errors.append(f"{slug}: expected exactly one static SVG research graph")
    if parser.math_count < 2:
        errors.append(f"{slug}: missing rendered native mathematics")
    if parser.scripts:
        errors.append(f"{slug}: avoid external scripts/runtime Markdown renderers")
    if "Not a detection system" not in html and "No operational missile sensor" not in html:
        errors.append(f"{slug}: missing research status disclaimer")
    for url in parser.links:
        if url.startswith("#") and url[1:] not in parser.ids:
            errors.append(f"{slug}: broken fragment {url}")
        if url.startswith("/") and not url.startswith("//"):
            path = url.split("#", 1)[0].split("?", 1)[0].lstrip("/")
            dest = ROOT / "public" / path
            if path == "" or path.endswith("/"):
                dest = dest / "index.html"
            if not dest.exists():
                errors.append(f"{slug}: missing site link {url}")
    return errors


def main() -> int:
    problems = []
    index_path = ROOT / "public/research/index.html"
    if not index_path.exists():
        return 1
    index_html = index_path.read_text(encoding="utf-8")
    for slug in SLUGS:
        if f'href="/research/{slug}/"' not in index_html:
            problems.append(f"index: missing link to {slug}")
        problems.extend(check_reader(slug))
    for err in problems:
        print("FAIL:", err, file=sys.stderr)
    if problems:
        print(f"{len(problems)} research publication error(s)", file=sys.stderr)
        return 1
    print("PASS: 4 study readers match their Markdown source and expose local graphs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
