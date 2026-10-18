# SPACEЖ — The sky belongs to everyone

**Ballistic early-warning research for Ukrainian civilian protection.**

**Public founding proposal | Version 0.5 | 17 October 2026**

> Working proposal for public comment. SpaceЖ is not represented here as an established nonprofit, an operational satellite constellation, or an approved securities offering.


> **A call to build** — SpaceЖ focuses on ballistic early-warning research for Ukrainian civilian protection. This is an invitation to contribute public documentary research, data-access analysis and scientific review. No outside organization is presumed to have endorsed this proposal.


---


## 01  |  Executive thesis

**Ukraine is why SpaceЖ exists.** Its current mission is **ballistic early-warning research for Ukrainian civilian protection**. The immediate work is a public documentary feasibility and data-access assessment. SpaceЖ has no demonstrated ballistic sensing capability or live warning service.

**Our premise:** A useful research programme must establish what evidence exists, what data can be accessed lawfully, what those records can support, and what remains unproven. Public records, software and mathematical models must each be described according to what they actually demonstrate.

SpaceЖ is a proposed open-source, public-interest initiative. Its next deliverable is a sourced assessment of published early-warning evidence, data-access conditions, upstream dependencies, validation limits and unresolved feasibility questions. The existing studies supply mathematical and methodological background, not real sensing results. SPACEЖ RELAY supports source review, publication and corrections; its general investigations and UNHCR case are existing supporting work. ECHO, ARRAY and PARALLAX remain proposed workstreams to assess against the research mission, with no validated warning architecture or committed hardware programme.


The 60-second objective and complete independence from U.S. sensing and indispensable operating services in the earlier studies remain **provisional research criteria to validate**. They are not newly confirmed requirements or achieved performance. No new sensor access, real sensing dataset, qualified external review, institutional partner or operational capability is claimed.

> **Operating sequence** — Document the public evidence and access conditions; publish the feasibility assessment and unresolved questions; seek qualified scientific and Ukrainian civilian-protection review; choose any further research only from the resulting evidence and an approved scope.


### Existing publication tools

SPACEЖ RELAY v0.1 is an existing supporting publication tool: a published, read-only public evidence workspace with two real cases, 30 claims, 31 sources and eight open questions. The UNHCR winter-aid case currently opens first in that viewer with 23 claims and 23 sources, comparing targets with reported delivery. Expanding that inquiry is not the programme priority. Public records document technical payment problems, regional resource limits and a court-upheld local registration failure. They include UK grant agreements, a donor review and one signed generator transfer. These do not apportion the national cash shortfall or reconcile the generator-count difference. Its history preserves five revisions and eleven attributed AI reviews, with one clarification, one correction and eighteen evidence additions. The Starshield dossier preserves allegations, denials and unresolved questions. Claim details, source locators, timelines, access receipts, actual AI reviews and revision records let readers inspect the sources and changes. AI reviews do not claim human approval or independent delivery verification. The architecture and delivery plan are recorded in [the RELAY OSINT RFC](SPACEZH_RELAY_OSINT_RFC.md) and [the implementation plan](RELAY_IMPLEMENTATION_PLAN.md).


### Our founding promises

- Open work by default: source code, design discussions, milestones, and financial reporting are public, subject to security and privacy limits.
- Public-benefit stewardship: donors may sponsor deliverables but may not purchase exclusive control of the mission.
- Interoperability first: build on SatNOGS and other established open projects; do not create a proprietary replacement simply to own the ecosystem.
- Defense through public infrastructure: support Ukraine's civilian resilience, independent information access, scientific transparency, and lawful open-source verification—not tactical targeting or claims of real-time missile detection.
- Ukraine-informed priorities: seek requirements and critical review from consenting Ukrainian civilian-protection and scientific participants; no partnership or endorsement is assumed.
- No false deadlines: orbital broadband is a distant ambition, not a funded or presently feasible deliverable.

### What this publication asks

