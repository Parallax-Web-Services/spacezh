# SPACEЖ — The sky belongs to everyone

**Global defense of Ukraine. Open infrastructure for the world.**

**Public founding proposal | Version 0.2 | 16 October 2026**

> Working proposal for public comment. SpaceЖ is not represented here as an established nonprofit, an operational satellite constellation, or an approved securities offering.


> **A call to build** — SpaceЖ begins with the global defense of Ukraine: an invitation to engineers, radio operators, researchers, Ukrainian civic groups, universities, and funders to help build auditable public infrastructure. No outside organization is presumed to have endorsed this proposal.


---


## 01  |  Executive thesis

**Ukraine is why SpaceЖ exists.** Its founding mission is the **global defense of Ukraine** through verifiable space intelligence, open technical infrastructure, and resilient communications research. This is a call for international technical cooperation—not a claim that we operate a satellite constellation, military warning system, or emergency communications network.

**Our premise:** Ukraine's defense and civilian resilience should not depend entirely on opaque, single-provider space infrastructure. The public deserves an interoperable alternative to concentrated private control of space-based communications and data. **We can begin building that alternative without pretending we can launch a broadband constellation tomorrow.**

SpaceЖ is a proposed open-source, public-interest initiative with Ukraine at the center of its purpose and international collaboration at the center of its approach. It would start by connecting trustworthy, licensed public satellite observations; producing an auditable orbital intelligence platform; and making community-operated ground infrastructure easier to deploy and use. Longer-term, it would pursue interoperable communications experiments and independently governed orbital capacity—only after engineering, regulatory, and financial milestones are met.


> **One-sentence strategy** — Open the data. Federate the ground. Prove the protocols. Earn the orbit.


### The first concrete product

A live public atlas of satellites and observations, paired with SpaceЖ Node: reproducible open software and documentation for compliant, opt-in ground stations. The product is useful on day one for educators, researchers, operators, journalists, and civic organizations.


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

Ukraine's defense is the founding purpose; public, inspectable infrastructure is the lasting international benefit. There is room for a cohesive, user-facing layer that makes open space observations discoverable, attributable, replayable, and useful to non-specialists, while connecting that software to a practical ground-node and future communications roadmap. SpaceЖ should win adoption through clarity, reliability, integrations, documentation, and accountable governance—not novelty claims.


> **Scope boundary** — Public orbital data and observations do not constitute a military-grade launch-detection or early-warning system. Community ground stations and terrestrial mesh links do not constitute a Starlink-class broadband replacement.


### Who benefits first

- Ukrainian researchers, civil-society and humanitarian groups seeking verifiable open-source context and lawful resilience technology, with privacy and safety safeguards.
- Universities, schools, and amateur-radio clubs that need accessible educational tooling.
- Researchers and journalists who need source-linked timelines and reproducible visualizations.
- Humanitarian and disaster-resilience organizations evaluating lawful, redundant communication options.
- Operators and makers who want interoperable equipment, software, test data, and clear contribution paths.

---


## 03  |  The open architecture


### Four workstreams, sequenced by proof

- **SPACEЖ ATLAS** Public orbital-intelligence software: catalog ingestion, licensed observation feeds, 3D orbital visualization, historical playback, event provenance, uncertainty, and accessible APIs.
- **SPACEЖ NODE** Reproducible node packages: ground-station setup, equipment profiles, health telemetry, privacy controls, hardware documentation, and SatNOGS-compatible contributions wherever licensing permits.
- **SPACEЖ LINK** An interoperable communications testbed, beginning with lawful terrestrial transport, delay-tolerant messaging, simulation, and interoperability evaluation. Actual satellite messaging depends on separately authorized links.
- **SPACEЖ ORBIT** A gated feasibility track for a hosted payload or small satellite with a qualified mission partner. No launch contract, satellite capacity, or service availability is assumed.

### Suggested technology foundation

Laravel for application APIs, ingest orchestration, access controls, queues, and a public ledger; React for research and operational interfaces; Babylon.js for immersive 3D orbit replay; PostgreSQL/PostGIS for spatial/event data; commodity object storage for versioned evidence; open exports and signed change history. These are implementation preferences, not claimed completed features.


### Trust is the actual product

