# SPACEЖ RELAY — public evidence and review RFC

**Version:** 0.1 · **Date:** 17 October 2026  
**Status:** published read-only public-data prototype and proposed architecture; no operational investigation service, connected Parallax RELAY import, confidential intake, or warning capability is claimed.

This RFC translates the supplied planning draft into a bounded first implementation. The current work covers site presentation, synchronized canonical plans, and a read-only case prototype. Further infrastructure and sensitive features have separate gates. See [the implementation plan](RELAY_IMPLEMENTATION_PLAN.md) for paths, acceptance, and delivery status and [the founding proposal](FOUNDING_PROPOSAL.md) for funding, governance, and wider mission.

## Product boundary

SPACEЖ RELAY is the proposed civilian, public-interest investigation and verified information-sharing product: source-linked evidence, analyst review, controlled sharing, public cases, revisions, and corrections. Start with Ukraine and public material useful to journalists, human-rights monitors, researchers, verification teams, and public-interest watchdogs. Editorial conclusions must follow the evidence; the mission does not establish an allegation as true.

The four SpaceЖ workstreams remain distinct:

| Workstream | Proposed responsibility and boundary |
| --- | --- |
| SPACEЖ RELAY | Cases, claim-level evidence, accountable human review, access policy, publication, and corrections. Real public-source cases in v0.1; minimal synthetic records only in unit tests. |
| SPACEЖ ECHO | Source-linked orbital intelligence, historical visualization, uncertainty, and provenance. Public orbit data does not establish launch detection. |
| SPACEЖ ARRAY | Lawful, opted-in, reproducible ground-station infrastructure and interoperability research. No station network is assumed. |
| SPACEЖ PARALLAX | Separately authorized hosted-payload or orbital feasibility, after engineering, regulatory, funding, and stewardship gates. |

**Transport/Interoperability** remains an optional, separately gated area under SPACEЖ RELAY: terrestrial transport, delay-tolerant messaging, simulation, and evaluation on authorized links. It is not the first evidence product and does not imply satellite connectivity or emergency service availability.

## Reuse before integration claims

**SPACEЖ RELAY** owns the product and editorial rules. **Parallax RELAY** is the intended reusable source ingestion, normalization, provenance, and publishing layer. The local workspace consumes a curated real-source registry and actual access receipts; it has no connection to a deployed Parallax RELAY service. A local publication projection must not be described as a completed external import.

Before implementing a networked application, inventory actual Parallax RELAY interfaces, versions, licensing, identity rules, export capabilities, and failure semantics. Record which responsibilities are reused and which belong to the SpaceЖ editorial domain. Do not invent provider APIs or duplicate ingestion infrastructure based on product names alone. Versioned open JSON exports should keep the static publication portable.

The six wider ecosystem roles are proposed: **Slipstream** for scoped engineering/review gates; **Plexus** for permissioned identity and collaboration; **Positronic** for structured analysis; **Parallax RELAY** for reusable ingestion/publication; **HOLO** for permitted preservation/media; **Continuum** for human-owned approvals and stewardship. No integration, partner relationship, or institutional endorsement is implied. The [Plexus handoff](PLEXUS_NETWORK_HANDOFF.md) continues to prohibit inferred public affiliations and publication of private outreach records.

## First release and data flow

The current static publication is at `/relay/`. Two real cases contain 20 claims, 17 source records and eight open questions. The UNHCR winter-aid case has 13 claims and nine sources and opens first; the Starshield dossier remains available. Readers can inspect claims, sources, reporting periods, target/result comparisons, AI review records and actual edits. Missing delivery or expenditure values remain unknown. There is no browser authoring, authentication, upload, tipline, ingestion endpoint or alert action.

