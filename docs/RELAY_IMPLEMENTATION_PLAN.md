# SPACEЖ RELAY — implementation plan

**Date:** 17 October 2026 · **Scope:** site presentation, canonical planning, and public-data v0.1  
**Release boundary:** local implementation for review; deployment, external integrations, confidential intake, payments, and warning services are not implied.

The first concrete release is a reproducible, revisable public evidence workspace using real source material. The [architecture RFC](SPACEZH_RELAY_OSINT_RFC.md) defines SPACEЖ RELAY's editorial responsibilities and the separate reusable Parallax RELAY layer. The [founding proposal](FOUNDING_PROPOSAL.md) remains canonical for the wider initiative, budgets, governance, and hardware gates.

## Current implementation status

| Area | Local scope and status |
| --- | --- |
| Existing foundation | Static site, canonical founding proposal and `/plan/`, Starshield editorial brief and claim/source registry, and separately labeled scientific research already exist. |
| Stage A | Site presentation work in this change: local solidarity asset, clear identity labels, tryzub treatment, and responsive verification. Local implementation and visual checks are complete; see [verification record](RELAY_QA.md). |
| Stage B | This implementation plan, the RELAY architecture RFC, and synchronized founding-proposal/`/plan/` changes are part of this change. |
| Stage C | Published read-only site: two real cases, 17 claims, 14 source records, source locators, an eight-question verification queue, timelines, actual revision/correction records, and separate content-review and HTTP-access evidence. See [verification record](RELAY_QA.md) for completed checks and visual review. |
| External services | No connected Parallax RELAY import, Plexus publication, professional review, backend authoring or confidential-source service is established by this work. |
| Future tracks | Permissioned authoring, secure intake, civilian-safety routing, field communications, and orbital work remain proposed with separate gates. |

The static site is deployed through the existing Forge host. The [verification record](RELAY_QA.md) and [deployment record](PRODUCTION_DEPLOYMENT.md) retain local checks, screenshots and live verification. Backend authoring and other follow-on tracks remain separate. No reviewer identity, approval, independent investigation, or external article retrieval should be fabricated to fill a missing field.

## Stage A — site presentation

**Paths:** `public/index.html`, `public/assets/spacezh-solidarity-flags.webp`, `public/assets/tryzub.svg`, the shared brand/mobile stylesheets, and associated local attribution documentation where changed.

1. Preserve `public/assets/spacezh-hero.webp` and its Earth/Ukraine hero position. Place the supplied 1448 × 1086 solidarity image in its own responsive feature, preserve its aspect ratio, and use descriptive alt text.
2. Identify the white-blue-white Russian anti-war / Free Russia flag accurately and the EU flag as solidarity symbolism. Keep Ukraine's tryzub prominent. Do not imply government, EU, or institutional endorsement.
3. Compare the local tryzub with an authentic, legally reusable authoritative vector; keep crisp small-scale line work and document provenance. Preserve the wordmark, four SpaceЖ products, six distinct Parallax ecosystem roles, and bilingual `ЖИТТЯ = LIFE`, `ВОЛЯ = FREEDOM`, `НАУКА = SCIENCE` ribbon.
4. Audit 390, 750, 820, 1024, and 1440 CSS-pixel viewports. Resolve page overflow and clipping; verify artwork, text, navigation, and focus visibility. Record mobile and desktop before/after screenshots in review artifacts.

**Acceptance:** original hero retained; image local and correctly labeled; meaningful alt text; no horizontal page overflow at target widths; usable mobile navigation and reading order. No backend/payment changes or removal of safety disclaimers. Release review must report any unavailable before-state screenshot rather than inventing one.

## Stage B — architecture and synchronized plans

**Paths:** `docs/SPACEZH_RELAY_OSINT_RFC.md`, `docs/RELAY_IMPLEMENTATION_PLAN.md`, `docs/FOUNDING_PROPOSAL.md`, `public/plan/index.html`; update adjacent README/product summaries consistently.

