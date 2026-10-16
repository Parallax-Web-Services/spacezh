# SpaceЖ — The sky belongs to everyone

Public site and founding proposal for SpaceЖ, an open-source public-interest initiative proposed in support of the **global defense of Ukraine** through auditable satellite intelligence and resilient communications research.

**Status:** public working proposal, not an established nonprofit, operational satellite network, or live warning service. No donations are being accepted through this repository.

## This site

The homepage at `/` links to a designed, complete public founding proposal at **`/plan/`**, sourced from [the Markdown proposal](docs/FOUNDING_PROPOSAL.md). No live payment processing is implemented.

The deployable static website lives in **`public/`**: `public/index.html`, `public/plan/index.html`, `public/assets/favicon.svg`, and `public/assets/spacezh-hero.webp`. Repository-level `docs/` and `CONTRIBUTING.md` are project documentation, not public web assets. No build tools, npm dependencies, analytics, third-party scripts, or backend. The launch design, responsive CSS, animated synthetic scanner, and original artwork have been preserved.

To preview locally:

```bash
python3 -m http.server 8080 --directory public
```

Visit http://localhost:8080 and http://localhost:8080/plan/. **Set the hosting site's document root / publish directory to `public/`** (not the repository root), so `index.html` is served at `/` and `assets/*` resolves at `/assets/*`. For nginx, point `root` to the full filesystem path of the `public` folder; for a static host, use `public` as the publish directory with no build command. The live canonical domain is `https://xn--80akd1bg1j.com/`.

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