```text
Real public-source cases + content-review notes
       data/relay/cases.json
       data/relay/source-reviews.json
                     |
Explicit public HTTPS access check (manual command)
       scripts/ingest_relay_sources.py
                     |
Actual response receipts: data/relay/retrievals.json
                     |
Validation + source receipt attachment + static export
       scripts/build_relay_publication.py
                     |
public/relay/data/{cases,retrievals,manifest}.json
                     |
       Read-only /relay/ browser experience
```

Real `public_case` histories now preserve the full wording, status, caveat, citations and locator of each claim. The first history entry can import an actual previously published Git commit; the validator reads that object and rejects a fabricated baseline. This import carries no retroactive approval. New revisions link actual review records to the SHA-256 of their claim snapshots. AI reviews use `reviewed`; a human publication approval must identify a human reviewer. Date ordering, changed claims and explicit before/after records are checked. Additions use `update`; wording clarifications and factual corrections remain distinct. The UNHCR history records a terminology clarification, new evidence and an actual correction: the earlier wording had applied a people-specific cutoff to generator units. The 110 and 186 reported generator totals differ by 76 without an established reconciliation. The [follow-up note](evidence/2026-10-17-unhcr-followup.md) also distinguishes cash funding and rollout context from a quantified explanation of the shortfall.

Publication records are immutable at runtime. A later correction must describe an actual repository edit and rebuild, with affected versions and prior revision records retained. No reviewer identity, approval, or correction history is fabricated to populate the interface. Git history and deterministic exports support inspection; neither guarantees tamper-proof storage, legal admissibility, or the truth of a source's statement. Never place restricted fields in a public file and rely on a hidden view or client-side filter to protect them.

The existing [Starshield brief](evidence/2026-10-16-starshield.md) and [source/claim registry](../data/evidence/starshield-restrictions-2026-10-16.json) remain the dated editorial source. [Content reviews](../data/relay/source-reviews.json) checked accessible reporting on 17 October 2026 and identify the exact copy read: originals, syndications, Reuters republications, or indexed AP content. The Telegraph original remained inaccessible; its AOL syndication is the same underlying investigation. Preserve attribution, denials, copyright limits, and the lack of a single verdict. Reuters' reported impact and separately sourced White House-origin allegation do not independently establish the reported Musk–Trump conversation. These reviews are AI-assisted source checks, not human editorial signoff, new original interviews, or proof of the allegations.

The published [case registry](../data/relay/cases.json) contains real public-source cases only. The fictional exercise and simulated reviewers have been removed from the public bundle; minimal synthetic records are confined to unit tests. Missing review attribution or unavailable retrieval details remain missing or explicitly described.

The [source access checker](../scripts/ingest_relay_sources.py) makes an explicitly invoked HTTPS GET to each allowlisted public URL and appends actual timestamps, status codes, response byte counts, and SHA-256 hashes to [retrievals.json](../data/relay/retrievals.json). Bodies are hashed in memory without full-article preservation or republication. The latest 17 October run attempted 21 URLs: twelve returned HTTP 200 and nine were unavailable (four Reuters 401 responses, Telegraph 402, AP 403, IAEA 403 and two UNHCR 403 responses). Readable Reuters republications are included in the registry. A content review through web research and a transport receipt from this command are distinct observations; HTTP success is not a factual verdict. This is a manual tool, not a background ingestion service. The builder attaches receipts to sources and emits public cases, receipts, and a manifest.

## Domain model

These are conceptual responsibilities. The current public registry schema is deliberately narrower than a future authoring database; a JSON collection does not implement permissioned collaboration.

