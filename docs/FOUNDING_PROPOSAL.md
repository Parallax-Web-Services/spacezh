# SPACEЖ — The sky belongs to everyone

**Global defense of Ukraine. Open infrastructure for the world.**

**Public founding proposal | Version 0.4 | 17 October 2026**

> Working proposal for public comment. SpaceЖ is not represented here as an established nonprofit, an operational satellite constellation, or an approved securities offering.


> **A call to build** — SpaceЖ begins with the global defense of Ukraine: an invitation to engineers, radio operators, researchers, Ukrainian civic groups, universities, and funders to help build auditable public infrastructure. No outside organization is presumed to have endorsed this proposal.


---


## 01  |  Executive thesis

**Ukraine is why SpaceЖ exists.** Its founding mission is the **global defense of Ukraine** through verifiable space intelligence, open technical infrastructure, and resilient communications research. This is a call for international technical cooperation—not a claim that we operate a satellite constellation, military warning system, or emergency communications network.

**Our premise:** Ukraine's defense and civilian resilience should not depend entirely on opaque, single-provider space infrastructure. The public deserves an interoperable alternative to concentrated private control of space-based communications and data. **We can begin building that alternative without pretending we can launch a broadband constellation tomorrow.**

SpaceЖ is a proposed open-source, public-interest initiative with Ukraine at the center of its purpose and international collaboration at the center of its approach. It would start with SPACEЖ RELAY: a civilian public-interest investigation and evidence platform for journalists, human-rights monitors, researchers, and verification teams. Its first release uses real public-source cases with claim-level citations, source locators, access receipts, and unresolved verification questions. SPACEЖ ECHO would add auditable orbital intelligence, and SPACEЖ ARRAY would make lawful, opt-in ground infrastructure easier to reproduce. Longer-term, separately gated communications experiments and orbital capacity depend on engineering, regulatory, and financial milestones.


> **Operating sequence** — Publish one revisable public evidence case; prove source provenance and human review; extend orbital intelligence and opt-in ground-station research; evaluate authorized communications links; consider orbital hardware only after independent review.


### The first concrete product

SPACEЖ RELAY v0.1 is a published, read-only public evidence workspace with two real cases, 30 claims, 31 sources and eight open questions. The UNHCR winter-aid case opens first with 23 claims and 23 sources, comparing targets with reported delivery. Public records document technical payment problems, regional resource limits and a court-upheld local registration failure. They include UK grant agreements, a donor review and one signed generator transfer. These do not apportion the national cash shortfall or reconcile the generator-count difference. Its history preserves five revisions and eleven attributed AI reviews, with one clarification, one correction and eighteen evidence additions. The Starshield dossier preserves allegations, denials and unresolved questions. Claim details, source locators, timelines, access receipts, actual AI reviews and revision records let readers inspect the sources and changes. AI reviews do not claim human approval or independent delivery verification. The architecture and delivery plan are recorded in [the RELAY OSINT RFC](SPACEZH_RELAY_OSINT_RFC.md) and [the implementation plan](RELAY_IMPLEMENTATION_PLAN.md).


### Our founding promises

- Open work by default: source code, design discussions, milestones, and financial reporting are public, subject to security and privacy limits.
- Public-benefit stewardship: donors may sponsor deliverables but may not purchase exclusive control of the mission.
- Interoperability first: build on SatNOGS and other established open projects; do not create a proprietary replacement simply to own the ecosystem.
- Defense through public infrastructure: support Ukraine's civilian resilience, independent information access, scientific transparency, and lawful open-source verification—not tactical targeting or claims of real-time missile detection.
- Ukraine-informed priorities: seek requirements and critical review from consenting Ukrainian researchers, civil-society, and humanitarian participants; no partnership or endorsement is assumed.
- No false deadlines: orbital broadband is a distant ambition, not a funded or presently feasible deliverable.

### What this publication asks

It seeks founding contributors, technical reviewers, station operators, institutional pilot hosts, governance stewards, and nonbinding financial expressions of interest. The goal is to build a credible public working group and a 90-day proof of work.


---


## 02  |  The public-interest opportunity

The International Telecommunication Union estimated that 2.2 billion people remained offline in 2025. Coverage, affordability, and meaningful access remain uneven. [1] Resilient communications matter during outages, disasters, displacement, and infrastructure failures. These are genuine public problems—but they do not imply that an amateur satellite network can provide consumer broadband at commercial constellation speeds.


### Existing work we should strengthen, not appropriate

- **Libre Space Foundation / SatNOGS** An established open-source ground-station network with public observations and open hardware/software. SpaceЖ should interoperate with it rather than reinvent its receiver infrastructure. [2]
- **OpenSatCom** A European Space Agency activity implemented by Libre Space Foundation and collaborators to advance open-source development approaches for satellite communications. It provides relevant research and ecosystem experience—not an endorsement of SpaceЖ. [3]
- **SatNOGS Optical** An independently developed, open optical-observation project with published measurement data. It illustrates how public observatories can complement radio tracking. [4]

