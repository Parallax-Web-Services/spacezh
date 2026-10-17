"""Public fixture validation and deterministic publication. No network or ingestion."""
from __future__ import annotations

import hashlib
import copy
import json
import math
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/relay/cases.json"
PUBLIC = ROOT / "public/relay/data"
SCHEMA = "spacezh.relay.prototype.v1"


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def validate_registry(data):
    """Validate evidence references and explicitly attributed publication history.

    Labels and fingerprints establish neither factual truth nor human approval.
    Real review records identify their method and bind to exact claim snapshots.
    """
    errors = []

    def require(condition, message):
        if not condition:
            errors.append(message)

    def index(records, label):
        if not isinstance(records, list):
            errors.append(label + ": expected a list")
            return {}
        result = {}
        for record in records:
            if not isinstance(record, dict) or not isinstance(record.get("id"), str) or not record["id"]:
                errors.append(label + ": missing record ID")
                continue
            require(record["id"] not in result, label + ": duplicate ID " + record["id"])
            result[record["id"]] = record
        return result

    if not isinstance(data, dict):
        return ["registry: expected an object"]
    require(data.get("schema_version") == SCHEMA, "registry: unsupported schema")
    require(data.get("prototype") is True, "registry: prototype disclosure required")
    require(data.get("confidential_intake") is False, "registry: confidential intake is excluded")
    require(data.get("trusted_operational_feed") is False, "registry: operational feed is excluded")
    cases = index(data.get("cases"), "cases")
    require(bool(cases), "registry: at least one case required")
    for case_id, case in cases.items():
        prefix = case_id + ": "
        synthetic = case.get("kind") == "synthetic"
        require(case.get("kind") in {"synthetic", "public_snapshot", "public_case"}, prefix + "unsupported case kind")
        require(case.get("visibility") == "public", prefix + "only public fixtures may be exported")
        typed = True
        for field in ("title", "summary", "status", "boundary_note", "publication_note"):
            valid = isinstance(case.get(field), str) and bool(case[field])
            require(valid, prefix + "missing or invalid text field: " + field)
            typed = typed and valid
        for field in ("tags", "source_independence_notes"):
            valid = isinstance(case.get(field), list) and all(isinstance(item, str) for item in case[field])
            require(valid, prefix + "missing or invalid text list: " + field)
            typed = typed and valid
        for field in ("sources", "claims", "artifacts", "reviews", "revisions", "corrections", "evidence_links", "timeline"):
            valid = isinstance(case.get(field), list) and all(isinstance(item, dict) for item in case[field])
            require(valid, prefix + "missing or invalid record list: " + field)
            typed = typed and valid
        provenance = case.get("provenance")
        valid = isinstance(provenance, dict) and all(isinstance(provenance.get(field), str) and provenance[field] for field in ("label", "url", "note"))
        require(valid, prefix + "missing or invalid provenance")
        typed = typed and valid
        if not typed:
            continue
        provenance_url = provenance["url"]
        require(provenance_url.startswith("https://") or (provenance_url.startswith("/") and not provenance_url.startswith("//")) or provenance_url == "./data/cases.json", prefix + "unsafe provenance URL")
        sources = index(case.get("sources", []), prefix + "sources")
        claims = index(case.get("claims", []), prefix + "claims")
        artifacts = index(case.get("artifacts", []), prefix + "artifacts")
        reviews = index(case.get("reviews", []), prefix + "reviews")
        revisions = index(case.get("revisions", []), prefix + "revisions")
        corrections = index(case.get("corrections", []), prefix + "corrections")
        require(bool(sources) and bool(claims), prefix + "sources and claims required")
        for source_id, source in sources.items():
            url = source.get("url", "")
            safe_external = isinstance(url, str) and urlsplit(url).scheme == "https" and bool(urlsplit(url).netloc) and not urlsplit(url).username and not urlsplit(url).password
            safe_artifact = synthetic and isinstance(url, str) and url.startswith("#artifact-") and url[len("#artifact-"):] in artifacts
            require(safe_external or safe_artifact, prefix + "unsafe or missing source URL: " + source_id)
            for field in ("title", "publisher", "byline", "published_date", "source_type", "notes", "rights"):
                require(isinstance(source.get(field), str) and bool(source[field]), prefix + "source " + field + " required: " + source_id)
            review = source.get("verification")
            if review is not None:
                require(isinstance(review, dict) and review.get("status") in {"content_reviewed", "not_accessible"}, prefix + "invalid source review status: " + source_id)
                if isinstance(review, dict):
                    require(all(isinstance(review.get(field), str) and review[field] for field in ("checked_at", "method", "note", "locator")), prefix + "source review provenance required: " + source_id)
            for field in ("retrieval", "alternate_retrieval"):
                receipt = source.get(field)
                if receipt is None:
                    continue
                require(isinstance(receipt, dict) and receipt.get("status") in {"retrieved", "unavailable"}, prefix + "invalid retrieval status: " + source_id)
                if not isinstance(receipt, dict):
                    continue
                require(bool(receipt.get("retrieved_at")) and receipt.get("method") == "public_https_get", prefix + "retrieval time/method required: " + source_id)
                if receipt.get("status") == "retrieved":
                    require(receipt.get("http_status") == 200 and isinstance(receipt.get("bytes"), int) and receipt["bytes"] >= 0 and isinstance(receipt.get("body_sha256"), str) and len(receipt["body_sha256"]) == 64, prefix + "retrieved response fingerprint required: " + source_id)
                else:
                    require(receipt.get("body_sha256") is None, prefix + "unavailable response cannot claim a body fingerprint: " + source_id)
        for artifact_id, artifact in artifacts.items():
            require(synthetic, prefix + "public snapshots must not copy publisher artifacts")
            require(artifact.get("source_id") in sources, prefix + "unknown artifact source: " + artifact_id)
            content = artifact.get("content")
            require(isinstance(content, str) and bool(content), prefix + "artifact content required: " + artifact_id)
            require(bool(artifact.get("rights")), prefix + "artifact rights required: " + artifact_id)
            if isinstance(content, str):
                require(artifact.get("sha256") == digest(content.encode("utf-8")), prefix + "artifact fingerprint mismatch: " + artifact_id)
        for claim_id, claim in claims.items():
            require(claim.get("kind") in {"observation", "report", "allegation", "denial", "inference"}, prefix + "unsupported claim kind: " + claim_id)
            require(claim.get("status") in {"supported", "disputed", "unresolved"}, prefix + "unsupported claim status: " + claim_id)
            require(bool(claim.get("text")) and bool(claim.get("caveat")), prefix + "claim text and caveat required: " + claim_id)
            cited = claim.get("source_ids", [])
            require(isinstance(cited, list) and bool(cited) and all(isinstance(s, str) and s in sources for s in cited), prefix + "uncited or unknown claim source: " + claim_id)
        links = case.get("evidence_links", [])
        require(isinstance(links, list), prefix + "evidence links must be a list")
        for link in links if isinstance(links, list) else []:
            if not isinstance(link, dict):
                errors.append(prefix + "invalid evidence link")
                continue
            claim = claims.get(link.get("claim_id"), {})
            require(bool(claim) and link.get("source_id") in sources, prefix + "unknown evidence link reference")
            require(link.get("source_id") in claim.get("source_ids", []), prefix + "evidence source is absent from claim citations")
            require(link.get("relationship") in {"supports", "contradicts", "ambiguous"}, prefix + "unsupported evidence relationship")
            require(bool(link.get("rationale")), prefix + "evidence rationale required")
        for claim_id in claims:
            require(any(isinstance(link, dict) and link.get("claim_id") == claim_id for link in (links if isinstance(links, list) else [])), prefix + "claim has no evidence relationship: " + claim_id)
        errors.extend(validate_case_history(case, sources, claims, reviews, revisions, corrections))
        comparisons = case.get("comparisons", [])
        comparison_ids = set()
        require(isinstance(comparisons, list), prefix + "comparisons must be a list")
        for comparison in comparisons if isinstance(comparisons, list) else []:
            if not isinstance(comparison, dict):
                errors.append(prefix + "invalid comparison record")
                continue
            comparison_id = comparison.get("id")
            valid_id = isinstance(comparison_id, str) and bool(comparison_id)
            require(valid_id and comparison_id not in comparison_ids, prefix + "comparison requires a unique ID")
            if valid_id:
                comparison_ids.add(comparison_id)
            for field in ("metric", "assessment", "note"):
                require(isinstance(comparison.get(field), str) and bool(comparison[field].strip()), prefix + "comparison " + field + " required")
            if "followup" in comparison:
                followup = comparison["followup"]
                require(isinstance(followup, dict), prefix + "comparison followup must be an object")
                if isinstance(followup, dict):
                    require(set(followup) == {"summary", "source_ids"}, prefix + "comparison followup requires summary and source_ids only")
                    require(isinstance(followup.get("summary"), str) and bool(followup["summary"].strip()), prefix + "comparison followup summary must be nonempty text")
                    cited = followup.get("source_ids")
                    require(isinstance(cited, list) and bool(cited) and all(isinstance(source_id, str) and source_id in sources for source_id in cited), prefix + "comparison followup requires known source IDs")
            for side in ("target", "actual"):
                measure = comparison.get(side)
                require(isinstance(measure, dict), prefix + "comparison " + side + " must be an object")
                if not isinstance(measure, dict):
                    continue
                value = measure.get("value")
                require("value" in measure and (value is None or (not isinstance(value, bool) and (isinstance(value, int) or (isinstance(value, float) and math.isfinite(value))) and value >= 0)), prefix + "comparison value must be a nonnegative finite number or null")
                for field in ("unit", "source_id", "locator", "period"):
                    require(isinstance(measure.get(field), str) and bool(measure[field].strip()), prefix + "comparison " + side + " " + field + " required")
                require(isinstance(measure.get("source_id"), str) and measure["source_id"] in sources, prefix + "comparison cites an unknown source")
            if "calculation" in comparison:
                require(isinstance(comparison["calculation"], str) and bool(comparison["calculation"].strip()), prefix + "comparison calculation must be text")
                target, actual = comparison.get("target"), comparison.get("actual")
                if isinstance(target, dict) and isinstance(actual, dict):
                    require(target.get("unit") == actual.get("unit"), prefix + "comparison calculation requires matching units")
        questions = case.get("open_questions", [])
        require(isinstance(questions, list), prefix + "verification queue must be a list")
        for question in questions if isinstance(questions, list) else []:
            require(isinstance(question, dict) and all(isinstance(question.get(field), str) and question[field] for field in ("question", "why_it_matters", "needed_evidence")), prefix + "invalid verification question")
            if isinstance(question, dict):
                cited = question.get("source_ids", [])
                require(isinstance(cited, list) and bool(cited) and all(isinstance(item, str) and item in sources for item in cited), prefix + "unknown verification question source")
        for event in case["timeline"]:
            for field in ("date", "label", "detail"):
                require(isinstance(event.get(field), str) and bool(event[field]), prefix + "timeline " + field + " required")
            cited = event.get("source_ids", [])
            require(isinstance(cited, list) and all(isinstance(item, str) and item in sources for item in cited), prefix + "unknown timeline source")
            if event.get("review_id") is not None:
                require(event["review_id"] in reviews, prefix + "unknown timeline review")
            if event.get("revision_id") is not None:
                require(event["revision_id"] in revisions, prefix + "unknown timeline revision")
    return errors



