#!/usr/bin/env python3
"""Check RELAY fixture references, revisions, citations and generated exports."""
import sys
import hashlib
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
from relay_registry import PUBLIC, ROOT, load_source, publication, validate_registry, validate_repository_sources, validate_publication_boundary


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = []
        self.meta = {}

    def handle_starttag(self, tag, attrs):
        fields = dict(attrs)
        if tag == "meta" and fields.get("name"):
            self.meta[fields["name"]] = fields.get("content", "")
        if fields.get("id"):
            self.ids.append(fields["id"])
        if tag in {"a", "link", "img", "script"}:
            url = fields.get("href") or fields.get("src")
            if url:
                self.links.append(url)


def check_exports(data, directory=PUBLIC):
    errors = []
    for name, expected in publication(data).items():
        target = directory / name
        if not target.is_file() or target.read_bytes() != expected:
            errors.append("stale or missing public export: " + name)
    return errors


def run():
    data = load_source()
    errors = validate_registry(data)
    errors.extend(validate_publication_boundary(data))
    if errors:
        return errors
    errors.extend(validate_repository_sources(data))
    errors.extend(check_exports(data))
    route = ROOT / "public/relay/index.html"
    page = Page()
    page.feed(route.read_text(encoding="utf-8"))
    if len(page.ids) != len(set(page.ids)):
        errors.append("duplicate RELAY page IDs")
    for link in page.links:
        parsed = urlsplit(link)
        if parsed.scheme or parsed.netloc or link.startswith("#"):
            continue
        path = ROOT / "public" / parsed.path.lstrip("/") if parsed.path.startswith("/") else route.parent / parsed.path
        if parsed.path.endswith("/"):
            path /= "index.html"
        if not path.is_file():
            errors.append("broken RELAY asset or local link: " + link)
    plan = Page()
    plan.feed((ROOT / "public/plan/index.html").read_text(encoding="utf-8"))
    source = (ROOT / "docs/FOUNDING_PROPOSAL.md").read_bytes().replace(b"\r\n", b"\n")
    if plan.meta.get("founding-source-path") != "docs/FOUNDING_PROPOSAL.md" or plan.meta.get("founding-source-sha256") != hashlib.sha256(source).hexdigest():
        errors.append("founding proposal changed without synchronizing the static plan")
    return errors


if __name__ == "__main__":
    try:
        failures = run()
    except (OSError, ValueError, TypeError, KeyError) as exc:
        failures = [str(exc)]
    for failure in failures:
        print("FAIL:", failure, file=sys.stderr)
    if failures:
        raise SystemExit(1)
    print("PASS: RELAY public fixtures, citations, revision/correction history and export fingerprints.")
