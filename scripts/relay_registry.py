"""Public fixture validation and deterministic publication. No network or ingestion."""
from __future__ import annotations

import hashlib
import copy
import json
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
    """Validate provenance references and the simulated publication lifecycle.

    Labels and fingerprints cannot establish factual truth, publication consent,
    or confidentiality. A human must review every new fixture before committing it.
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
            require(isinstance(cited, list) and bool(cited) and all(s in sources for s in cited), prefix + "uncited or unknown claim source: " + claim_id)
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
        if not synthetic:
            require(not reviews and not revisions and not corrections, prefix + "public snapshot must not invent review or publication history")
            require(bool(case.get("provenance", {}).get("url")), prefix + "public snapshot provenance required")
        for review_id, review in reviews.items():
            require(synthetic and review.get("kind") == "simulated", prefix + "review must be explicitly simulated: " + review_id)
            require(review.get("decision") == "approved_for_demo", prefix + "unapproved simulated review: " + review_id)
            for field in ("reviewer", "rationale", "conflicts"):
                require(bool(review.get(field)), prefix + "review " + field + " required: " + review_id)
        previous_id = None
        previous_time = ""
        snapshots = {}
        for revision_id, revision in revisions.items():
            require(revision.get("parent_revision_id") == previous_id, prefix + "broken revision chain: " + revision_id)
            published_at = revision.get("published_at", "")
            require(bool(published_at) and published_at >= previous_time, prefix + "revision dates out of order: " + revision_id)
            review_ids = revision.get("review_ids", [])
            require(isinstance(review_ids, list) and bool(review_ids) and all(r in reviews for r in review_ids), prefix + "revision missing simulated approval: " + revision_id)
            items = revision.get("claim_snapshots", [])
            snapshot = {s.get("claim_id"): s for s in items if isinstance(s, dict)} if isinstance(items, list) else {}
            require(bool(snapshot) and set(snapshot).issubset(claims), prefix + "revision contains unknown claims: " + revision_id)
            require(bool(revision.get("change_note")), prefix + "revision change note required: " + revision_id)
            require(isinstance(items, list) and len(snapshot) == len(items), prefix + "duplicate or invalid claim snapshot: " + revision_id)
            for claim_id, item in snapshot.items():
                require(bool(item.get("text")) and item.get("status") in {"supported", "disputed", "unresolved"}, prefix + "invalid claim snapshot: " + str(claim_id))
            snapshots[revision_id] = snapshot
            previous_id, previous_time = revision_id, published_at
        if synthetic:
            require(len(revisions) >= 2 and bool(corrections), prefix + "complete demo needs original and corrected revisions")
        if previous_id:
            require(set(snapshots[previous_id]) == set(claims), prefix + "latest revision must snapshot every current claim")
            for claim_id, claim in claims.items():
                item = snapshots[previous_id].get(claim_id, {})
                require(item.get("text") == claim.get("text") and item.get("status") == claim.get("status"), prefix + "current claim differs from latest revision: " + claim_id)
        for correction_id, correction in corrections.items():
            old = correction.get("from_revision_id")
            new = correction.get("to_revision_id")
            claim_id = correction.get("claim_id")
            require(old in revisions and new in revisions and claim_id in claims, prefix + "unknown correction reference: " + correction_id)
            require(revisions.get(new, {}).get("parent_revision_id") == old, prefix + "correction must link adjacent revisions: " + correction_id)
            require(bool(correction.get("cause")), prefix + "correction cause required: " + correction_id)
            cited = correction.get("source_ids")
            require(isinstance(cited, list) and bool(cited) and all(isinstance(item, str) and item in sources for item in cited), prefix + "unknown or missing correction source: " + correction_id)
            before = snapshots.get(old, {}).get(claim_id, {}).get("text")
            after = snapshots.get(new, {}).get(claim_id, {}).get("text")
            old_status = snapshots.get(old, {}).get(claim_id, {}).get("status")
            new_status = snapshots.get(new, {}).get(claim_id, {}).get("status")
            changed = before != after or old_status != new_status
            require(changed and correction.get("before") == before and correction.get("after") == after, prefix + "correction text differs from preserved revisions: " + correction_id)
            if old_status != new_status:
                require(correction.get("before_status") == old_status and correction.get("after_status") == new_status, prefix + "correction status differs from preserved revisions: " + correction_id)
        questions = case.get("open_questions", [])
        require(isinstance(questions, list), prefix + "verification queue must be a list")
        for question in questions if isinstance(questions, list) else []:
            require(isinstance(question, dict) and all(isinstance(question.get(field), str) and question[field] for field in ("question", "why_it_matters", "needed_evidence")), prefix + "invalid verification question")
            if isinstance(question, dict):
                cited = question.get("source_ids", [])
                require(isinstance(cited, list) and bool(cited) and all(item in sources for item in cited), prefix + "unknown verification question source")
        for event in case["timeline"]:
            for field in ("date", "label", "detail"):
                require(isinstance(event.get(field), str) and bool(event[field]), prefix + "timeline " + field + " required")
            cited = event.get("source_ids", [])
            require(isinstance(cited, list) and all(isinstance(item, str) and item in sources for item in cited), prefix + "unknown timeline source")
            if event.get("review_id") is not None:
                require(event["review_id"] in reviews, prefix + "unknown timeline review")
            if event.get("revision_id") is not None:
                require(event["revision_id"] in revisions, prefix + "unknown timeline revision")
        for revision_id, revision in revisions.items():
            parent = revision.get("parent_revision_id")
            if parent in snapshots:
                for claim_id, item in snapshots[revision_id].items():
                    if claim_id in snapshots[parent] and item != snapshots[parent][claim_id]:
                        require(any(c.get("claim_id") == claim_id and c.get("from_revision_id") == parent and c.get("to_revision_id") == revision_id for c in corrections.values()), prefix + "changed claim lacks correction: " + claim_id)
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
        if case["kind"] != "public_snapshot":
            continue
        if case.get("source_record") != source_path:
            errors.append("public snapshot has an unknown canonical editorial register")
            continue
        original = json.loads((ROOT / source_path).read_text(encoding="utf-8"))
        errors.extend(validate_public_snapshot(case, original))
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
