"""Real publication records must preserve the published baseline and exact review state."""
import copy
import json
import subprocess
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from relay_registry import ROOT, claim_snapshot, digest, encoded, validate_registry, validate_repository_sources

BASELINE_COMMIT = "dd67d14ca52eea17a8d6c1a12a5c31d80c66370e"


def real_history_fixture():
    raw = subprocess.run(["git", "show", BASELINE_COMMIT + ":data/relay/cases.json"], cwd=ROOT, check=True, capture_output=True).stdout
    data = json.loads(raw.decode("utf-8"))
    case = next(record for record in data["cases"] if record["kind"] == "public_case")
    data["cases"] = [case]
    baseline = [claim_snapshot(claim) for claim in case["claims"]]
    before = copy.deepcopy(baseline[-1])
    case["claims"][-1]["caveat"] += " The delivery period must be matched before comparison."
    updated = [claim_snapshot(claim) for claim in case["claims"]]
    after = copy.deepcopy(updated[-1])
    case["revisions"] = [
        {"id": "published-baseline", "parent_revision_id": None, "published_at": "2026-10-17T20:52:30.313791+00:00", "recorded_at": "2026-10-17T21:00:00Z", "historical_import": True, "source_commit": BASELINE_COMMIT, "source_path": "data/relay/cases.json", "import_note": "Imported from the published commit; timestamp is the observed public upper bound, not exact activation.", "review_ids": [], "change_note": "Preserve the previously published claim state without inventing review.", "claim_snapshots": baseline},
        {"id": "period-clarification", "parent_revision_id": "published-baseline", "published_at": "2026-10-17T21:01:00Z", "recorded_at": "2026-10-17T21:01:00Z", "publication_basis": "user_authorized", "review_ids": ["review-period"], "change_note": "Clarify the comparison period.", "claim_snapshots": updated},
    ]
    case["reviews"] = [{"id": "review-period", "kind": "ai_assisted", "reviewer_type": "ai", "decision": "reviewed", "reviewer": "AI test reviewer", "reviewed_at": "2026-10-17T21:00:30Z", "method": "Compared the cited source and revised caveat.", "scope": "Claim wording and source attribution.", "rationale": "The period caveat bounds the comparison.", "conflicts": "No human sign-off is represented.", "revision_id": "period-clarification", "snapshot_sha256": digest(encoded(updated))}]
    case["corrections"] = [{"id": "change-period", "kind": "clarification", "from_revision_id": "published-baseline", "to_revision_id": "period-clarification", "claim_id": before["claim_id"], "cause": "Make the comparison period explicit.", "before": before["text"], "after": after["text"], "before_status": before["status"], "after_status": after["status"], "before_snapshot": before, "after_snapshot": after, "source_ids": after["source_ids"], "recorded_at": "2026-10-17T21:01:00Z"}]
    return data


