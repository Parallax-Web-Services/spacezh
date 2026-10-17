# SpaceЖ — The sky belongs to everyone

Public site and founding proposal for SpaceЖ, an open-source public-interest initiative proposed in support of the **global defense of Ukraine** through auditable satellite intelligence and resilient communications research.

**Status:** public working proposal, not an established nonprofit, operational satellite network, or live warning service. No donations are being accepted through this repository.

## This site

The homepage at `/` links to the designed public proposal at **`/plan/`** and the public coalition research/invitation at **`/coalition/`**. The [Markdown proposal](docs/FOUNDING_PROPOSAL.md) and [coalition strategy](docs/COALITION_STRATEGY.md) remain editable source documents. No live payment processing is implemented.

The deployable static website lives in **`public/`**: `public/index.html`, `public/plan/index.html`, `public/coalition/index.html`, `public/assets/favicon.svg`, and `public/assets/spacezh-hero.webp`. Repository-level `docs/` and `CONTRIBUTING.md` are project documentation, not public web assets. No build tools, npm dependencies, analytics, third-party scripts, or backend. The launch design, responsive CSS, animated synthetic scanner, and original artwork have been preserved.

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

## Roadmap

1. **Atlas:** A public, source-linked 3D atlas of satellite observations and predictions.
2. **Node:** Reproducible, opt-in ground-station tools interoperable with established open projects.
3. **Link:** Authorized terrestrial communications testbeds and simulation.
4. **Orbit:** Separately gated feasibility research for a hosted payload or spacecraft.

### Proposed funding envelope

The first 90 days are **illustratively budgeted at $50,000**. The first-year planning envelope is **$300,000, inclusive of kickoff**. These are estimates, not existing funding or offers of tax-deductible donation. GoFundYourself support checkout will be enabled only after legal and payment arrangements are approved and published.

## Maintaining visual integrity

The original `<style>` block in `public/index.html` has not been changed, and `public/assets/` is retained byte-for-byte. This change is content, metadata, links, and a **hidden** future GoFundYourself mount hook only. No visible payment form has been introduced.

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

**Important:** A public check on 16 October 2026 still returned the older parody version of the live domain, even though `master` had already been updated. Verify deployment of the `public/` folder and fresh content at all three routes before sharing partner links.

## Mobile layout and copy

The original embedded desktop CSS and design assets are preserved. A separate [mobile polish stylesheet](public/assets/mobile-polish.css), loaded after each page's existing styles, adjusts layouts **only at widths of 750px and below**. It removes the overflowing ribbon on phones, reduces section/card spacing, preserves 44px menu tap targets, and improves hero, buttons and proposal reading typography.

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

The public website features this reporting on both the homepage and `/research/`. **This is a sourced editorial brief, not an independently verified finding that a named individual ordered the restriction.** The original publishers retain their articles and imagery. The JSON is **staged for future RELAY import but has not been ingested into a connected RELAY service**. Review, corrections and date updates are required as new reporting emerges.
