# SpaceЖ — Plexus Network Handoff

**Proposed architecture; no records have been imported into Plexus.**

Keep Plexus as the canonical public people/org/project identity and capabilities network. The public `data/partner_candidates.public.json` file is **identity-resolution input only**: independent organizations/programs plus public evidence URLs, not a verified network of relationships.

## Resolution

1. Match canonical existing Plexus `Organization`/`Program` nodes by reliable domains and known aliases, with human review for ambiguous names.
2. Save source URL and as-of date. Avoid duplicate organizations and mistakenly merging embedded projects into parents.
3. Do **not** create public `PARTNER_OF`, `ENDORSED_BY`, `KNOWS` or similar claims from research candidates.
4. Create a separate **private** opportunity only after an outreach owner approves a specific target.
5. Record contact, reply, proposal, mutual introduction, governance commitment, and delivery only when actually evidenced and properly permissioned.

## Proposed private record

```json
{
  "initiative_id": "initiative-spacezh",
  "canonical_plexus_organization_id": "<after-resolution>",
  "stage": "researched_not_contacted",
  "review_area": "open_satellite_provenance",
  "outreach_owner": null,
  "approved_to_contact": false,
  "interaction_log": [],
  "last_contact_at": null,
  "consent_to_public_affiliation": false,
  "visibility": "private"
}
```

Stage progression: `researched_not_contacted → verified_channel → approved_to_contact → contacted → replied → exploratory_call → scoped_contribution → committed_contribution → delivered`; also `declined`, `deferred`, `unresponsive`.

Potential types: `Organization`, `Person`, `Program`, `Capability`, `Initiative`, `Opportunity`, `Interaction`, `Evidence`, `Pilot`. Potential relationship types: `RESEARCHED_FOR` (private), `REQUESTED_REVIEW` (private), `CONSENTED_INTRODUCTION`, `AGREED_TO_PILOT` (evidenced), `PUBLICLY_ENDORSED` (specific published consent).

**Privacy:** do not put outreach records, prospect notes, sensitive location/communications details, personal emails, credentials, restricted material, or consent information on the public DeSo graph. No inferred reputation scores or bulk solicitation.

## First implementation

Build a **read-only dry-run entity resolver** with fields: `candidate_id`, `suggested_existing_ids`, `match_evidence`, `needs_review`, `recommendation`. Publish nothing and send no messages. Only then add an access-controlled initiative opportunity store and human approval flow.

The previous 24-lead private research seed remains outside GitHub. Only public organization/program identities are committed here.