class RealHistoryTests(unittest.TestCase):
    def setUp(self):
        self.data = real_history_fixture()
        self.case = self.data["cases"][0]

    def rejects(self, fragment):
        errors = validate_registry(self.data)
        self.assertTrue(any(fragment in error for error in errors), errors)

    def refresh_review(self):
        self.case["reviews"][0]["snapshot_sha256"] = digest(encoded(self.case["revisions"][-1]["claim_snapshots"]))

    def test_real_review_and_caveat_clarification_preserve_authentic_baseline(self):
        self.assertEqual(validate_registry(self.data), [])
        self.assertEqual(validate_repository_sources(self.data), [])

    def test_forged_historical_snapshot_is_rejected_against_git(self):
        self.case["revisions"][0]["claim_snapshots"][0]["text"] += " Forged."
        self.assertTrue(any("differs from preserved repository claims" in error for error in validate_repository_sources(self.data)))

    def test_nonexistent_import_commit_fails_closed(self):
        self.case["revisions"][0]["source_commit"] = "0" * 40
        self.assertTrue(any("could not be verified" in error for error in validate_repository_sources(self.data)))

    def test_historical_import_does_not_receive_retroactive_review(self):
        self.case["revisions"][0]["review_ids"] = ["review-period"]
        self.rejects("cannot invent retrospective review")

    def test_ai_review_cannot_claim_human_approval(self):
        self.case["reviews"][0]["decision"] = "approved_for_publication"
        self.rejects("misrepresents reviewer type")
        self.case["reviews"][0].update(decision="reviewed", reviewer_type="human")
        self.rejects("misrepresents reviewer type")

    def test_changed_snapshot_invalidates_old_review(self):
        self.case["revisions"][-1]["claim_snapshots"][-1]["locator"] += " Unreviewed locator."
        self.rejects("review snapshot fingerprint mismatch")

    def test_classification_change_requires_new_review_and_current_snapshot(self):
        self.case["claims"][-1]["kind"] = "allegation"
        self.rejects("current claim differs from latest revision")
        self.case["claims"][-1]["kind"] = "report"
        self.case["revisions"][-1]["claim_snapshots"][-1]["kind"] = "allegation"
        self.rejects("review snapshot fingerprint mismatch")

    def test_snapshot_classification_must_be_an_allowed_claim_kind(self):
        self.case["revisions"][-1]["claim_snapshots"][-1]["kind"] = "verdict"
        self.refresh_review()
        self.rejects("unsupported claim snapshot kind")

    def test_review_cannot_be_reused_for_another_revision(self):
        self.case["reviews"][0]["revision_id"] = "published-baseline"
        self.rejects("reuses a review of another snapshot")
        self.rejects("historical import cannot receive retroactive approval")

    def test_latest_claim_caveat_and_citations_must_match_snapshot(self):
        self.case["claims"][-1]["caveat"] = "Unsupported certainty."
        self.rejects("current claim differs from latest revision")
        self.case["claims"][-1]["source_ids"] = [self.case["sources"][0]["id"]]
        self.rejects("current claim differs from latest revision")

    def test_changed_caveat_requires_visible_change_record(self):
        self.case["corrections"] = []
        self.rejects("changed claim lacks correction or update record")

    def test_correction_record_cannot_hide_caveat_or_locator_change(self):
        self.case["corrections"][0]["after_snapshot"]["caveat"] = "Rewritten history."
        self.rejects("change record provenance differs")

    def test_unchanged_claim_cannot_be_presented_as_a_correction(self):
        unchanged = self.case["revisions"][0]["claim_snapshots"][0]
        correction = self.case["corrections"][0]
        correction.update(claim_id=unchanged["claim_id"], before=unchanged["text"], after=unchanged["text"], before_snapshot=unchanged, after_snapshot=unchanged)
        self.rejects("correction text differs from preserved revisions")

    def test_added_claim_requires_recorded_update(self):
        added = copy.deepcopy(self.case["claims"][-1])
        added["id"] = "new-follow-up"
        self.case["claims"].append(added)
        self.case["evidence_links"].append({"claim_id": added["id"], "source_id": added["source_ids"][0], "relationship": "supports", "rationale": "New source comparison."})
        snapshot = claim_snapshot(added)
        self.case["revisions"][-1]["claim_snapshots"].append(snapshot)
        self.refresh_review()
        self.rejects("changed claim lacks correction or update record")
        self.case["corrections"].append({"id": "added-follow-up", "kind": "update", "from_revision_id": "published-baseline", "to_revision_id": "period-clarification", "claim_id": added["id"], "cause": "New source comparison.", "before": None, "after": added["text"], "before_status": None, "after_status": added["status"], "before_snapshot": None, "after_snapshot": snapshot, "source_ids": added["source_ids"], "recorded_at": "2026-10-17T21:01:00Z"})
        self.assertEqual(validate_registry(self.data), [])

    def test_full_snapshot_fields_and_timezone_timestamps_required(self):
        del self.case["revisions"][-1]["claim_snapshots"][-1]["locator"]
        self.case["reviews"][0]["reviewed_at"] = "2026-10-17T21:00:30"
        self.rejects("complete claim snapshot fields")
        self.rejects("timezone-qualified ISO timestamp")

    def test_review_after_publication_is_rejected(self):
        self.case["reviews"][0]["reviewed_at"] = "2026-10-17T21:02:00Z"
        self.rejects("review must precede publication")

    def test_malformed_history_shapes_fail_closed(self):
        self.case["reviews"][0]["kind"] = []
        self.case["reviews"][0]["revision_id"] = []
        self.case["revisions"][-1]["review_ids"] = None
        self.case["corrections"][0]["claim_id"] = []
        self.case["revisions"][-1]["claim_snapshots"][-1]["status"] = {}
        self.assertTrue(validate_registry(self.data))

    def comparison(self):
        source_id = self.case["sources"][-1]["id"]
        self.case["comparisons"] = [{"id": "winter-cash", "metric": "Winter cash", "assessment": "Delivery not verified", "note": "Different reporting periods must not be divided.", "target": {"value": 263000, "unit": "households", "source_id": source_id, "locator": "Plan p. 1", "period": "Winter 2024–2025"}, "actual": {"value": None, "unit": "households", "source_id": source_id, "locator": "Plan p. 1 has targets only", "period": "Winter 2024–2025"}}]
        return self.case["comparisons"][0]

    def test_unknown_delivery_remains_null(self):
        self.comparison()
        self.assertEqual(validate_registry(self.data), [])

    def test_comparison_followup_accepts_attributed_context(self):
        comparison = self.comparison()
        comparison["followup"] = {"summary": "The later source explains its reporting period, not why assistance fell short.", "source_ids": [self.case["sources"][-1]["id"]]}
        self.assertEqual(validate_registry(self.data), [])

    def test_comparison_followup_rejects_missing_or_unknown_sources(self):
        comparison = self.comparison()
        for cited in ([], ["unknown"], [["malformed"]], "source-id", None):
            comparison["followup"] = {"summary": "Sourced follow-up context.", "source_ids": cited}
            self.rejects("comparison followup requires known source IDs")

    def test_comparison_followup_rejects_malformed_or_empty_content(self):
        comparison = self.comparison()
        for followup in (None, [], "context"):
            comparison["followup"] = followup
            self.rejects("comparison followup must be an object")
        for summary in ("", "   ", [], None):
            comparison["followup"] = {"summary": summary, "source_ids": [self.case["sources"][-1]["id"]]}
            self.rejects("comparison followup summary must be nonempty text")
        comparison["followup"] = {"summary": "Sourced context.", "source_ids": [self.case["sources"][-1]["id"]], "verdict": "unreviewed"}
        self.rejects("comparison followup requires summary and source_ids only")

    def test_comparison_rejects_unbounded_or_mismatched_calculation(self):
        comparison = self.comparison()
        for bad in (True, -1, float("nan"), float("inf")):
            comparison["actual"]["value"] = bad
            self.rejects("nonnegative finite number or null")
        comparison["actual"].update(value=550000, unit="people")
        comparison["calculation"] = "Incomparable counts."
        self.rejects("calculation requires matching units")
        comparison["actual"]["source_id"] = "unknown"
        self.rejects("comparison cites an unknown source")


if __name__ == "__main__":
    unittest.main()