| Entity | Required meaning and future authoring responsibility |
| --- | --- |
| Source | Public provenance, publisher/creator, URL, source type, publication/retrieval times where known, rights, and relationship to upstream reporting. |
| Artifact | Original or derivative, lawful preservation basis, fingerprint of the actual stored bytes, acquisition/custody and transformation history, safe storage and release policy. |
| Observation | A precisely attributed account of what was directly observed, including limits and timing uncertainty. Reporting that someone observed something is not SpaceЖ's own observation. |
| Claim | One testable proposition, scope, classification, status, uncertainty, and the distinction between an observation, reported allegation, denial, and inference. |
| EvidenceLink | The relationship between a claim and source/artifact/observation: supporting, contradicting, or ambiguous, with a rationale. |
| Case | An investigation scope, question, responsible owner, claims, evidence, timeline, and unresolved gaps. |
| Review | Attribution, method, scope, rationale, conflicts, decision, time, and the exact reviewed revision. AI-assisted content checks, HTTP access, and human editorial approval remain separate records. |
| Publication | A public revision, scope, content fingerprint, publication status/date, and linked review; a redacted projection of permitted content. |
| Correction | An append-only record of what changed, why, affected claims/revisions, responsible review, and the replacement or withdrawal. |
| AccessPolicy | Public/restricted classification, disclosure consent where applicable, permitted uses, retention, and explicit redactions, enforced before export. |

A fingerprint of repository-authored export bytes proves only that those bytes match a recorded value. A transport receipt's body hash identifies the response bytes fetched at its timestamp; it does not authenticate their origin beyond that recorded request or establish their truth. Full articles, screenshots, paywalled bodies, copyrighted photographs, and private sources are not archived or republished by this workspace. Future artifact preservation requires an explicit lawful basis and safety review.

## Editorial lifecycle

The proposed authoring lifecycle is `received → triaged → needs corroboration → supported / disputed / unresolved → human-approved for publication → published / updated / corrected / withdrawn`. Confidential material, if ever authorized, begins restricted in a separate system. A source's type, a claim's status, the case's workflow state, and a publication's approval are separate concepts.

1. Scope the case and identify allowed public material. Record the original publisher, relevant dates, rights, and known upstream relationships.
2. Split compound propositions where their evidence or status differs. Link contrary evidence and denials next to the claims they address; do not count URLs as independent witnesses.
3. Record observations, source assertions, and analyst inferences distinctly. State uncertainty and unresolved gaps; avoid invented confidence scores.
4. A responsible human reviews sourcing, proportionality, rights, safety/redactions, conflicts, and the exact proposed publication. Record missing review provenance honestly.
5. Publish only the allowed projection. Preserve revision IDs and a correction/withdrawal reason; do not silently overwrite a contested conclusion or use a correction log to repeat harmful personal data.

AI may assist clustering, proposed cross-references, and drafting for review. It cannot independently declare truth, deanonymize contributors, approve publication, or trigger emergency alerts. The static prototype represents this workflow; it does not implement an approval authority or accept new cases from visitors.

## Source-protection threat model and trust boundaries

This is an initial design boundary, not a completed security assessment. Public availability does not eliminate risk to people identified in a source or excuse unnecessary republication.

| Area | Initial assessment and boundary |
| --- | --- |
| People and assets | Contributors, subjects, witnesses, readers and reviewers; identities, location metadata, access logs, unpublished notes, evidence integrity, and editorial decisions. |
| Adversaries and failures | State-capable surveillance, coercion, malicious submissions, account compromise, insiders, accidental disclosure, fabricated or coordinated reporting, and correlation of apparently separate sources. |
| v0.1 public trust zone | Repository case records and deployable static assets contain intentionally public real-source material. Minimal synthetic records exist only in unit tests. All downloaded JSON is public. External links remain at the source; no third-party embeds or tracking are needed. Hosting and source publishers may still receive normal network requests. |
| Restricted trust zone | No confidential submission route exists in v0.1. Do not solicit confidential material through public issues, forms, chat integrations, or the Plexus public graph. Private outreach and any sensitive material remain outside publication fixtures. |
| Publication boundary | Human editorial/safety review and an explicit public projection precede release. Validate IDs, references, safe URLs, classifications, and revision consistency. Treat imported text as data, never executable instructions or HTML. |
| Residual risks | A public release can be copied permanently; a hash does not authenticate a claim; compromised devices, coercion, traffic correlation, source metadata, and mistakes can defeat protections. No anonymity, legal-admissibility, or state-adversary protection guarantee is made. |