1. Make SPACEЖ RELAY the proposed investigation, human-review, evidence, controlled-sharing, and corrections product. Keep Transport/Interoperability as an optional separately authorized sub-track.
2. Preserve Parallax RELAY as the intended reusable ingestion/normalization/provenance/publication layer; state that no connected integration exists. Preserve Slipstream, Plexus, Positronic, HOLO, and Continuum as distinct intended roles.
3. Specify the conceptual Source, Artifact, Observation, Claim, EvidenceLink, Case, Review, Publication, Correction, and AccessPolicy responsibilities, review lifecycle, public/private boundaries, and staged source-protection threat model.
4. Synchronize changed canonical proposal text and roadmap into `/plan/` in this change. Keep the original up-to-$2,000 discretionary cash ceiling, separate funding requirements, governance rules, regulatory discussion, and scientific/operational limits.

**Acceptance:** the first deliverable contains real public-source cases; canonical/rendered paragraphs and lists agree; architecture names and status claims agree across pages; no launch date, partnership, operational network, confidential intake, or independent fact-check result is invented.

## Stage C — static public-data v0.1

**Canonical content:** [case registry](../data/relay/cases.json), [source content reviews](../data/relay/source-reviews.json), and [actual HTTP receipts](../data/relay/retrievals.json); preserve the existing `data/evidence/starshield-restrictions-2026-10-16.json` and `docs/evidence/2026-10-16-starshield.md` as the dated editorial source.  
**Publication:** `public/relay/index.html`, generated `public/relay/data/{cases,retrievals,manifest}.json`, `public/assets/relay.css`, and `public/assets/relay.js`.  
**Tooling:** [source access checker](../scripts/ingest_relay_sources.py), [publication builder](../scripts/build_relay_publication.py), `scripts/check_relay_publication.py`, and `tests/test_relay_publication.py`.

1. Curate real public-source case records with stable IDs and explicit classifications. Preserve allegations, denials, unresolved questions, source-independence relationships, and caveats. Keep rights restrictions visible; do not archive/republish full source articles or accept visitor submissions.
2. Generate the deployable public projection deterministically and attach actual access receipts to sources. Validate IDs/references, source URLs, claim statuses, review methods, and revision/correction relationships. Keep response hashes separate from authored export fingerprints and factual conclusions.
3. Build the Evidence Ledger, Claim Details, Case Timeline, Corrections Log, and eight-question verification queue with client-side browsing/filtering. Show source locators, content-review scope, and transport results distinctly. Render imported text as data. Ensure keyboard access, readable empty/error states, and local assets.
4. Open the updated UNHCR winter-aid case by default, with the Starshield dossier also available: two cases, 17 claims and 14 source records. The UNHCR case retains earlier UN/OHCHR and IAEA context. Remove the fictional exercise and simulated reviewers from the published bundle. Retain minimal synthetic records only in unit tests. Content reviews checked on 17 October 2026 are AI-assisted, not human editorial signoff.
5. Record actual revisions only. A future correction must identify a real edit, its reason, and affected versions; never fabricate reviews or correction history to populate a workflow. Browser state is read-only: publication changes require a repository edit, review, validation, and rebuild. No backend, login, upload, continuous ingestion service, analytics, tipline, emergency action, or third-party tracking is added.
6. Run the source access checker explicitly when refreshing transport evidence. It performs HTTPS GET requests only to allowlisted public publishers, hashes response bodies in memory, and appends actual timestamps, HTTP status, byte counts, and response hashes. The 17 October run attempted 15 URLs: eight HTTP 200 responses and seven unavailable URLs (four Reuters 401 responses, Telegraph 402, AP 403, and IAEA 403). Accessible Reuters republications are included. This manual command is not a daemon, full-article archive, or factual verdict; web-research content access is a separate record.

