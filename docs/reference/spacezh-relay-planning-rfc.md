# SPACEЖ RELAY — Counter-Authoritarian OSINT Platform

**Status:** Draft planning RFC for review before Codex implementation  
**Date:** 17 October 2026  
**Repository:** `Parallax-Web-Services/spacezh` (`master`)

## 1. Product decision

Retain the established `SPACEЖ RELAY` name, but broaden the proposed product from only an interoperable communications testbed to a civilian, public-interest OSINT and verified information-sharing platform. Its mission is to document and challenge authoritarian abuses, information suppression, disinformation, and threats to civilian safety with source-linked evidence rather than unsupported assertions. Start with Ukraine; support globally reusable, auditable infrastructure over time.

**Distinct layers:**

- **SPACEЖ RELAY:** Investigation, analyst review, evidence, controlled sharing, public cases and corrections.
- **Parallax RELAY:** Reusable source ingestion, normalization, provenance, and publishing mechanics beneath the product; avoid duplicating its core functionality.
- **SPACEЖ ECHO:** Source-linked orbital intelligence, historical visualization, and provenance.
- **SPACEЖ ARRAY:** Lawful, opted-in and reproducible ground-station infrastructure.
- **SPACEЖ PARALLAX:** Separately authorized orbital/hosted-payload feasibility.

The original communications testbed remains an optional, separately gated **Transport/Interoperability** area under SPACEЖ RELAY, not an assertion of operating links or satellite connectivity.

The wider Parallax ecosystem has potential roles: **Slipstream** (scoped engineering and review gates), **Plexus** (permissioned collaboration), **Positronic** (structured data/analysis), **Parallax RELAY** (source ingestion/publication), **HOLO** (preservation/media), and **Continuum** (human-owned approvals and institutional stewardship). These are intended relationships, not claims of deployed integrations.

## 2. First audience and use cases

Initial users: journalists, human-rights monitors, Ukrainian civilian-resilience researchers, verification teams, open-source investigators and public-interest watchdogs. Others, including anti-war Russian citizens, may voluntarily contribute, subject to a separate safety review of confidential-source handling.

Version 0.1 should let analysts compile and publish one well-supported, revisable evidence case from already public material, with transparent citations, preserved original artifacts when legally permitted, and a clear correction history. The existing SpaceЖ Starshield evidence brief is a plausible **example content case**, but it must preserve its attributed reporting, denials, independent corroboration limits, and no unsupported conclusions.

## 3. Trust boundaries and editorial workflow

Separate two trust zones:

**Public-source OSINT:** legally accessible sources, dates and URLs; licensed artifacts and content fingerprints; source provenance; claim-to-evidence relationships; analyst reviews; publishable redacted outputs and corrections.

**Confidential voluntary submissions:** NOT part of the first public release. Never pipe unvetted tips into public content or the Plexus public graph. Require a written threat model, security/privacy/legal review, organizational capacity and source-protection processes before opening an intake route. Consider a professionally operated SecureDrop-class system or trusted external partner; do not invent bespoke anonymous submission infrastructure on the fly. VPNs and network bouncing do not establish anonymity against state-capable adversaries, and the platform must never promise it.

Suggested review lifecycle: `received (restricted if confidential)` → `triaged` → `needs corroboration` → `supported / disputed / unresolved` → `human-approved for publication` → `published / updated / corrected / withdrawn`. Distinguish a source's observation from its claim or an analyst's inference. AI can assist with clustering and proposed cross-references, never autonomously declare truth, deanonymize a contributor or trigger emergency alerts.

Public content must not publish unconsented identities, precise sensitive locations, live military movement, targetable military data, or operational sensor layouts. Do not solicit contributors to trespass, gain unauthorized access, approach military assets or take personal risks.

**Early warning is a separate safety-critical track:** SPACEЖ has *research* about independent ballistic-launch verification, but no operational detection system. No public warning origination, relay of unverified launch sightings as alerts, or claims of launch-detection capability. Official civilian warning authorities retain control of any future handoff, after formal review and approval.

## 4. Proposed data model

Core entities: `Source` (public provenance, source type, rights, timestamps); `Artifact` (original, license, fingerprint, safe storage); `Observation` (what was directly observed); `Claim` (precise proposition, status, uncertainty); `EvidenceLink` (supporting, contradicting, ambiguous); `Case` (investigation); `Review` (human attribution, rationale and conflicts); `Publication` (public revision); `Correction` (immutable changelog with cause); `AccessPolicy` (restricted/public lifecycle, explicit redactions).

The public-facing views are an **Evidence Ledger**, **Claim Details**, **Case Timeline**, and **Corrections Log**. A complete published case must show what is known, what remains disputed, what has been corrected, and the evidence for each key assertion.

