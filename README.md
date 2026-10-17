# SpaceЖ — The sky belongs to everyone

Public site and founding proposal for SpaceЖ, an open-source public-interest initiative proposed in support of the **global defense of Ukraine** through public-source evidence, auditable satellite intelligence and resilient communications research.

**Status:** public working proposal, not an established nonprofit, operational satellite network, or live warning service. No donations are being accepted through this repository.

## This site

The homepage at `/` links to the designed public proposal at **`/plan/`** and the public coalition research/invitation at **`/coalition/`**. The [Markdown proposal](docs/FOUNDING_PROPOSAL.md) and [coalition strategy](docs/COALITION_STRATEGY.md) remain editable source documents. No live payment processing is implemented.

The deployable static website lives in **`public/`**: `public/index.html`, `public/plan/index.html`, `public/coalition/index.html`, `public/assets/favicon.svg`, and `public/assets/spacezh-hero.webp`. Repository-level `docs/` and `CONTRIBUTING.md` are project documentation, not public web assets. No npm dependencies, analytics, third-party scripts, or backend. RELAY uses local JavaScript, a deterministic Python publication export, and an explicitly run public-source access checker. The launch design, responsive CSS, animated synthetic scanner, and original artwork have been preserved.

To preview locally:

```bash
python3 -m http.server 8080 --directory public
```

Visit http://localhost:8080, http://localhost:8080/plan/, and http://localhost:8080/coalition/. **Set the hosting site's document root / publish directory to `public/`** (not the repository root), so `index.html` is served at `/` and `assets/*` resolves at `/assets/*`. For nginx, point `root` to the full filesystem path of the `public` folder; for a static host, use `public` as the publish directory with no build command. The live canonical domain is `https://xn--80akd1bg1j.com/`.

## Read before contributing

- [Public founding proposal (full Markdown)](docs/FOUNDING_PROPOSAL.md)
- [How to contribute](CONTRIBUTING.md)
- [GoFundYourself post-funnel integration plan](docs/GOFUNDYOURSELF_INTEGRATION.md)

A PDF copy of the proposal was produced separately and can be uploaded to the repository once an approved binary-file publishing route is available.

## Workstreams

1. **SpaceЖ Echo:** Source-linked orbital intelligence, 3D observations, provenance, and playback.
2. **SpaceЖ Array:** Reproducible, opt-in ground-station tools interoperable with established open projects.
3. **SpaceЖ Relay:** Public-interest investigations, evidence review, source-linked cases and corrections; Transport / Interoperability is a separately gated research area.
4. **SpaceЖ Parallax:** Separately gated feasibility research for a hosted payload or spacecraft.

### Bootstrap funding discipline

The first 90 days have an **up-to-$2,000 discretionary cash spending ceiling**, not a fundraising commitment or assumption that money is available. Begin with open tools, public datasets, and available infrastructure. There is no arbitrary year-one fundraising target: price and approve concrete milestones before spending, and publish actual receipts, expenses, in-kind support, and progress.

Paid labor, professional reviews, regulated operations, and flight hardware are **outside** this startup cash allowance and require separately funded approved scopes. No donations or GoFundYourself checkout are live; payment, tax, and governance arrangements must be settled first.

## Ukrainian identity and Parallax products

