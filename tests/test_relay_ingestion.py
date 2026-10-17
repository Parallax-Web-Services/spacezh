"""Transport receipts must not become factual verdicts or fictional public cases."""
import copy
import hashlib
import io
import sys
import unittest
from pathlib import Path
from urllib.error import HTTPError

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from ingest_relay_sources import allowed_url, fetch_source
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