This publication invites documentary researchers, data-governance specialists, scientific reviewers and Ukrainian civilian-protection contributors to critique a bounded research assessment. No invitation establishes a partnership, an access agreement, a funded role or permission to begin field operations.


---


## 02  |  The public-interest opportunity

The current public-interest question is whether independent ballistic early-warning research can establish a credible path to better civilian protection in Ukraine. The first assessment must distinguish documented capabilities, access restrictions, dependencies and missing evidence. Broader communications work remains supporting context: the International Telecommunication Union estimated that 2.2 billion people remained offline in 2025. [1] That statistic does not establish ballistic sensing capability or justify a spacecraft programme.


### Existing work we should strengthen, not appropriate

- **Libre Space Foundation / SatNOGS** An established open-source ground-station network with public observations and open hardware/software. SpaceЖ should interoperate with it rather than reinvent its receiver infrastructure. [2]
- **OpenSatCom** A European Space Agency activity implemented by Libre Space Foundation and collaborators to advance open-source development approaches for satellite communications. It provides relevant research and ecosystem experience—not an endorsement of SpaceЖ. [3]
- **SatNOGS Optical** An independently developed, open optical-observation project with published measurement data. It illustrates how public observatories can complement radio tracking. [4]

### The gap SpaceЖ could fill

SpaceЖ can make the early-warning research record easier to examine: what each public source claims, what it demonstrates, whether relevant data is accessible for evaluation, and which uncertainties prevent a defensible conclusion. A published gap or an access barrier is a valid finding. General investigations and communications products should not displace this specific research question.


> **Scope boundary** — Public orbital data and observations do not constitute a military-grade launch-detection or early-warning system. Community ground stations and terrestrial mesh links do not constitute a Starlink-class broadband replacement.


### Who benefits first

- Ukrainian civilian-protection and scientific contributors assessing the research question, evidence limits and appropriate review requirements.
- Researchers and reviewers who need an attributable public record of capability claims, data-access conditions, dependencies, disputes and corrections.
- Universities and educational contributors examining reproducible methods and the limits of the existing mathematical studies.
- Researchers and journalists who need source-linked explanations of what the programme has and has not established.
- Humanitarian and resilience contributors offering civilian-safety context without assuming a warning service or organizational endorsement.
- Software contributors maintaining accessible publication, source provenance and the public research record.

---


## 03  |  The open architecture


### Four workstreams, sequenced by proof

These four proposed workstreams are supporting options, not an established early-warning system design. Further development must address a documented need from the research assessment.

- **SPACEЖ ECHO** Public orbital-intelligence software: catalog ingestion, licensed observation feeds, 3D orbital visualization, historical playback, event provenance, uncertainty, and accessible APIs.
- **SPACEЖ ARRAY** Reproducible node packages: ground-station setup, equipment profiles, health telemetry, privacy controls, hardware documentation, and SatNOGS-compatible contributions wherever licensing permits.
- **SPACEЖ RELAY** A proposed civilian investigation, evidence, human-review, controlled-sharing, and public-corrections platform. The first release uses real public-source cases; minimal synthetic records remain only in unit tests. Transport/Interoperability remains an optional, separately gated research area for lawful terrestrial transport, delay-tolerant messaging, simulation, and authorized-link evaluation; no satellite connectivity is assumed.
- **SPACEЖ PARALLAX** A gated feasibility track for a hosted payload or small satellite with a qualified mission partner. No launch contract, satellite capacity, or service availability is assumed.

### Suggested technology foundation

The existing static publication at `/relay/` supports browsing, source links and locators, claim details, unresolved questions, timelines and actual revision history without a backend or confidential intake. Reuse it where useful to publish the research record. A proposed Laravel, React/Inertia and PostgreSQL authoring application is deferred behind the current assessment. Software choices do not establish data access or early-warning feasibility.

