"""Transport receipts must not become factual verdicts or fictional public cases."""
import copy
import hashlib
import io
import sys
import unittest
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from ingest_relay_sources import PublisherRedirects, allowed_url, fetch_source, source_urls
from relay_registry import attach_receipts, load_source, validate_publication_boundary, validate_registry

URL = "https://ukraine.ohchr.org/en/public-report"


class PublicResponse(io.BytesIO):
    status = 200
    headers = {"Content-Type": "text/html; charset=utf-8"}

    def geturl(self):
        return URL


class IngestionTests(unittest.TestCase):
    def test_only_named_https_publishers_are_requested(self):
        self.assertTrue(allowed_url(URL))
        for url in ("http://ukraine.ohchr.org/report", "https://127.0.0.1/", "https://ukraine.ohchr.org.evil.example/", "https://person:password@ukraine.ohchr.org/", "https://ukraine.ohchr.org:8080/"):
            self.assertFalse(allowed_url(url), url)

    def test_followup_sources_accept_only_the_named_new_publishers(self):
        data = {"cases": [{"kind": "public_case", "sources": [
            {"url": "https://www.msp.gov.ua/", "alternate_url": "https://www.kmu.gov.ua/", "verification": {"reviewed_url": "https://suspilne.media/"}},
            {"url": "https://kharkivoda.gov.ua/"},
        ]}]}
        self.assertEqual(source_urls(data), sorted(["https://www.msp.gov.ua/", "https://www.kmu.gov.ua/", "https://suspilne.media/", "https://kharkivoda.gov.ua/"]))

    def test_followup_hosts_do_not_admit_subdomains_or_unsafe_urls(self):
        for url in ("https://news.msp.gov.ua/", "https://msp.gov.ua/", "https://www.kmu.gov.ua.evil.example/", "https://cdn.suspilne.media/", "http://kharkivoda.gov.ua/", "https://person:password@www.msp.gov.ua/", "https://suspilne.media:8080/"):
            with self.subTest(url=url):
                self.assertFalse(allowed_url(url))
                with self.assertRaisesRegex(ValueError, "outside the publisher allowlist"):
                    source_urls({"cases": [{"kind": "public_case", "sources": [{"url": url}]}]})

    def test_followup_redirects_stay_within_exact_https_publisher_hosts(self):
        redirects = PublisherRedirects()
        request = Request("https://www.msp.gov.ua/")
        allowed = redirects.redirect_request(request, None, 302, "Found", {}, "https://www.kmu.gov.ua/")
        self.assertEqual(allowed.full_url, "https://www.kmu.gov.ua/")
        for target in ("https://cdn.suspilne.media/", "https://unlisted.example/", "http://www.msp.gov.ua/"):
            with self.subTest(target=target), self.assertRaisesRegex(ValueError, "explicit public-publisher allowlist"):
                redirects.redirect_request(request, None, 302, "Found", {}, target)

    def test_public_records_accept_only_exact_publisher_hosts(self):
        hosts = ("dp-reintegration.gov.ua", "fcdo.iati.cloud", "devtracker.fcdo.gov.uk", "iati.fcdo.gov.uk", "fastiv-rada.gov.ua", "reyestr.court.gov.ua", "opendatabot.ua", "snovmr.gov.ua")
        for host in hosts:
            with self.subTest(host=host):
                url = "https://" + host + "/public-record?format=json"
                self.assertEqual(source_urls({"cases": [{"kind": "public_case", "sources": [{"url": url}]}]}), [url])
                for unsafe in ("http://" + host + "/", "https://" + host + ".evil.example/", "https://sub." + host + "/", "https://user:password@" + host + "/", "https://" + host + ":8443/"):
                    self.assertFalse(allowed_url(unsafe), unsafe)

    def test_public_record_redirects_reject_unlisted_and_unsafe_destinations(self):
        redirects = PublisherRedirects()
        request = Request("https://reyestr.court.gov.ua/Review/131707397")
        for target in ("https://snovmr.gov.ua.evil.example/", "https://cdn.fastiv-rada.gov.ua/", "http://iati.fcdo.gov.uk/", "https://user:password@fcdo.iati.cloud/", "https://reyestr.court.gov.ua:8443/"):
            with self.subTest(target=target), self.assertRaisesRegex(ValueError, "explicit public-publisher allowlist"):
                redirects.redirect_request(request, None, 302, "Found", {}, target)

    def test_invalid_url_never_calls_the_network(self):
        def unexpected(*args, **kwargs):
            self.fail("Disallowed URL reached network")
        receipt = fetch_source("https://127.0.0.1/", open_url=unexpected)
        self.assertEqual(receipt["status"], "unavailable")
        self.assertIsNone(receipt["body_sha256"])

    def test_success_receipt_fingerprints_actual_response_bytes(self):
        body = b"<html><body>A public statement</body></html>"
        receipt = fetch_source(URL, open_url=lambda *args, **kwargs: PublicResponse(body))
        self.assertEqual(receipt["status"], "retrieved")
        self.assertEqual(receipt["bytes"], len(body))
        self.assertEqual(receipt["body_sha256"], hashlib.sha256(body).hexdigest())
        self.assertEqual(receipt["http_status"], 200)
        self.assertNotIn("content", receipt)

    def test_access_failure_is_recorded_without_a_fingerprint(self):
        def denied(*args, **kwargs):
            raise HTTPError(URL, 403, "Forbidden", {}, None)
        receipt = fetch_source(URL, open_url=denied)
        self.assertEqual(receipt["status"], "unavailable")
        self.assertEqual(receipt["http_status"], 403)
        self.assertIsNone(receipt["body_sha256"])

    def test_receipts_do_not_promote_claims_or_create_content_review(self):
        data = load_source()
        before = copy.deepcopy(data["cases"][0]["claims"])
        source = data["cases"][0]["sources"][0]
        source.pop("verification", None)
        receipt = {"requested_url": source["url"], "status": "retrieved", "http_status": 200}
        result = attach_receipts(data, {"runs": [{"completed_at": "2026-10-17T19:00:00Z", "receipts": [receipt]}]})
        self.assertEqual(result["cases"][0]["claims"], before)
        self.assertNotIn("verification", result["cases"][0]["sources"][0])

    def test_public_registry_contains_only_real_cases(self):
        data = load_source()
        self.assertEqual(validate_registry(data), [])
        self.assertEqual(validate_publication_boundary(data), [])
        self.assertTrue(all(case["kind"] != "synthetic" for case in data["cases"]))
        data["cases"].append({"kind": "synthetic"})
        self.assertTrue(validate_publication_boundary(data))

    def test_verification_questions_must_cite_known_sources(self):
        data = load_source()
        data["cases"][0]["open_questions"][0]["source_ids"] = ["missing"]
        self.assertTrue(any("unknown verification question source" in error for error in validate_registry(data)))

    def test_failed_retrieval_cannot_claim_an_archived_response_hash(self):
        data = load_source()
        data["cases"][0]["sources"][0]["retrieval"] = {"method": "public_https_get", "retrieved_at": "2026-10-17T19:00:00Z", "status": "unavailable", "body_sha256": "0" * 64}
        self.assertTrue(any("unavailable response cannot claim" in error for error in validate_registry(data)))


if __name__ == "__main__":
    unittest.main()
