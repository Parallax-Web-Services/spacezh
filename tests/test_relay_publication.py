"""Regression tests for broken provenance and misleading demo publication states."""
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from check_relay_publication import check_exports
from relay_registry import ROOT, SCHEMA, digest, load_source, publication, validate_registry, validate_public_snapshot


def fixture():
    old, new = "The fictional library closed at 16:00.", "The fictional library closed at 17:00."
    return {"schema_version": SCHEMA, "prototype": True, "confidential_intake": False, "trusted_operational_feed": False, "cases": [{
        "id": "demo", "kind": "synthetic", "visibility": "public", "title": "Fictional notice", "summary": "Synthetic correction exercise", "status": "corrected", "boundary_note": "Synthetic exercise", "publication_note": "Simulated history", "tags": ["synthetic"], "source_independence_notes": [], "timeline": [], "provenance": {"label": "Local fixture", "url": "./data/cases.json", "note": "Synthetic"},
        "sources": [{"id": "notice", "title": "Invented public notice", "url": "#artifact-notice", "publisher": "Fictional library", "byline": "Simulated", "published_date": "2026-10-16", "source_type": "synthetic", "notes": "Synthetic", "rights": "Original exercise text"}],
        "artifacts": [{"id": "notice", "source_id": "notice", "content": new, "rights": "Synthetic fixture", "sha256": digest(new.encode())}],
        "claims": [{"id": "hours", "text": new, "kind": "observation", "status": "supported", "caveat": "Fictional; no real event", "source_ids": ["notice"]}],
        "evidence_links": [{"claim_id": "hours", "source_id": "notice", "relationship": "supports", "rationale": "Corrected synthetic notice"}],
        "reviews": [{"id": "review", "reviewer": "Fictional reviewer", "kind": "simulated", "decision": "approved_for_demo", "rationale": "Exercise only", "conflicts": "No real reviewer"}],
        "revisions": [{"id": "v1", "parent_revision_id": None, "published_at": "2026-10-16T10:00:00Z", "change_note": "First simulated publication", "review_ids": ["review"], "claim_snapshots": [{"claim_id": "hours", "text": old, "status": "supported"}]}, {"id": "v2", "parent_revision_id": "v1", "published_at": "2026-10-16T11:00:00Z", "change_note": "Corrected fictional closing time", "review_ids": ["review"], "claim_snapshots": [{"claim_id": "hours", "text": new, "status": "supported"}]}],
        "corrections": [{"id": "c1", "from_revision_id": "v1", "to_revision_id": "v2", "claim_id": "hours", "cause": "A deliberately misread timestamp", "before": old, "after": new, "source_ids": ["notice"]}]
    }]}


class RegistryTests(unittest.TestCase):
    def setUp(self):
        self.data = fixture()
        self.case = self.data["cases"][0]

    def rejects(self, fragment):
        errors = validate_registry(self.data)
        self.assertTrue(any(fragment in error for error in errors), errors)

    def test_valid_simulated_lifecycle(self):
        self.assertEqual(validate_registry(self.data), [])

    def test_restricted_records_do_not_export(self):
        self.case["visibility"] = "restricted"
        self.rejects("only public")

    def test_operational_or_confidential_flags_rejected(self):
        self.data["confidential_intake"] = True
        self.data["trusted_operational_feed"] = True
        self.rejects("confidential intake")
        self.rejects("operational feed")

    def test_unknown_source_cannot_support_claim(self):
        self.case["claims"][0]["source_ids"] = ["missing"]
        self.rejects("unknown claim source")

    def test_unsafe_citation_rejected(self):
        self.case["sources"][0]["url"] = "javascript:alert(1)"
        self.rejects("unsafe or missing source URL")

    def test_artifact_mutation_detected(self):
        self.case["artifacts"][0]["content"] += " changed"
        self.rejects("fingerprint mismatch")

    def test_missing_review_blocks_simulated_revision(self):
        self.case["revisions"][1]["review_ids"] = ["missing"]
        self.rejects("missing simulated approval")

    def test_fictional_review_cannot_claim_human_approval(self):
        self.case["reviews"][0]["kind"] = "human"
        self.rejects("explicitly simulated")

    def test_broken_revision_chain_rejected(self):
        self.case["revisions"][1]["parent_revision_id"] = None
        self.rejects("broken revision chain")

    def test_correction_preserves_before_and_after(self):
        self.case["corrections"][0]["before"] = "History rewritten"
        self.rejects("differs from preserved revisions")

    def test_silent_revision_edit_rejected(self):
        self.case["corrections"] = []
        self.rejects("changed claim lacks correction")

    def test_public_snapshot_cannot_gain_fabricated_history(self):
        self.case["kind"] = "public_snapshot"
        self.rejects("must not invent review")

    def test_current_claim_matches_latest_revision(self):
        self.case["claims"][0]["text"] = "Unreviewed replacement"
        self.rejects("differs from latest revision")

    def test_renderer_required_fields_are_checked(self):
        del self.case["tags"]
        self.rejects("invalid text list: tags")

    def test_unknown_correction_citation_rejected(self):
        self.case["corrections"][0]["source_ids"] = ["missing"]
        self.rejects("unknown or missing correction source")

    def test_unknown_timeline_references_rejected(self):
        self.case["timeline"] = [{"date": "2026-10-16", "label": "Review", "detail": "Synthetic", "source_ids": ["missing"], "review_id": "missing", "revision_id": "missing"}]
        self.rejects("unknown timeline source")
        self.rejects("unknown timeline review")
        self.rejects("unknown timeline revision")

    def test_status_only_correction_keeps_old_status(self):
        correction = self.case["corrections"][0]
        correction["after"] = correction["before"]
        self.case["claims"][0]["text"] = correction["before"]
        self.case["claims"][0]["status"] = "disputed"
        snapshot = self.case["revisions"][1]["claim_snapshots"][0]
        snapshot["text"] = correction["before"]
        snapshot["status"] = "disputed"
        correction.update(before_status="supported", after_status="disputed")
        self.assertEqual(validate_registry(self.data), [])
        correction["before_status"] = "unresolved"
        self.rejects("correction status differs")

    def test_public_snapshot_preserves_caveats_and_source_dependencies(self):
        data = load_source()
        case = copy.deepcopy(next(item for item in data["cases"] if item["kind"] == "public_snapshot"))
        original = json.loads((ROOT / case["source_record"]).read_text(encoding="utf-8"))
        self.assertEqual(validate_public_snapshot(case, original), [])
        case["claims"][0]["caveat"] = "Unsupported certainty"
        case["source_independence_notes"] = []
        errors = validate_public_snapshot(case, original)
        self.assertTrue(any("caveat" in error for error in errors))
        self.assertTrue(any("independence" in error for error in errors))

    def test_export_is_deterministic_and_staleness_detected(self):
        files = publication(self.data)
        self.assertEqual(files, publication(copy.deepcopy(self.data)))
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder)
            for name, raw in files.items():
                (target / name).write_bytes(raw)
            self.assertEqual(check_exports(self.data, target), [])
            (target / "cases.json").write_bytes(files["cases.json"].replace(b"\n", b"\r\n"))
            self.assertTrue(check_exports(self.data, target))
            (target / "cases.json").write_text("{}", encoding="utf-8")
            self.assertTrue(check_exports(self.data, target))


if __name__ == "__main__":
    unittest.main()