The explicit source access checker makes allowlisted public HTTPS GET requests and appends actual timestamps, HTTP status, byte counts and response hashes to the access receipts. Consult the recorded runs for transport outcomes rather than treating an earlier summary as current. Response bodies are hashed in memory without full-article archiving or republication. This manual command is not a background daemon or a factual verdict. AI-assisted content reviews dated 17 October 2026 separately record what was read through originals, syndications, republications or indexed content; they are not human editorial signoff. The publication builder attaches receipts to sources and exports cases, receipts and a manifest.

The [real-source registry](../data/relay/cases.json), [source content reviews](../data/relay/source-reviews.json), [HTTP access receipts](../data/relay/retrievals.json), and [source access checker](../scripts/ingest_relay_sources.py) make that work inspectable. The fictional public case and simulated reviewers have been removed from the published bundle.

### SPACEЖ RELAY and the Parallax ecosystem

SPACEЖ RELAY owns the investigation product, editorial decisions, case access policy, and publication review. **Parallax RELAY** is the intended reusable ingestion, normalization, provenance, and publication layer beneath it. Reuse documented interfaces and export formats before duplicating that machinery; no connected integration is claimed by the static prototype.

The six proposed ecosystem roles remain distinct: **Slipstream** for scoped engineering and review gates; **Plexus** for permissioned identity and collaboration; **Positronic** for structured analysis; **Parallax RELAY** for reusable ingestion/publication; **HOLO** for permitted preservation and media; and **Continuum** for human-owned approval and institutional stewardship. These are intended relationships, not deployed integrations, partnerships, or public affiliation claims.

### Editorial and source-protection boundaries

Separate what a source observed, what it claims, and what an analyst infers. Record supporting, contradicting, and ambiguous evidence without counting syndication as independent corroboration. Human review precedes publication; updates, corrections, and withdrawals preserve an attributable revision history. AI may propose clustering and cross-references, but cannot declare truth or approve publication.

Confidential voluntary submissions are outside v0.1. Do not collect secret tips, expose contributor identities or sensitive locations, or copy restricted material into a public graph or static bundle. Any future intake requires a separate source-protection threat model, expert security/privacy/legal review, trained operations, and a decision about a professionally operated submission system or trusted partner. No anonymity guarantee, government affiliation, or warning capability is made. Ballistic early-warning research is the programme priority; any future operational warning function remains outside RELAY and requires its own authorized civilian-protection scope.


### Source provenance and verification

- Every observation carries a source, capture time, ingest time, license, checksum, and any transformation history.
- Separate measurements, predicted orbits, reporting, analysis, and simulation; never quietly promote inference to fact.
- Honor dataset redistribution licenses, source rate limits, opt-in station consent, and any operator location privacy.
- Keep an offline-capable documentation and deployment path; open standards and exportable data minimize lock-in.

> **Design test** — Can an independent reader trace each research conclusion to its public sources, distinguish available evidence from missing data, and reproduce the analysis where permitted inputs exist? If not, the assessment needs more work.

For the first RELAY release, an independent reader must be able to trace each key proposition to source locators, inspect contrary evidence and unresolved questions, distinguish AI-assisted content review from HTTP access and human editorial signoff, and understand every actual correction.


---


## 04  |  Delivery roadmap and gates


### Days 1–30  •  Document the evidence

- Maintain a public source and access register for the early-warning research assessment, recording source scope, dates, licenses, dependencies and unresolved questions.
- Define the assessment questions and distinguish inherited provisional criteria from confirmed requirements. Preserve the existing RELAY cases and actual corrections as supporting publication history.
- Publish what relevant evidence is publicly documented, what data access is established, and what access or evaluation remains unavailable. Do not infer access from an institutional programme description.
- Publish a donation/contracting policy draft before accepting organizational funds.

### Days 31–90  •  Publish the assessment