SNAPSHOT_FIELDS = ("kind", "text", "status", "caveat", "source_ids", "locator")


def claim_snapshot(claim):
    """The complete reviewable claim state, including citation and caveat changes."""
    return {"claim_id": claim.get("id"), **{field: copy.deepcopy(claim.get(field)) for field in SNAPSHOT_FIELDS}}


def _timestamp(value):
    if not isinstance(value, str) or not re.match(r"^\d{4}-\d{2}-\d{2}T", value):
        return None
    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return result.astimezone(timezone.utc) if result.tzinfo is not None else None
    except ValueError:
        return None


def validate_case_history(case, sources, claims, reviews, revisions, corrections):
    """Keep simulated exercises separate from attributable, exact-snapshot reviews."""
    errors = []
    prefix = case["id"] + ": "
    synthetic = case.get("kind") == "synthetic"

    def require(condition, message):
        if not condition:
            errors.append(prefix + message)

    def known(value, records):
        return isinstance(value, str) and value in records

    if case.get("kind") == "public_snapshot":
        require(not reviews and not revisions and not corrections, "public snapshot must not invent review or publication history")
        return errors

    for review_id, review in reviews.items():
        if synthetic:
            require(review.get("kind") == "simulated", "review must be explicitly simulated: " + review_id)
            require(review.get("decision") == "approved_for_demo", "unapproved simulated review: " + review_id)
            fields = ("reviewer", "rationale", "conflicts")
        else:
            kind = review.get("kind")
            expected = {"ai_assisted": ("ai", "reviewed"), "human": ("human", "approved_for_publication")}.get(kind) if isinstance(kind, str) else None
            require(expected is not None, "real review kind must identify AI assistance or a human: " + review_id)
            require(expected is not None and (review.get("reviewer_type"), review.get("decision")) == expected, "review attribution or decision misrepresents reviewer type: " + review_id)
            fields = ("reviewer", "rationale", "conflicts", "method", "scope")
            require(_timestamp(review.get("reviewed_at")) is not None, "review requires a timezone-qualified ISO timestamp: " + review_id)
            revision_id = review.get("revision_id")
            require(known(revision_id, revisions), "review references an unknown revision: " + review_id)
            if known(revision_id, revisions):
                revision = revisions[revision_id]
                linked = revision.get("review_ids")
                require(isinstance(linked, list) and review_id in linked, "review must be linked by its exact revision: " + review_id)
                require(review.get("snapshot_sha256") == digest(encoded(revision.get("claim_snapshots"))), "review snapshot fingerprint mismatch: " + review_id)
                require(not revision.get("historical_import"), "historical import cannot receive retroactive approval: " + review_id)
                reviewed_at, published_at = _timestamp(review.get("reviewed_at")), _timestamp(revision.get("published_at"))
                require(reviewed_at is not None and published_at is not None and reviewed_at <= published_at, "review must precede publication: " + review_id)
        for field in fields:
            require(isinstance(review.get(field), str) and bool(review[field].strip()), "review " + field + " required: " + review_id)

    previous_id, previous_time, previous_recorded_time = None, None, None
    snapshots = {}
    for revision_id, revision in revisions.items():
        require(revision.get("parent_revision_id") == previous_id, "broken revision chain: " + revision_id)
        published_at = revision.get("published_at")
        if synthetic:
            valid_time = isinstance(published_at, str) and bool(published_at)
            require(valid_time and (previous_time is None or published_at >= previous_time), "revision dates out of order: " + revision_id)
            if valid_time:
                previous_time = published_at
        else:
            require("historical_import" not in revision or isinstance(revision["historical_import"], bool), "historical_import must be a boolean: " + revision_id)
            published_time, recorded_time = _timestamp(published_at), _timestamp(revision.get("recorded_at"))
            require(published_time is not None and (previous_time is None or published_time >= previous_time), "revision dates out of order or invalid: " + revision_id)
            require(recorded_time is not None, "revision requires a timezone-qualified recorded_at: " + revision_id)
            require(recorded_time is not None and (previous_recorded_time is None or recorded_time >= previous_recorded_time), "revision recording dates out of order: " + revision_id)
            if recorded_time is not None:
                previous_recorded_time = recorded_time
            if published_time is not None:
                previous_time = published_time
            require(published_time is not None and recorded_time is not None and recorded_time >= published_time, "revision recorded_at precedes publication: " + revision_id)
        review_ids = revision.get("review_ids")
        valid_reviews = isinstance(review_ids, list) and all(known(item, reviews) for item in review_ids) and len(set(review_ids)) == len(review_ids)
        if not synthetic and revision.get("historical_import") is True:
            require(previous_id is None, "historical import must be the first revision: " + revision_id)
            require(review_ids == [], "historical import cannot invent retrospective review: " + revision_id)
            require(isinstance(revision.get("source_commit"), str) and re.fullmatch(r"[0-9a-f]{40}", revision["source_commit"]) is not None and revision.get("source_path") == "data/relay/cases.json", "historical import requires an exact repository commit and canonical path: " + revision_id)
            require(isinstance(revision.get("import_note"), str) and bool(revision["import_note"].strip()), "historical import note required: " + revision_id)
        else:
            require(valid_reviews and bool(review_ids), ("revision missing simulated approval: " if synthetic else "revision missing exact-snapshot review: ") + revision_id)
            if not synthetic:
                require(revision.get("publication_basis") == "user_authorized", "real revision publication basis required: " + revision_id)
                for review_id in review_ids if isinstance(review_ids, list) else []:
                    if known(review_id, reviews):
                        require(reviews[review_id].get("revision_id") == revision_id, "revision reuses a review of another snapshot: " + revision_id)
        items = revision.get("claim_snapshots")
        snapshot = {}
        if isinstance(items, list):
            for item in items:
                if isinstance(item, dict) and isinstance(item.get("claim_id"), str) and item["claim_id"]:
                    require(item["claim_id"] not in snapshot, "duplicate or invalid claim snapshot: " + revision_id)
                    snapshot[item["claim_id"]] = item
        require(isinstance(items, list) and len(snapshot) == len(items), "duplicate or invalid claim snapshot: " + revision_id)
        require(bool(snapshot) and set(snapshot).issubset(claims), "revision contains unknown claims: " + revision_id)
        require(isinstance(revision.get("change_note"), str) and bool(revision["change_note"].strip()), "revision change note required: " + revision_id)
        for claim_id, item in snapshot.items():
            require(isinstance(item.get("text"), str) and bool(item["text"]) and item.get("status") in ("supported", "disputed", "unresolved"), "invalid claim snapshot: " + claim_id)
            if not synthetic:
                require(item.get("kind") in ("observation", "report", "allegation", "denial", "inference"), "unsupported claim snapshot kind: " + claim_id)
                require(set(item) == {"claim_id", *SNAPSHOT_FIELDS}, "real revision must preserve complete claim snapshot fields: " + claim_id)
                for field in ("caveat", "locator"):
                    require(isinstance(item.get(field), str) and bool(item[field].strip()), "claim snapshot " + field + " required: " + claim_id)
                cited = item.get("source_ids")
                require(isinstance(cited, list) and bool(cited) and all(known(source_id, sources) for source_id in cited), "claim snapshot has unknown citation: " + claim_id)
        snapshots[revision_id] = snapshot
        previous_id = revision_id
    if synthetic:
        require(len(revisions) >= 2 and bool(corrections), "complete demo needs original and corrected revisions")
    else:
        require(bool(revisions) or (not reviews and not corrections), "real review or correction requires a revision")
    if previous_id:
        require(set(snapshots[previous_id]) == set(claims), "latest revision must snapshot every current claim")
        for claim_id, claim in claims.items():
            item = snapshots[previous_id].get(claim_id, {})
            expected = {"text": claim.get("text"), "status": claim.get("status")} if synthetic else claim_snapshot(claim)
            require(all(item.get(field) == value for field, value in expected.items()), "current claim differs from latest revision: " + claim_id)
    for correction_id, correction in corrections.items():
        old, new, claim_id = (correction.get(field) for field in ("from_revision_id", "to_revision_id", "claim_id"))
        references_valid = known(old, revisions) and known(new, revisions) and known(claim_id, claims)
        require(references_valid, "unknown correction reference: " + correction_id)
        if not references_valid:
            continue
        require(revisions[new].get("parent_revision_id") == old, "correction must link adjacent revisions: " + correction_id)
        require(isinstance(correction.get("cause"), str) and bool(correction["cause"].strip()), "correction cause required: " + correction_id)
        cited = correction.get("source_ids")
        require(isinstance(cited, list) and bool(cited) and all(known(item, sources) for item in cited), "unknown or missing correction source: " + correction_id)
        before_item, after_item = snapshots.get(old, {}).get(claim_id), snapshots.get(new, {}).get(claim_id)
        before, after = (item.get("text") if item else None for item in (before_item, after_item))
        old_status, new_status = (item.get("status") if item else None for item in (before_item, after_item))
        changed = before != after or old_status != new_status if synthetic else before_item != after_item
        require(changed and correction.get("before") == before and correction.get("after") == after, "correction text differs from preserved revisions: " + correction_id)
        if not synthetic or old_status != new_status:
            require(correction.get("before_status") == old_status and correction.get("after_status") == new_status, "correction status differs from preserved revisions: " + correction_id)
        if not synthetic:
            require(all(field in correction for field in ("before", "after", "before_status", "after_status", "before_snapshot", "after_snapshot")), "real change record must preserve explicit before/after fields: " + correction_id)
            require(isinstance(correction.get("kind"), str) and correction["kind"] in {"correction", "update", "clarification"}, "real change record must classify correction, update, or clarification: " + correction_id)
            require(correction.get("before_snapshot") == before_item and correction.get("after_snapshot") == after_item, "change record provenance differs from preserved revisions: " + correction_id)
            recorded_at = _timestamp(correction.get("recorded_at"))
            revision_at = _timestamp(revisions[new].get("recorded_at"))
            require(recorded_at is not None and revision_at is not None and recorded_at >= revision_at, "change record requires a timestamp after its revision was recorded: " + correction_id)
            if before_item is None or after_item is None:
                require(correction.get("kind") == "update", "added or removed claim must be recorded as an update: " + correction_id)
    for revision_id, revision in revisions.items():
        parent = revision.get("parent_revision_id")
        if known(parent, snapshots):
            old, new = snapshots[parent], snapshots[revision_id]
            for claim_id in set(old) | set(new):
                if old.get(claim_id) != new.get(claim_id):
                    require(any(c.get("claim_id") == claim_id and c.get("from_revision_id") == parent and c.get("to_revision_id") == revision_id for c in corrections.values()), "changed claim lacks correction or update record: " + claim_id)
    return errors