- Every observation carries a source, capture time, ingest time, license, checksum, and any transformation history.
- Separate measurements, predicted orbits, reporting, analysis, and simulation; never quietly promote inference to fact.
- Honor dataset redistribution licenses, source rate limits, opt-in station consent, and any operator location privacy.
- Keep an offline-capable documentation and deployment path; open standards and exportable data minimize lock-in.

> **Design test** — Could an independent university fork the software, operate an authorized station, and validate one published observation without our permission? If not, we have not built a public alternative.


---


## 04  |  Delivery roadmap and gates


### Days 1–30  •  Publish the work

- Open a public repository, contribution guide, architecture RFC, source/license inventory, and issue tracker.
- Publish an initial 3D orbit viewer with clearly labeled predictions, source links, and replayable event examples.
- Recruit an interim advisory group covering ground stations, spectrum regulation, security, and nonprofit governance.
- Publish a donation/contracting policy draft before accepting organizational funds.

### Days 31–90  •  Prove the first value

- Release SpaceЖ Atlas alpha with a reproducible ingestion pipeline and downloadable evidence records.
- Document and demonstrate three authorized receiver/node pilots, using existing open projects where practical.
- Run an independent reproducibility review and publish an error log and privacy assessment.
- Publish monthly financial and technical updates, even if money raised is zero.

### Months 4–12  •  Earn a community

- Targets—not commitments: 20 opt-in pilot stations, 50 external code/documentation contributions, and two nonprofit or academic demonstrations.
- Stable public APIs, accessibility and localization, interoperability tests, and independent governance input.
- Demonstrate a store-and-forward communications prototype on authorized terrestrial links, explicitly without claiming orbital capacity.

### Months 12–30  •  Assess an orbital mission

- Publish link budgets, spectrum plan, deorbit plan, security design, independent technical review, and fully costed vendor/partner options.
- Proceed only if required approvals, appropriate partners, funds, operational responsibilities, and mission safety are demonstrably in place.

> **Go / no-go rule** — No orbital procurement on the strength of a viral post. The first release must be reproducible, useful, and independently reviewable before any spacecraft commitment.


---


## 05  |  Funding and sustainability

The illustrative first-year funding target is $300,000, including a $50,000 kickoff tranche for a 90-day proof of work. These are planning assumptions, not quotes, commitments, or evidence that the initiative is already staffed. They rely on a lean paid core complemented by voluntary contributions and in-kind support.


### 90-day kickoff  •  $50,000 total

| Use | Planning amount |
| --- | --- |
| Engineering / integration | $25,000 |
| Prototype ground hardware | $8,000 |
| Hosting / security / data | $5,000 |
| Legal and regulatory review | $7,000 |
| Documentation and outreach | $3,000 |
| Contingency | $2,000 |
| TOTAL | $50,000 |


### 12-month envelope  •  $300,000 total (kickoff included)

| Use | Planning amount |
| --- | --- |
| Software, protocol engineering, maintenance | $164,000 |
| Ground equipment and pilots | $36,000 |
| Hosting, data, security, audits | $21,000 |
| Legal, spectrum, export reviews | $31,000 |
| Community, translation, documentation | $24,000 |
| Contingency | $24,000 |
| TOTAL | $300,000 |

The 12-month amount excludes spacecraft manufacturing, launch, insurance, commercial spectrum acquisition, constellation operations, and any promise of satellite internet service. Those require separate feasibility work and potentially much larger financing.


### How the commons pays its bills

Early support would be philanthropic grants, sponsorship of named milestones, in-kind hosting and hardware, and university collaborations. Long-term options include optional managed hosting, commercial support and training—never exclusive ownership of the open core or undisclosed resale of user-location or surveillance data.

Any accepted donations, tax status, and payment channels depend on a properly established legal vehicle and professional review. The publication itself is a call for collaborators and nonbinding expressions of support.


---


## 06  |  Governance people can trust


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
- Three reproducible node pilots and a source-linked atlas alpha within the first 90 days (targets).
- 20 opt-in pilot stations, 50 external contributions, and two documented institutional demos by month 12 (targets).
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
- Support: offer a nonbinding pledge toward the independently administered $50,000 kickoff.
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