The SpaceЖ wordmark remains **SPACEЖ**. A Ukrainian **tryzub** now accompanies the header and footer wordmarks across the static website, with a larger, labeled emblem on the homepage. The public-domain vector is stored locally in `public/assets/tryzub.svg`, adapted from [Wikimedia Commons — Coat of Arms of Ukraine](https://commons.wikimedia.org/wiki/File:Coat_of_Arms_of_Ukraine.svg). This represents solidarity with Ukraine, **not** government affiliation, endorsement, or official status. The original SpaceЖ favicon and Earth artwork are preserved.

The homepage presents the four SpaceЖ workstreams as **proposed products**: **ECHO**, **ARRAY**, **RELAY**, and **PARALLAX**, preserving their research-stage and feasibility gates. A separate Parallax technology section describes possible infrastructure roles for **Slipstream**, **Plexus**, **Positronic**, **RELAY**, **HOLO**, and **Continuum**. Parallax RELAY is a general-purpose ingestion/publication product, separate from the SpaceЖ RELAY investigation and evidence platform. Transport / Interoperability remains a separately gated SpaceЖ RELAY research area. These are intended integrations, not claims of operational services.

The new shared stylesheet, `public/assets/brand-products.css`, keeps tryzub and wordmark treatment consistent throughout the homepage, public proposal, coalition page, research index, research readers and evidence brief. No external scripts or assets, intake forms, or payment processing were added.

## Maintaining visual integrity

The original artwork and `public/assets/` are retained. The bilingual ribbon separators now pair Ukrainian with English using equals signs, and its intermediate-width rule keeps pairs together. The supplied anti-war / EU solidarity artwork is displayed in a separate, labeled feature; the original Earth/Ukraine hero is retained. All three Ukrainian/English ribbon pairs remain visible on mobile. See [asset provenance](docs/ASSET_SOURCES.md). The future GoFundYourself mount remains **hidden**; no payment form has been introduced.

The front-end is currently just a publication channel, not the promised orbital product. Technical workstreams, licensing, and governance are proposals for public review.

## Maintaining the published proposal

`docs/FOUNDING_PROPOSAL.md` is the editorial source. `public/plan/index.html` is a static rendered edition with a responsive reading layout, navigation, sources, and accessible tables. Update both together; no runtime Markdown fetching or CDN is required. Original homepage CSS and design assets remain unchanged.

## Coalition, outreach and Plexus

- [Coalition landing page](public/coalition/index.html): first-wave candidate research, public requests, a 90-day sequence, and clear non-affiliation disclaimers.
- [Coalition research and outreach strategy](docs/COALITION_STRATEGY.md): 22 source-linked institutional/program research leads (public identities only), six suggested review questions, and the rollout.
- [Public identity-resolution seed](data/partner_candidates.public.json): **not** a CRM, partner list, or evidence of endorsement.
- [Plexus private relationship handoff](docs/PLEXUS_NETWORK_HANDOFF.md): canonical entity matching, public/private boundaries, consent, evidence and gated outreach.
- [Deployment / first outreach checklist](docs/DEPLOYMENT_AND_OUTREACH_GATE.md): verify the actual public website before any invitations.
- [Public GitHub coalition-interest issue template](.github/ISSUE_TEMPLATE/coalition-interest.yml): for public technical contributions, never confidential personal contacts.

No emails have been sent, no Plexus import has been performed, and no affiliation has been established through this repo update. The separate 24-candidate **private** prospecting package was deliberately not committed to the public repository.

**Deployment:** The existing production host and nginx document root were verified on 17 October 2026. See the [production deployment record](docs/PRODUCTION_DEPLOYMENT.md) for the observed release, publication checks and rollback procedure. Verify the intended commit and fresh public content before sharing links; a GitHub push alone does not establish that a new release is live.

## Mobile layout and copy

The original embedded desktop CSS and design assets are preserved. A separate [mobile polish stylesheet](public/assets/mobile-polish.css), loaded after each page's existing styles, adjusts phone layouts, preserves the bilingual ribbon through tablet widths, and stacks the hero/navigation at 1000px and below. It wraps the bilingual ribbon on phones, reduces section/card spacing, preserves 44px menu tap targets, and improves hero, buttons and proposal reading typography.

Public headlines and explanatory copy have been revised to describe the actual scope and proposed partnership work rather than rely on generic startup slogans. The main "The sky belongs to everyone" identity is retained.

For manual QA, check all three routes (`/`, `/coalition/`, `/plan/`) at narrow mobile widths, ~390px, 750px and desktop. Confirm no horizontal page scroll, readable cards and budgets, working navigation, intact artwork, and the synthetic-data/funding disclaimers.

## Research programme

- [Research index](research/README.md) — scientific standards and status of open studies.
- [Research 001](research/001-leo-contact/README.md) — circular LEO contact, radio budget and link margin; ten tests; not field validated.
- [Research 002](research/002-independent-early-warning/README.md) — independent 60-second ballistic-warning feasibility question; nine tests of synthetic metric accounting, **not** a real missile-detection system.
- [Research 003](research/003-observation-gap/README.md) — evidence register of six public programmes/service categories, mathematically bounded correlated observations, uncertainty and sampling bias; 15 tests, **no launch detector**.
- [Research 003 independent review protocol](research/003-observation-gap/REVIEW_PROTOCOL.md) — evidence required before any claim of 60-second launch verification.
- [Research 004](research/004-claim-validation/README.md) — statistical evidence thresholds for a 60-second reliability claim, including false-alarm confidence and 24 tests; **not demonstrated**.
- [Independent peer review, 16 October 2026](research/PEER_REVIEW_2026-10-16.md) — what reproduces, which citations were wrong, and what the studies still lack.
- [Public research page](public/research/index.html) available at `/research/` after deployment.

Run the first three test suites with `python3 -m unittest discover -s research/001-leo-contact -p 'test_*.py' -v`, `python3 -m unittest discover -s research/002-independent-early-warning -p 'test_*.py' -v`, and `python3 -m unittest discover -s research/003-observation-gap -p 'test_*.py' -v`. No third-party libraries are required. Passing synthetic-model tests is **not** proof of real-world sensing.

Run Research 004 using `python3 -m unittest discover -s research/004-claim-validation -p 'test_*.py' -v`. Together the four studies contain **58 passing mathematical/model tests**, which do not demonstrate any real launch-sensing capability.

## Reading the studies without GitHub Markdown

The [research page](public/research/index.html) links to the full on-site versions of Research 001–004. Each reader includes the complete canonical README prose, responsive tables, **native MathML** instead of raw LaTeX, and a **standalone SVG graph**. Research 003 and 004 also include their scientific review documents below the main study. Graphs are deliberately fictional or hypothetical and provide their underlying numbers on the page.

GitHub remains the home of source code and test suites, not the required publication viewer.

**Maintainer rule:** when a Markdown study changes, update its corresponding on-site HTML and re-run `python3 scripts/check_research_publication.py`. The published pages include a content fingerprint of the canonical Markdown source, so CI will fail if the source changes without updating the website. This is a source-consistency check, not a scientific result or proof that a browser renders well; mobile and desktop layout still need visual QA.

## Featured source reporting

- [On-site SpaceЖ evidence brief: Who throttled Ukraine's Starshield?](public/research/briefings/starshield-restrictions/index.html) — a dated source-by-source explanation separating Telegraph's allegation, Reuters' independently sourced reporting, public denials and Ukrainian frontline impact.
- [Canonical original editorial source](docs/evidence/2026-10-16-starshield.md).
- [Machine-readable claim and source register](data/evidence/starshield-restrictions-2026-10-16.json) — source IDs, per-claim classifications, denials, independence and copyright notes.

The public website features this reporting on both the homepage and `/research/`. **This is a sourced editorial brief, not an independently verified finding that a named individual ordered the restriction.** The original publishers retain their articles and imagery. The JSON is **staged for future Parallax RELAY import but has not been ingested into a connected RELAY service**. Review, corrections and date updates are required as new reporting emerges.


## SPACEЖ RELAY public evidence workspace

The `/relay/` site publishes two real cases with **20 claims, 17 source records and 8 open questions**. The UNHCR winter-aid comparison opens first: its 13 claims and nine source records compare the September 2024 plan with reported delivery, document funding and rollout context, and preserve the unresolved cash shortfall and generator-count difference. The Starshield dossier remains available with allegations, denials and source dependencies intact.

The UNHCR case includes seven comparisons, five recorded AI source reviews, a Git-verified baseline, one wording clarification, one generator-cutoff correction and eight evidence additions. Reviews are bound to exact claim snapshots; they do not claim human approval or independent verification with recipients. See the [source comparison](docs/evidence/2026-10-17-unhcr-winter-delivery.md), [cash and generator follow-up](docs/evidence/2026-10-17-unhcr-followup.md) and [history rules](docs/SPACEZH_RELAY_OSINT_RFC.md).

The interface uses direct labels: Cases, Claims and supporting sources, Open questions, Updates and corrections. It displays reporting periods, source locators, missing results and the difference between content review and HTTP access.

- [Architecture RFC and source-protection boundaries](docs/SPACEZH_RELAY_OSINT_RFC.md)
- [Concrete implementation plan and next release gates](docs/RELAY_IMPLEMENTATION_PLAN.md)
- [Local verification record and before/after screenshots](docs/RELAY_QA.md)
- [Original owner-supplied planning draft](docs/reference/spacezh-relay-planning-rfc.md)
- [Canonical case registry](data/relay/cases.json), [source content reviews](data/relay/source-reviews.json), and [actual HTTP access receipts](data/relay/retrievals.json).
- [Explicit source access checker](scripts/ingest_relay_sources.py), [publication builder](scripts/build_relay_publication.py), and generated [cases](public/relay/data/cases.json), [receipts](public/relay/data/retrievals.json), and [SHA-256 manifest](public/relay/data/manifest.json).
- App: `public/relay/index.html`, `public/assets/relay.css`, `public/assets/relay.js`.

To refresh source access receipts, explicitly run `python scripts/ingest_relay_sources.py`. It makes HTTPS GET requests only to allowlisted public publishers, records actual timestamps, status codes, byte counts, and response hashes, and appends a run to `data/relay/retrievals.json`. It hashes response bodies in memory without archiving or republishing full articles. This is a manual command, not a background daemon or a factual verdict. The latest 17 October run attempted 21 URLs: twelve returned HTTP 200; nine were unavailable (four Reuters 401 responses, Telegraph 402, AP 403, IAEA 403 and two UNHCR 403 responses). Web-research content access is recorded separately and may differ from this command's transport results.

History validation reads the preserved baseline Git object. Use a full clone, or fetch that recorded commit before checking a shallow checkout. CI checks out full history.

After a case, source review, or receipt change, regenerate and verify the publication:

```bash
python scripts/build_relay_publication.py
python scripts/check_relay_publication.py
python -m unittest discover -s tests -v
python scripts/check_research_publication.py
python scripts/check_evidence_brief.py
python -m http.server 8080 --directory public
```

Open `http://localhost:8080/relay/`. Browser filters and shareable case/claim URLs do not save or publish edits. The builder attaches access receipts to sources and emits static public JSON. Hashes identify response or export bytes, not truth or reviewer approval. Actual revision records and Git support inspection; they do not form a tamper-proof evidence vault. Validation rejects fictional public cases, restricted records, unknown references, and inconsistent revision/correction history.

The static public site and RELAY workbench are [deployed and verified](docs/PRODUCTION_DEPLOYMENT.md). No confidential intake, continuous ingestion service, public tipline, operational warnings, external tracking, access-control backend, or payments are implemented. A later Laravel + React/Inertia application with Postgres, authenticated review and tested public projection belongs in a separately deployable project; see the RFC before extending this static workspace.