def validate_public_snapshot(case, original):
    """The public snapshot must preserve the existing dated editorial register."""
    errors = []
    if case.get("id") != original.get("record_id") or case.get("title") != original.get("title"):
        errors.append("public snapshot identity differs from editorial register")
    sources = {item["id"]: item for item in case["sources"]}
    expected_sources = {item["id"]: item for item in original["sources"]}
    if set(sources) != set(expected_sources):
        errors.append("public snapshot source set differs from editorial register")
    for source_id, source in expected_sources.items():
        if any(sources.get(source_id, {}).get(field) != value for field, value in source.items()):
            errors.append("public snapshot altered original source metadata: " + source_id)
    claims = {item["id"]: item for item in case["claims"]}
    expected_claims = {item["id"]: item for item in original["claims"]}
    if set(claims) != set(expected_claims):
        errors.append("public snapshot claim set differs from editorial register")
    fields = {"claim": "text", "evidence_class": "original_evidence_class", "sourcing": "sourcing", "caveat": "caveat", "source_ids": "source_ids"}
    for claim_id, claim in expected_claims.items():
        if any(claims.get(claim_id, {}).get(target) != claim.get(source) for source, target in fields.items()):
            errors.append("public snapshot altered original claim or caveat: " + claim_id)
    if case.get("source_independence_notes") != original.get("source_independence_notes"):
        errors.append("public snapshot altered source independence notes")
    for source, target in (("date_first_published", "original_date_first_published"), ("date_reviewed", "original_date_reviewed"), ("publication_status", "original_publication_status")):
        if case.get(target) != original.get(source):
            errors.append("public snapshot altered original publication metadata")
    return errors


