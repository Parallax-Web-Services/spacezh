#!/usr/bin/env python3
"""Fetch public source access receipts. Never infer a claim verdict from HTTP access.

Only named public publishers are accepted. Bodies are hashed in memory, not
archived or republished. Re-running appends a new receipt run for comparison.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/relay/retrievals.json"
HOSTS = {"www.telegraph.co.uk", "telegraph.co.uk", "www.aol.com", "aol.com", "www.reuters.com", "reuters.com", "kyivindependent.com", "apnews.com", "www.internazionale.it", "ukraine.ohchr.org", "ukraine.un.org", "www.iaea.org", "iaea.org", "data.unhcr.org", "www.unhcr.org", "www.msp.gov.ua", "www.kmu.gov.ua", "suspilne.media", "kharkivoda.gov.ua"}
MAX_BYTES = 30_000_000


def allowed_url(url):
    try:
        parsed = urlsplit(url)
        return parsed.scheme == "https" and parsed.hostname in HOSTS and parsed.port in (None, 443) and not parsed.username and not parsed.password
    except (TypeError, ValueError):
        return False


class PublisherRedirects(HTTPRedirectHandler):
    def redirect_request(self, request, response, code, message, headers, newurl):
        if not allowed_url(newurl):
            raise ValueError("Redirect left the explicit public-publisher allowlist")
        return super().redirect_request(request, response, code, message, headers, newurl)


def utc_now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def fetch_source(url, timeout=15, open_url=None):
    receipt = {"requested_url": url, "final_url": url, "retrieved_at": utc_now(), "method": "public_https_get", "status": "unavailable", "http_status": None, "content_type": None, "body_sha256": None, "bytes": None}
    if not allowed_url(url):
        receipt["error"] = "URL is outside the public-publisher allowlist"
        return receipt
    request = Request(url, headers={"User-Agent": "SpaceZh-Public-Source-Audit/0.1 (+https://github.com/Parallax-Web-Services/spacezh)", "Accept": "text/html,application/pdf;q=0.9,*/*;q=0.5", "Accept-Encoding": "identity"})
    opener = open_url or build_opener(PublisherRedirects()).open
    try:
        with opener(request, timeout=timeout) as response:
            final = response.geturl()
            if not allowed_url(final):
                raise ValueError("Response URL left the public-publisher allowlist")
            receipt.update(final_url=final, http_status=response.status, content_type=response.headers.get("Content-Type", "unknown"))
            fingerprint = hashlib.sha256()
            size = 0
            while True:
                block = response.read(65536)
                if not block:
                    break
                size += len(block)
                if size > MAX_BYTES:
                    raise ValueError("Response exceeds the 30 MB receipt limit; no partial fingerprint retained")
                fingerprint.update(block)
            receipt.update(status="retrieved", body_sha256=fingerprint.hexdigest(), bytes=size)
    except HTTPError as exc:
        receipt.update(http_status=exc.code, error="Publisher returned HTTP " + str(exc.code))
        if exc.fp is not None:
            exc.fp.close()
    except Exception as exc:
        receipt["error"] = type(exc).__name__ + ": " + str(exc)[:180]
    return receipt


def source_urls(data):
    urls = set()
    for case in data["cases"]:
        if case["kind"] == "synthetic":
            continue
        for source in case["sources"]:
            for url in (source["url"], source.get("alternate_url"), source.get("verification", {}).get("reviewed_url")):
                if url:
                    if not allowed_url(url):
                        raise ValueError("Source URL is outside the publisher allowlist: " + url)
                    urls.add(url)
    return sorted(urls)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeout", type=int, default=15)
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    data = json.loads((ROOT / "data/relay/cases.json").read_text(encoding="utf-8"))
    urls = source_urls(data)
    started = utc_now()
    with ThreadPoolExecutor(max_workers=max(1, min(args.workers, 4))) as pool:
        receipts = list(pool.map(lambda url: fetch_source(url, args.timeout), urls))
    audit = json.loads(AUDIT.read_text(encoding="utf-8")) if AUDIT.exists() else {"schema_version": "spacezh.relay.retrievals.v1", "runs": []}
    audit["runs"].append({"started_at": started, "completed_at": utc_now(), "receipts": receipts})
    AUDIT.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    retrieved = sum(item["status"] == "retrieved" for item in receipts)
    print(f"Recorded {len(receipts)} real source access attempts: {retrieved} retrieved; {len(receipts) - retrieved} unavailable.")
    print("Receipts establish access to response bytes, not factual verification or editorial approval.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