## 5. SPACEЖ website design patch (independent small PR)

Do not replace the existing Earth/Ukraine hero artwork. Add a tasteful, clearly labeled **Solidarity** feature using the existing generated intertwined **white-blue-white Russian anti-war / Free Russia** and **EU** flags image, with Ukraine's **tryzub** retaining visual prominence. The white-blue-white flag is **not** the Russian Federation's state flag; the EU flag symbolizes solidarity, not institutional endorsement. This imagery is not a claim of official EU or Ukrainian governmental partnership.

Flag artwork supplied separately as `spacezh-solidarity-flags.webp` (1448 × 1086, approximately 153 KB). Copy into `public/assets/`, preserve aspect ratio, add meaningful alt text and responsive treatment. Prefer a separate mid-page section or framed feature, not a replacement for the original hero. Avoid oversized branding and generic stock gradients.

Improve the tryzub by comparing the current hand-authored local SVG against an authentic, legally reusable authoritative coat-of-arms vector. Keep line work crisp at small scales; avoid transforms/blur or tiny overcomplicated badges. The prior 820px-wide screenshot shows substantial clipping of right-side hero content: audit 390, 750, 820, 1024 and 1440 CSS pixel widths, remove horizontal overflow, and preserve image visibility and legibility. Keep functional mobile navigation and the existing bilingual `ЖИТТЯ = LIFE`, `ВОЛЯ = FREEDOM`, `НАУКА = SCIENCE` ribbon wherever it is displayed.

The homepage already presents SPACEЖ ECHO / ARRAY / RELAY / PARALLAX as proposed products and a six-product Parallax stack. Update the RELAY description only after the underlying RFC text is approved; do not present the platform as already deployed.

## 6. Incremental delivery, with human-owned scope

**Stage A — Site presentation PR:** flags / Solidarity section; accurate tryzub; responsive fixes; performance and accessible labels. No changes to backend, payment endpoints or existing safety disclaimers. Include mobile/desktop screenshots before and after.

**Stage B — Architecture RFC:** update `docs/FOUNDING_PROPOSAL.md` and related canonical plans, and synchronize the rendered `/plan/` static edition in the same PR. Add a separate `docs/SPACEZH_RELAY_OSINT_RFC.md` with the changed product boundary, source model, editorial workflow, source protection threat model, staged goals and exclusions. Preserve `SpaceЖ Relay` versus `Parallax RELAY` as distinct product names.

**Stage C — Non-operational v0.1:** source-linked case registry, evidence ledger and correction lifecycle using fully public or synthetic data. Keep the static publication available; discuss whether the application belongs in a separately deployable Laravel + React/Inertia project instead of mixing it into the static `public/` tree. Prefer open interfaces and Postgres-backed data with explicit access control when moving beyond a static proof of concept; do not invent live ingestion endpoints or collect secret tips.

**Stage D — Separately approved security review:** confidential-source intake and/or authorized civilian-safety routing only after expert threat modeling, secure operational staffing, legal approval and Ukrainian civilian protection input. No explicit date or public launch commitment now.

## 7. Acceptance and non-goals

- Site has original hero intact; three symbolic identities are readable and accurately described; assets load locally; no horizontal overflow; accessible on mobile.
- Four existing SpaceЖ product names and six Parallax ecosystem products remain correct and distinct.
- Public OSINT case transparently distinguishes facts, allegations, denials, inference and uncertainty, with preserved provenance and reproducible review.
- No new public tipline, real-time attack map, unauthorized threat warning, targeting feed, military sensor configuration, third-party tracking, payment checkout or claims of government affiliation.
- All claims of operational capability explicitly remain **research stage / proposed** until independently demonstrated and authorized.
- Proposed future secure intake includes source-protection review and separation from public/open datasets.

## 8. Standards and references

- UN OHCHR + Berkeley Human Rights Center: [Berkeley Protocol on Digital Open Source Investigations](https://humanrights.berkeley.edu/publications/berkeley-protocol-on-digital-open-source-investigations/).
- [WITNESS — Video as Evidence and ethical sharing](https://archiving.witness.org/archive-guide/resources/video-as-evidence/).
- [SecureDrop documentation and threat model](https://docs.securedrop.org/en/stable/threat_model/threat_model.html).
- Existing SpaceЖ repo: `docs/FOUNDING_PROPOSAL.md`, `research/002-independent-early-warning/README.md`, `research/003-observation-gap/REVIEW_PROTOCOL.md`, `docs/PLEXUS_NETWORK_HANDOFF.md`.

This document is a planning draft, not authorization to deploy sensitive features. Freeze the work packages with the project owner before handing the individual implementation stages to Codex.