### The gap SpaceЖ could fill

Ukraine's defense is the founding purpose; public, inspectable infrastructure is the lasting international benefit. There is room for a cohesive layer that makes public evidence discoverable, attributable, contestable, and revisable for non-specialists, while connecting source-linked orbital research to a practical ground-node and future communications roadmap. SPACEЖ RELAY would document authoritarian abuses, information suppression, disinformation, and civilian-safety concerns through evidence and accountable review. SpaceЖ should win adoption through clarity, reliability, integrations, documentation, and accountable governance—not novelty claims.


> **Scope boundary** — Public orbital data and observations do not constitute a military-grade launch-detection or early-warning system. Community ground stations and terrestrial mesh links do not constitute a Starlink-class broadband replacement.


### Who benefits first

- Ukrainian researchers, civil-society and humanitarian groups seeking verifiable open-source context and lawful resilience technology, with privacy and safety safeguards.
- Journalists, human-rights monitors, verification teams, and public-interest investigators who need claim-level evidence, visible disputes, and corrections.
- Universities, schools, and amateur-radio clubs that need accessible educational tooling.
- Researchers and journalists who need source-linked timelines and reproducible visualizations.
- Humanitarian and disaster-resilience organizations evaluating lawful, redundant communication options.
- Operators and makers who want interoperable equipment, software, test data, and clear contribution paths.

---


## 03  |  The open architecture


### Four workstreams, sequenced by proof

- **SPACEЖ ECHO** Public orbital-intelligence software: catalog ingestion, licensed observation feeds, 3D orbital visualization, historical playback, event provenance, uncertainty, and accessible APIs.
- **SPACEЖ ARRAY** Reproducible node packages: ground-station setup, equipment profiles, health telemetry, privacy controls, hardware documentation, and SatNOGS-compatible contributions wherever licensing permits.
- **SPACEЖ RELAY** A proposed civilian investigation, evidence, human-review, controlled-sharing, and public-corrections platform. The first release uses real public-source cases; minimal synthetic records remain only in unit tests. Transport/Interoperability remains an optional, separately gated research area for lawful terrestrial transport, delay-tolerant messaging, simulation, and authorized-link evaluation; no satellite connectivity is assumed.
- **SPACEЖ PARALLAX** A gated feasibility track for a hosted payload or small satellite with a qualified mission partner. No launch contract, satellite capacity, or service availability is assumed.

### Suggested technology foundation

Start with a static, read-only public case prototype at `/relay/`, using real public-source records and local assets. It supports browsing, source links and locators, claim details, unresolved verification work, timelines, and actual revision history without a backend or confidential intake. A later authoring application may be separately deployable with Laravel, React/Inertia, PostgreSQL, explicit access controls, and versioned evidence storage; Babylon.js and PostGIS remain possible tools for orbital research. These are implementation preferences, not claimed deployed services.

The explicit source access checker makes allowlisted public HTTPS GET requests and appends actual timestamps, HTTP status, byte counts, and response hashes. The latest 17 October 2026 run attempted 27 URLs: seventeen returned HTTP 200; ten were unavailable (four Reuters 401 responses, Telegraph 402, AP 403, IAEA 403 and three UNHCR 403 responses: the story, annual report PDF and global cash-monitoring PDF). Response bodies are hashed in memory without full-article archiving or republication. This manual command is not a background daemon or a factual verdict. AI-assisted content reviews dated 17 October 2026 separately record what was read through originals, syndications, republications, or indexed content; they are not human editorial signoff. The publication builder attaches receipts to sources and exports cases, receipts, and a manifest.

The [real-source registry](../data/relay/cases.json), [source content reviews](../data/relay/source-reviews.json), [HTTP access receipts](../data/relay/retrievals.json), and [source access checker](../scripts/ingest_relay_sources.py) make that work inspectable. The fictional public case and simulated reviewers have been removed from the published bundle.

### SPACEЖ RELAY and the Parallax ecosystem

SPACEЖ RELAY owns the investigation product, editorial decisions, case access policy, and publication review. **Parallax RELAY** is the intended reusable ingestion, normalization, provenance, and publication layer beneath it. Reuse documented interfaces and export formats before duplicating that machinery; no connected integration is claimed by the static prototype.

The six proposed ecosystem roles remain distinct: **Slipstream** for scoped engineering and review gates; **Plexus** for permissioned identity and collaboration; **Positronic** for structured analysis; **Parallax RELAY** for reusable ingestion/publication; **HOLO** for permitted preservation and media; and **Continuum** for human-owned approval and institutional stewardship. These are intended relationships, not deployed integrations, partnerships, or public affiliation claims.