- Publish a documentary feasibility and data-access assessment, including contradictory records, access restrictions, source dependencies and conclusions that the evidence cannot support.
- List the specific questions needing qualified scientific and Ukrainian civilian-protection review. Report whether review has actually occurred; do not substitute AI source checks for it.
- Use the assessment to decide whether further research is justified and what a separately approved scope would need. Defer general authoring software, field work and hardware procurement.
- Publish monthly financial and technical updates, even if money raised is zero.

### Months 4–12  •  Review further research

- Reassess the research question after actual review and any lawfully obtained evidence. Retain unresolved or negative findings rather than promising a capability.
- Maintain accessible research publication, source provenance and actual correction history. Extend RELAY only for a documented supporting need and an approved scope.
- Consider ECHO or ARRAY research only where the assessment identifies a justified contribution, with separate resources, responsibilities and review.
- Keep communications demonstrations and operational warning work outside this assessment; neither follows automatically from a publication milestone.

### Months 12–30  •  Retain the orbital gate

- No orbital mission is committed by this roadmap. Any later proposal must first establish its purpose, evidence, engineering case, spectrum and safety plans, independent review and costs.
- Proceed only if required approvals, appropriate partners, funds, operational responsibilities, and mission safety are demonstrably in place.

> **Go / no-go rule** — Complete and review the documentary assessment before deciding on further work. A published page, mathematical test or product proposal does not establish sensing capability or justify spacecraft procurement.


---


## 05  |  Funding and sustainability

### Bootstrap first. Scale when justified.

SpaceЖ does not need a funding round to begin. It needs working software, credible research, committed contributors, and independently reproducible results. Start with open-source software, public datasets, commodity computing, available infrastructure, and voluntarily contributed expertise—not hypothetical financing.

**Our operating principle: prove it, then pay for it.** This is a proposed plan, not a claim that funds, equipment, sponsors, or contributors have been secured.

### First 90 days  •  Up to $2,000 discretionary cash

The immediate deliverable is a public documentary feasibility and data-access assessment with source provenance, explicit uncertainties and review questions. Existing mathematical tests remain background methods; they do not substitute for real sensing evidence. No deployed warning system, commissioned ground-station network, satellite link or spacecraft is promised.

| Use | Discretionary cash allowance |
| --- | --- |
| Source control, documentation, collaboration | $0 |
| Public datasets and simulation tools | $0 |
| Development infrastructure and compute | $0–$300 |
| Demo hosting and storage | $0–$300 |
| Optional prototype and testing equipment | $0–$1,000 |
| Contingency | $0–$400 |
| **MAXIMUM discretionary cash spend** | **$2,000** |

These are **spending ceilings, not money raised or purchase commitments**. The default is $0 wherever available resources suffice. The cap excludes the economic value of contributed labor. Paid engineering, professional legal or security review, regulated communications activities, field deployments, and orbital hardware must have separately funded and approved scopes before proceeding.

### Funding follows demonstrated progress

1. **Build with what we have.** Release source, data provenance, repeatable simulations, and documentation before buying equipment.
2. **Sponsor specific milestones.** Price an auditable integration, permitted ground-station pilot, independent review, dataset, or equipment purchase before asking anyone to fund it. Show deliverables and outcomes.
3. **Earn revenue where appropriate.** Optional engineering services, integrations, hosted infrastructure, deployment assistance, training, support, and research contracts can support maintainers while the open-source core remains accessible.
4. **Expand only when funded.** Larger hardware pilots, paid positions, regulated radio work, and orbital feasibility require secured resources, qualified reviews, and legal approvals—not optimistic projections.

### Year one  •  No imaginary runway

There is **no arbitrary annual fundraising target**. Publish actual receipts, approved expenditures, donated infrastructure, milestones, and outcomes. Each new project should have its own scope, budget, responsible party, and go/no-go review. Volunteer time is valuable but not an unlimited free staffing plan; compensate contributors when funding permits and disclose compensation and related-party transactions.

Open software, portable infrastructure, clear documentation, and replaceable vendors keep the project useful even if a sponsor disappears. Public-interest access must not depend on a paid relationship, and any revenue or sponsorship must not buy exclusive control of the open core.

