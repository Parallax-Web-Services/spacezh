#!/usr/bin/env python3
"""Verify SpaceЖ evidence-brief publication, attribution, and local links.

Standard library only. This enforces source integrity and status disclosures,
not the independent factual truth of any reporting or the presence of a RELAY feed.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "data/evidence/starshield-restrictions-2026-10-16.json"
SOURCE = ROOT / "docs/evidence/2026-10-16-starshield.md"
ARTICLE = ROOT / "public/research/briefings/starshield-restrictions/index.html"
HUB = ROOT / "public/research/index.html"
HOME = ROOT / "public/index.html"
CSS = ROOT / "public/assets/evidence-brief.css"
PATH = "/research/briefings/starshield-restrictions/"


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.links = []
        self.meta = {}
        self.scripts = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag in ("a", "link", "img", "script"):
            url = a.get("href") or a.get("src")
            if url:
                self.links.append(url)
        if tag == "meta" and a.get("name"):
            self.meta[a["name"]] = a.get("content", "")
        if tag == "script":
            self.scripts.append(a.get("src") or "inline")


def git_blob_sha(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\\0" + raw).hexdigest()


def run():
    errors = []
    for f in [RECORD, SOURCE, ARTICLE, HUB, HOME, CSS]:
        if not f.is_file():
            errors.append("missing file: " + str(f.relative_to(ROOT)))
    if errors:
        return errors
    record = json.loads(RECORD.read_text(encoding="utf-8"))
    source_text = SOURCE.read_text(encoding="utf-8")
    article_text = ARTICLE.read_text(encoding="utf-8")
    if record.get("schema_version") != "spacezh.evidence_brief.v1":
        errors.append("unsupported source register schema")
    if record.get("relay_integration_status") != "staged_in_repository_not_imported_to_RELAY":
        errors.append("misleading RELAY ingestion status")
    if record.get("canonical_public_path") != PATH:
        errors.append("wrong public article route")
    sources = record.get("sources", [])
    claims = record.get("claims", [])
    ids = [x.get("id") for x in sources]
    if len(ids) != len(set(ids)) or len(ids) < 6:
        errors.append("insufficient/duplicate source IDs")
    if len(claims) < 6 or len(set(x.get("id") for x in claims)) != len(claims):
        errors.append("insufficient/duplicate claim IDs")
    for claim in claims:
        if not claim.get("source_ids") or not set(claim["source_ids"]).issubset(set(ids)):
            errors.append("uncited or unknown source: " + str(claim.get("id")))
        if not claim.get("evidence_class") or not claim.get("caveat"):
            errors.append("missing caveat/status for " + str(claim.get("id")))
    if not any(x.get("source_type") == "on_record_denial" for x in sources):
        errors.append("missing on-record denial")
    if not any(x.get("source_type") == "independent_exclusive" for x in sources):
        errors.append("missing independently sourced White House report")
    if not any("one underlying investigation" in x for x in record.get("source_independence_notes", [])):
        errors.append("Telegraph syndication must not be counted twice")
    if "not independently" not in article_text or "Trump" not in article_text:
        errors.append("brief must clearly preserve uncertainty and denial")
    if "no live" not in article_text.lower() and "not a claim that SpaceЖ" not in article_text:
        errors.append("missing operational capability caveat")
    page = Page()
    page.feed(article_text)
    digest = git_blob_sha(SOURCE.read_bytes().replace(b"\\r\\n", b"\\n"))
    if page.meta.get("evidence-source-path") != str(SOURCE.relative_to(ROOT)):
        errors.append("wrong canonical source path")
    if page.meta.get("evidence-source-blob") != digest:
        errors.append("canonical editorial Markdown changed without updating site reader")
    if page.scripts:
        errors.append("runtime script dependency on evidence page")
    for url in page.links:
        if url.startswith("#") and url[1:] not in page.ids:
            errors.append("broken fragment " + url)
        if url.startswith("/") and not url.startswith("//"):
            local = url.split("?", 1)[0].split("#", 1)[0].lstrip("/")
            destination = ROOT / "public" / local
            if not local or local.endswith("/"):
                destination /= "index.html"
            if not destination.is_file():
                errors.append("broken local link " + url)
    for source in sources:
        if not source.get("url", "").startswith("https://"):
            errors.append("missing HTTPS citation URL")
        if source.get("url") not in source_text:
            errors.append("source absent from canonical Markdown: " + str(source.get("id")))
    for entry in (HOME, HUB):
        text = entry.read_text(encoding="utf-8")
        if 'href="' + PATH + '"' not in text:
            errors.append("feature not linked from " + entry.name)
        if 'href="/assets/evidence-brief.css"' not in text:
            errors.append("feature stylesheet not linked from " + entry.name)
    if re.search(r'<img[^>]+(?:musk|trump|telegraph)', article_text, re.I):
        errors.append("third-party photos should not be copied into the site")
    return errors


if __name__ == "__main__":
    failures = run()
    for problem in failures:
        print("FAIL:", problem, file=sys.stderr)
    if failures:
        print(f"{len(failures)} evidence-publication error(s)", file=sys.stderr)
        raise SystemExit(1)
    print("PASS: cited evidence brief, source fingerprint, denials, and local links.")