def validate_repository_sources(data):
    errors = []
    source_path = "data/evidence/starshield-restrictions-2026-10-16.json"
    for case in data["cases"]:
        if case["kind"] == "public_snapshot":
            if case.get("source_record") != source_path:
                errors.append("public snapshot has an unknown canonical editorial register")
                continue
            original = json.loads((ROOT / source_path).read_text(encoding="utf-8"))
            errors.extend(validate_public_snapshot(case, original))
        if case["kind"] != "public_case":
            continue
        for revision in case.get("revisions", []):
            if revision.get("historical_import") is not True:
                continue
            commit, path = revision.get("source_commit"), revision.get("source_path")
            if not isinstance(commit, str) or re.fullmatch(r"[0-9a-f]{40}", commit) is None or path != "data/relay/cases.json":
                errors.append(case["id"] + ": historical import repository reference is invalid")
                continue
            try:
                result = subprocess.run(["git", "show", commit + ":" + path], cwd=ROOT, check=True, capture_output=True, timeout=15)
                original = json.loads(result.stdout.decode("utf-8"))
                matches = [record for record in original["cases"] if record.get("id") == case["id"] and record.get("kind") == "public_case"]
                if len(matches) != 1 or revision.get("claim_snapshots") != [claim_snapshot(claim) for claim in matches[0]["claims"]]:
                    errors.append(case["id"] + ": historical import differs from preserved repository claims")
            except (OSError, subprocess.SubprocessError, ValueError, KeyError, TypeError, AttributeError):
                errors.append(case["id"] + ": historical import commit could not be verified from local repository history")
    return errors