No contributions or checkout are live through this publication. Any future donation or sponsorship acceptance must identify the legal recipient, payment and refund terms, tax status, and required disclosures beforehand.

**We do not need permission to begin. We need proof worth supporting.**

---


## 06  |  Governance and accountability


### Proposed legal shape

SpaceЖ begins as a public working proposal, not as an already incorporated foundation. The preferred destination is an independent nonprofit or comparable public-benefit steward with transparent rules and a separately contracted service ecosystem. The eventual jurisdiction and entity type need legal review.

- An interim steering committee with public minutes; transition to an independent board when legally formed.
- A majority of governors independent of any single sponsor or commercial vendor; conflicts disclosed and recusal required.
- No purchasing of board votes or veto powers through philanthropy; donor support does not confer control.
- Public roadmap votes and RFCs for non-sensitive technical decisions; legally reserved decisions remain with accountable human officers/directors.
- Published transactions, contributor compensation, procurement conflicts, and annual reports when operational.

### Proposed openness policy

Adopt OSI-approved software licenses, with Apache-2.0 considered for libraries/SDKs and AGPL-3.0 considered for network-hosted core services. Consider CERN-OHL-S v2 for original open hardware. Data licenses must follow upstream terms (including attribution/share-alike where required), privacy commitments, and contributor permissions. No final license policy is adopted merely by this proposal. [5]


### Civic and scientific safeguards

- SpaceЖ supports the global defense of Ukraine through lawful public-interest technology. Public releases focus on civilian resilience, humanitarian, educational, and scientific uses; they will not provide direct tactical targeting or live threat cueing.
- Do not publish exact positions of sensitive volunteer stations without informed consent.
- Disclose uncertainty and correct errors visibly; public claims require source links and a defined confidence standard.
- Conduct security review before launching messaging features, especially those used in crisis conditions.
- Release public documentation without assuming all radio transmissions, encryption practices, or cross-border hardware transfers are permitted.

> **Governance promise** — The right to inspect, reproduce, and improve the work must survive the founders, funders, and any commercial operator.


---


## 07  |  Regulatory and execution realities


### Licensing is not optional

U.S.-jurisdiction spacecraft and earth-station activities can involve FCC authorizations, including Part 25 and streamlined small-satellite pathways when eligible; global satellite radio systems involve national administrations and International Telecommunication Union coordination. Launch providers and operators must satisfy the relevant launch rules. Export-controlled hardware, technical data, and cross-border collaborations demand case-specific legal review. [6–9]


### Major risks and responses

| Risk | Operating response |
| --- | --- |
| Confusing observation with broadband | Publish a capability matrix on every milestone; no unsupported service claims. |
| Spectrum/launch barriers | Gate spaceflight on qualified legal and engineering reviews; use licensed partners. |
| Misleading or sensitive OSINT | Label predictions vs observations; preserve provenance and privacy defaults. |
| Duplicating existing open projects | Build adapters and upstream improvements before creating competing stacks. |
| Single-donor capture | Cap donor control; publish conflicts, funding concentration and procurement. |
| Volunteer burnout / security debt | Fund maintainers and documentation; maintain security and incident processes. |


### First-year public scorecard

- Public repository and license inventory, visible issue backlog, documented builds, and monthly published progress.
- Publish the ballistic early-warning feasibility and data-access assessment first; report source scope, established access, missing evidence, provisional criteria, actual review and corrections. Keep general investigations and proposed products supporting this priority.
- Report actual pilot installations, external reviews, and institutional demonstrations as achieved instead of promising adoption quotas.
- A public source-quality report, privacy policy, maintenance/security response plan, and proposed governance charter.
- Ukrainian-language resources and voluntarily solicited input from Ukrainian research and civic contributors, without implying any endorsement before confirmation.

> **What success is not** — Success is not a valuation, an impressive rendering, an unverified satellite map, or a promise to challenge commercial constellation throughput without a credible link budget.