**Acceptance:** a reader can trace each key claim to source locators, inspect contradictory accounts and uncertainty, distinguish content review from HTTP access and human approval, see unresolved verification work, and inspect actual revisions. Any future correction identifies its reason and affected version. Registry checks fail on meaningful integrity violations and reject fictional public cases. Generated publication matches canonical case and receipt content. The app remains visibly a public evidence workspace for review and provides a useful static fallback/error path if interactive data cannot load.

To refresh access evidence, explicitly run `python scripts/ingest_relay_sources.py` before rebuilding. This makes public network requests and appends a new receipt run; it is separate from the offline publication checks below.

Run the reproducible checks from the repository root with Python 3:

```sh
python scripts/build_relay_publication.py
python scripts/check_relay_publication.py
python -m unittest discover -s tests -p 'test_*.py' -v
python scripts/check_research_publication.py
python scripts/check_evidence_brief.py
python -m http.server 8080 --directory public
```

The research-publication check verifies existing scientific source/rendered consistency; it is not an early-warning capability test. Re-run relevant research suites if their inputs or code change. Review `/`, `/plan/`, and `/relay/` at the target widths; inspect `/research/` and the existing Starshield brief for navigation and status regressions. Verify navigation/filter/detail/timeline/correction interactions, asset requests, browser console, keyboard access, and absence of external application requests. File/model checks do not substitute for visual inspection or validate source truth.

### C follow-on — separately deployed authoring application

**Status: proposed, not scaffolded.** First inventory the actual Parallax RELAY implementation and agree a versioned adapter/export contract. Decide whether a separately deployable Laravel + React/Inertia + PostgreSQL application is justified; do not mix a server application into the static `public/` tree.

An approved follow-on scope must name its deployment repository/path, accountable editor/operator, access model and funding. It should cover role- and case-level authorization, drafts/reviews separated from public exports, human publication approval, append-only audit/revision history, backup and restoration, rights-aware artifact storage, retention, incident response, and reproducible export to the existing static publication. Restricted records must never reach public bundles. Security review and adversarial access/export tests precede deployment. No live interface or credentials are assumed now.

## Stage D — separately approved sensitive features

**Status: excluded from v0.1; no date or public launch commitment.** Confidential voluntary submissions and authorized civilian-safety handoff are independent decisions, not automatic consequences of completing the public prototype.

Before confidential intake, require qualified security/privacy/legal review, an institution capable of sustained source protection, a case-specific written threat model, affected-contributor safety input, trained staffing, access/key management, retention/deletion, incident response, and a funded operating scope. Assess professional SecureDrop-class operation or a trusted partner; do not create bespoke anonymous intake or promise anonymity. Keep restricted records separate from public/Plexus graphs and publication fixtures.

Civilian-warning research requires its own lawful independent observation evidence, evaluation, Ukrainian civilian-protection input, and authorized official control. Public tips, orbital catalogues, fast transport, and synthetic metric tests are not a detection capability. Do not originate warnings, publish live attack maps, create targeting feeds, expose operational sensor layouts, or imply a government relationship.

**Acceptance before any future launch:** a concrete reviewed design, named accountable owners, approved funding and operating responsibilities, documented residual risks, and explicit authorization for that specific feature. The [architecture RFC's standards references](SPACEZH_RELAY_OSINT_RFC.md#standards-and-references) guide review but do not confer certification, endorsement, or automatic approval.

## Release review and truthful reporting

- Report local implementation, checks, visual evidence, and known limitations separately from deployment status. Serve only `public/` if deployment is later authorized; never expose repository-only or restricted data by changing the document root.
- Preserve the founding proposal's funding/governance rules. No spending, purchase, fundraising target, checkout, or paid-review commitment is authorized by a plan entry.
- Keep the static publication useful while future architecture is unresolved. Do not label the platform operational solely because a browser prototype works.
- External publication, messages, contacts, service provisioning, confidential intake, field operations, and warning routing require their own authorized scope. They are not completion steps for this local release.