def attach_receipts(data, audit):
    data = copy.deepcopy(data)
    latest = {}
    for run in audit.get("runs", []):
        for receipt in run.get("receipts", []):
            latest[receipt["requested_url"]] = receipt
    for case in data["cases"]:
        for source in case["sources"]:
            if source["url"] in latest:
                source["retrieval"] = latest[source["url"]]
            alternate = source.get("alternate_url") or source.get("verification", {}).get("reviewed_url")
            if alternate and alternate != source["url"] and alternate in latest:
                source["alternate_retrieval"] = latest[alternate]
    data["retrieval_runs"] = audit.get("runs", [])
    if audit.get("runs"):
        data["source_access_audit"] = {"completed_at": audit["runs"][-1]["completed_at"], "run_count": len(audit["runs"])}
    return data


def validate_publication_boundary(data):
    return ["synthetic cases are test-only and cannot enter the public registry"] if any(case.get("kind") == "synthetic" for case in data["cases"]) else []


def publication(data):
    payload = encoded(data)
    receipt_bytes = encoded({"schema_version": "spacezh.relay.retrievals.v1", "runs": data.get("retrieval_runs", [])})
    manifest = {"schema_version": SCHEMA, "source_path": "data/relay/cases.json", "dataset_sha256": digest(payload), "retrieval_log_sha256": digest(receipt_bytes), "case_count": len(data["cases"]), "integrity_note": "Dataset hashes identify published bytes. Source response hashes identify bytes fetched at the recorded time; source bodies are not archived. Neither proves factual truth or editorial approval."}
    return {"cases.json": payload, "retrievals.json": receipt_bytes, "manifest.json": encoded(manifest)}


def load_source():
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    audit_path = ROOT / "data/relay/retrievals.json"
    if audit_path.exists():
        data = attach_receipts(data, json.loads(audit_path.read_text(encoding="utf-8")))
    return data