Do not publish unconsented identities, precise sensitive locations, live military movements, targetable military data, operational sensor layouts, credentials, or restricted feeds. Do not ask contributors to trespass, access systems without authorization, approach military assets, or take personal risks. Collect and retain only what the approved purpose requires. Public withdrawals may need to remove unsafe content from the current export while preserving a minimal, non-identifying correction record; unrestricted public Git is unsuitable for secret evidence or guaranteed erasure.

Before any confidential intake, require a written case-specific threat model; security, privacy and legal review; Ukrainian and other affected contributor-safety input; an accountable staffed operator; access and key management; retention/deletion rules; incident response; and a realistic budget. Assess a professionally operated SecureDrop-class service or trusted external partner instead of inventing bespoke anonymous infrastructure. A VPN or network bouncing does not establish anonymity. No such service or partner is selected, contacted, provisioned, or endorsed by this RFC.

## Separate early-warning safety track

The [independent early-warning research](../research/002-independent-early-warning/README.md) and [scientific review protocol](../research/003-observation-gap/REVIEW_PROTOCOL.md) remain research. Their useful transferable principles are explicit time origins, uncertainty, complete evaluation denominators, upstream-dependency audits, independent review, and publication of insufficiencies. Synthetic metric tests are not launch sensing.

The public case platform must not originate warnings, turn unverified sightings into alerts, expose real-time threat locations, infer targets, or claim a 60-second operational capability. Any future handoff to official civilian warning authorities requires its own authorized safety-critical scope, independent evidence, qualified review, and approval. It is outside this release.

## Delivery gates and remaining decisions

- **A — Site presentation:** preserve the original hero, add accurately labeled solidarity artwork, retain Ukrainian tryzub prominence, and verify responsive/accessibility behavior.
- **B — Canonical architecture:** synchronize this RFC, the implementation plan, founding proposal, and rendered `/plan/`; preserve budgets, governance, and existing safety limits.
- **C — Public-data v0.1:** two real-source cases, source locators, separate content reviews and actual HTTP receipts, eight unresolved verification questions, read-only local assets, and reproducible validation/build. No fictional public case, fabricated reviewer/correction history, secrets, or networked intake. Integrated checks and visual review precede any deployment decision.
- **C follow-on — Authoring architecture:** assess actual Parallax RELAY reuse, then separately scope a Laravel + React/Inertia + PostgreSQL application, access controls, review separation, audit history, safe exports, backups and funded operations. Do not scaffold it into `public/` now.
- **D — Sensitive features:** confidential intake or civilian-safety routing requires expert review and separately authorized operating capacity. There is no launch date or commitment.

The workspace leaves real editorial staffing, a verified upstream integration contract, production authoring permissions, long-term preservation and independently reviewed security unimplemented. Passing registry and source-consistency checks does not resolve those decisions or validate the underlying allegations.

## Standards and references

- [Berkeley Protocol on Digital Open Source Investigations — UN OHCHR and Berkeley Human Rights Center](https://humanrights.berkeley.edu/publications/berkeley-protocol-on-digital-open-source-investigations/): a reference for professional, ethical collection, analysis, preservation, and investigator/witness safety. This RFC does not claim certification or full compliance.
- [WITNESS — Archiving and Video as Evidence](https://archiving.witness.org/archive-guide/resources/video-as-evidence/): documentation, contextual metadata, custody, original files, and fixity are relevant to future permitted artifacts. Hashes alone do not establish evidentiary truth or court admissibility.
- [SecureDrop — Threat Model](https://docs.securedrop.org/en/stable/threat_model/threat_model.html): a reference for explicit actors, adversaries, assumptions, and limits. It does not make this static site a secure submission system.

References identify design resources, not organizational endorsement, a legal opinion, an implemented control, or a completed expert review.