### Editorial and source-protection boundaries

Separate what a source observed, what it claims, and what an analyst infers. Record supporting, contradicting, and ambiguous evidence without counting syndication as independent corroboration. Human review precedes publication; updates, corrections, and withdrawals preserve an attributable revision history. AI may propose clustering and cross-references, but cannot declare truth or approve publication.

Confidential voluntary submissions are outside v0.1. Do not collect secret tips, expose contributor identities or sensitive locations, or copy restricted material into a public graph or static bundle. Any future intake requires a separate source-protection threat model, expert security/privacy/legal review, trained operations, and a decision about a professionally operated submission system or trusted partner. No anonymity guarantee, government affiliation, or warning capability is made. Independent early-warning research remains a separate safety-critical track under authorized civilian-protection review.


### Source provenance and verification

- Every observation carries a source, capture time, ingest time, license, checksum, and any transformation history.
- Separate measurements, predicted orbits, reporting, analysis, and simulation; never quietly promote inference to fact.
- Honor dataset redistribution licenses, source rate limits, opt-in station consent, and any operator location privacy.
- Keep an offline-capable documentation and deployment path; open standards and exportable data minimize lock-in.

> **Design test** — Could an independent university fork the software, operate an authorized station, and validate one published observation without our permission? If not, we have not built a public alternative.

For the first RELAY release, an independent reader must be able to trace each key proposition to source locators, inspect contrary evidence and unresolved questions, distinguish AI-assisted content review from HTTP access and human editorial signoff, and understand every actual correction.


---


## 04  |  Delivery roadmap and gates


### Days 1–30  •  Publish the work

- Maintain the public repository, contribution guide, source/license inventory, and issue tracker; reconcile the founding proposal with the RELAY architecture RFC and implementation plan.
- Maintain the static real-source RELAY v0.1 with two source-linked cases, claim classifications, explicit disputes, source locators, access receipts, and unresolved verification questions. Record only actual revisions and corrections; report missing human editorial signoff honestly.
- Recruit an interim advisory group covering ground stations, spectrum regulation, security, and nonprofit governance.
- Publish a donation/contracting policy draft before accepting organizational funds.

### Days 31–90  •  Prove the first value

- Seek independent editorial and reproducibility review of the first RELAY case; publish the error log, source-quality assessment, correction policy, and privacy limits.
- Evaluate documented Parallax RELAY interfaces before planning a separately deployable authoring application; do not open confidential intake or invent a live ingestion service.
- Scope SpaceЖ Echo's source-linked orbital alpha and a SpaceЖ Array receiver recipe as subsequent proof-based milestones; validate permitted inputs and a consenting host or simulation before scaling.
- Publish monthly financial and technical updates, even if money raised is zero.

### Months 4–12  •  Validate community pilots

- Expand pilots and demonstrations only as willing hosts, maintained software, and separately approved resources become available.
- Extend RELAY only after public-case review: permissioned authoring, reviewed publication exports, accessible/localized views, and documented open interfaces, with funding and security ownership in place.
- Develop Echo/Array pilots, stable public APIs, interoperability tests, and independent governance input as separately scoped work.
- Demonstrate a store-and-forward communications prototype on authorized terrestrial links, explicitly without claiming orbital capacity.

### Months 12–30  •  Assess an orbital mission

- Publish link budgets, spectrum plan, deorbit plan, security design, independent technical review, and fully costed vendor/partner options.
- Proceed only if required approvals, appropriate partners, funds, operational responsibilities, and mission safety are demonstrably in place.

> **Go / no-go rule** — No orbital procurement on the strength of a viral post. The first release must be reproducible, useful, and independently reviewable before any spacecraft commitment.


---


## 05  |  Funding and sustainability

### Bootstrap first. Scale when justified.

SpaceЖ does not need a funding round to begin. It needs working software, credible research, committed contributors, and independently reproducible results. Start with open-source software, public datasets, commodity computing, available infrastructure, and voluntarily contributed expertise—not hypothetical financing.

**Our operating principle: prove it, then pay for it.** This is a proposed plan, not a claim that funds, equipment, sponsors, or contributors have been secured.

### First 90 days  •  Up to $2,000 discretionary cash

The immediate deliverable is a source-linked public software demonstration, reproducible tests, and documentation. We are not promising a deployed warning system, commissioned ground-station network, satellite link, or spacecraft.

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
- Real public-source SPACEЖ RELAY cases first; report review provenance, actual access evidence, unresolved questions, and actual correction history. Echo alpha and an Array receiver recipe follow their own approved proof gates.
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

SpaceЖ is presented as a proposed open public infrastructure initiative. The document is not a claim of completed construction, reliable communications coverage, planned missile detection, tax-deductible donation eligibility, or an investment opportunity.


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