---


## 08  |  Sources and assumptions

The external facts below support the problem framing, existing open ecosystem, and regulatory discussion. All forecasts, budget ranges, adoption targets, governance choices, and implementation details elsewhere in this proposal are SpaceЖ planning assumptions—not verified third-party commitments.

1. [ITU — Facts and Figures 2025 (2.2 billion offline in 2025)](https://www.itu.int/en/ITU-D/Statistics/Pages/facts/default.aspx)
2. [Libre Space Foundation — SatNOGS project](https://www.libre.space/projects/satnogs/)
3. [OpenSatCom — About the ESA-supported activity](https://opensatcom.org/about-us/)
4. [Libre Space Foundation — SatNOGS Optical](https://www.libre.space/projects/satnogs-optical/)
5. [Open Source Initiative — Approved licenses](https://opensource.org/licenses)
6. [U.S. FCC — Small satellite and spacecraft licensing](https://www.fcc.gov/space/small-satellite-and-small-spacecraft-licensing-process)
7. [ITU — Regulation of satellite systems](https://www.itu.int/en/mediacentre/backgrounders/Pages/Regulation-of-Satellite-Systems.aspx)
8. [U.S. FAA — Commercial space launch licensing](https://www.faa.gov/space/licenses)
9. [U.S. BIS — Export Administration Regulations, Part 734](https://www.bis.gov/regulations/ear/734)

### Publication notes

Date of preparation: 16 October 2026. Named external organizations have not endorsed SpaceЖ merely because they are referenced here. No billionaires, government agencies, universities, or foundations are represented as committed supporters. The working name, governance model, legal status, trademark, and financing strategy are subject to public review.

SpaceЖ is presented as a proposed public-interest research initiative focused on ballistic early warning for civilian protection. The document does not establish sensing capability, reliable warning or communications coverage, tax-deductible donation eligibility, or an investment opportunity.


---


## 09  |  THE CALL TO ARMS

**Ukraine is why we begin. The world is invited to build.** The global defense of Ukraine also needs enduring, independent public knowledge and resilient infrastructure. SpaceЖ seeks verifiable contributions to that foundation, with honest limits on present capabilities.

A terminal. An antenna. A soldering iron. A laboratory. A classroom. A team. A contribution that can be audited.

If you build software, take ownership of an issue. If you know RF, review the node specification. If you run a university, host a research team. If you operate a station, bring it to the standards conversation. If you can fund public-interest work, sponsor a milestone without purchasing control. If you see a flaw in this plan, publish the critique.


### The immediate ask: a 30-day commitment

- Contribute: choose a task you can complete or review within 30 days.
- Validate: test the assumptions, licensing pathways, and technical architecture.
- Host: offer lab time, space, a permitted ground station, or educational pilots.
- Support: offer in-kind resources or discuss sponsorship of a priced milestone once a legal recipient exists.
- Govern: help design an independent, auditable public-benefit charter.

> **How to respond** — Reply to the public release with your role, an email or safe contact method, and the specific first-month deliverable you can own. Never post passwords, exact sensitive site coordinates, or other private details publicly.


---

# THE CALL TO ARMS

**Built for Ukraine's defense. Open to the world.**

This is a call for public engineering, independent verification, and civilian resilience—not a claim of deployed defense capabilities or a request for targeting support.

A terminal. An antenna. A soldering iron. A laboratory. A classroom. A team. A contribution that can be audited.

If you build software, take ownership of an issue. If you know RF, review the node specification. If you run a university, host a research team. If you operate a station, bring it to the standards conversation. If you can fund public-interest work, sponsor a milestone without purchasing control. If you see a flaw in this plan, publish the critique.

**The immediate ask: a 30-day commitment.**

Reply to the public release with your role, a safe contact method, and the specific first-month deliverable you can own.

**TO ARMS. TO WORK. TO ORBIT.**

**SPACEЖ — THE SKY BELONGS TO EVERYONE.**
