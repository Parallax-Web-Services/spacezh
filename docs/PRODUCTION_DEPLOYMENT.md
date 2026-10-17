# Production deployment

## UNHCR cash and generator follow-up: verified production payload

Verified at 2026-10-17T21:26:41.239562+00:00. Forge automatically activated release `80484376` for commit `9880f84728de63889bb7c3a5f5e78e4058cbcd28`, with public tree `d80bfacb7ecff2ba08a1cb335c84e277e4d19fc1`. The preceding release `80483855` (`232f36b`) remains available for rollback. These identify the verified payload; a later documentation-only release may share the same public tree.

Both CI checks passed: [RELAY publication integrity](https://github.com/Parallax-Web-Services/spacezh/actions/runs/39070901411) and [research publication integrity](https://github.com/Parallax-Web-Services/spacezh/actions/runs/39070901495). The release passed 49 unit tests, publication/export checks, research-reader and evidence-brief checks, and JavaScript syntax validation.

[Live HTTP receipts](qa/unhcr-followup-2026-10-17/production-http.json) record 18 critical routes/assets returning HTTP 200 with bytes matching that exact commit. This includes the source registry, retrieval receipts, manifest, browser script and synchronized public plan. The case adds sourced cash funding and rollout context, corrects the unsupported generator cutoff and retains the unresolved causes and 76-unit difference. Five actual AI reviews and three revisions are published with reviewer conflicts and earlier wording preserved.

[Live case](https://xn--80akd1bg1j.com/relay/?case=ukraine-energy-civilian-resilience-2024#comparisons), [source note](evidence/2026-10-17-unhcr-followup.md), [release receipt](qa/unhcr-followup-2026-10-17/release-candidate.json).

Live browser checks passed at 1440px and 390px: both follow-ups and their source anchors work; the actual generator correction expands with preserved earlier wording; all three revisions and five AI reviews are visible. There was no page overflow or console warning/error. See [live browser findings](qa/unhcr-followup-2026-10-17/production-findings.json) and the production screenshots alongside that receipt.

## UNHCR delivery update: verified production payload

Verified at 2026-10-17T21:11:20.705667+00:00. Forge automatically activated release `80483794` for commit `a4e248e802700dfb5938060cbb67b5258eb76665`; the previous release `80483094` (`88afa7e`) remained available for rollback. These are the payload identifiers observed during this check; a documentation-only publication may produce a later release with the same `public/` tree.

Both CI checks passed: [RELAY publication integrity](https://github.com/Parallax-Web-Services/spacezh/actions/runs/39069802786) and [research publication integrity](https://github.com/Parallax-Web-Services/spacezh/actions/runs/39069802815). The release passed 46 tests. CI checks out full Git history so the preserved baseline commit can be verified.

[Live HTTP receipts](qa/unhcr-2026-10-17/production-http.json) show 18 critical routes/assets returning HTTP 200 with bytes matching the pushed commit. Live browser checks confirmed the direct heading “Public evidence and source checks,” the UNHCR case, seven comparisons, two unknown results, two attributed AI reviews, one clarification and five added-evidence records. Phone width 390px had no page overflow; its source note retained word spacing. Console checks returned no errors or warnings.

[Live comparison](https://xn--80akd1bg1j.com/relay/?case=ukraine-energy-civilian-resilience-2024#comparisons), [desktop proof](qa/unhcr-2026-10-17/production-comparisons.jpg), [phone proof](qa/unhcr-2026-10-17/production-comparisons-390.jpg), and [history proof](qa/unhcr-2026-10-17/production-history.jpg).

## Initial RELAY release record

Verified live on 17 October 2026, following the production push observed around 20:51 UTC. The existing Forge push hook activated the RELAY release from `master`.

| Item | Verified value |
| --- | --- |
| Canonical site | https://xn--80akd1bg1j.com/ |
| Existing host | `slipstream.host` (`104.248.52.126`), matching the canonical domain's A record |
| nginx document root | `/home/forge/xn--80akd1bg1j.com/current/public` |
| RELAY payload release verified | `releases/80483011`, observed through `current` |
| RELAY payload commit verified | `dd67d14ca52eea17a8d6c1a12a5c31d80c66370e` |
| Previous release retained | `releases/80475209`, commit `d197c18` |
| Ownership and working tree | Forge-owned; tracked files clean; an untracked `.env` symlink exists |
| Website payload | Static `public/`; no application build or npm installation required |

The existing Forge deployment hook automatically activated the pushed revision. Both GitHub publication checks succeeded ([RELAY](https://github.com/Parallax-Web-Services/spacezh/actions/runs/39068458889), [research](https://github.com/Parallax-Web-Services/spacezh/actions/runs/39068458807)). The active server release was checked independently against the exact pushed SHA.

These identifiers record the verified RELAY payload. A later documentation-only commit may create another Forge release with the same `public/` tree.

[Production HTTP receipts](qa/relay-2026-10-17/production-http.json) record 18 critical routes and assets returning HTTP 200 with response bytes matching the release's Git blobs, including the homepage, plan, research, coalition, RELAY data and manifest. Browser checks confirmed both cases work, no horizontal overflow at 390 CSS pixels, no broken homepage images and no console errors.

## Publish an exact revision

1. Run the repository publication checks and relevant tests. Review the generated RELAY export and ensure it matches its canonical registry.
2. Commit and push the reviewed changes. Record the full Git commit SHA intended for production; use that exact SHA rather than the moving `master` branch tip.
3. On the existing host, record the resolved `current` target and its commit before making changes. Preserve that release and the existing `.env` arrangement.
4. The existing Forge push hook prepares and activates a separate Forge-owned release. Confirm `git rev-parse HEAD` in that release matches the recorded SHA and the release contains `public/index.html`, `public/relay/index.html` and the generated RELAY data. Do not overwrite a dirty checkout or copy the repository root into the public directory.
5. Verify publication checks and activation through the existing deployment mechanism. The nginx root already resolves through `current/public`; changing DNS or provisioning hosting is unnecessary.
6. Confirm the active symlink resolves to the new release and its Git SHA still matches the intended revision. Keep the previous release until public verification is complete.

## Verify the public release

Use fresh, cache-bypassed HTTPS retrievals and a browser. Confirm successful responses, expected content and working local assets at:

- https://xn--80akd1bg1j.com/
- https://xn--80akd1bg1j.com/plan/
- https://xn--80akd1bg1j.com/coalition/
- https://xn--80akd1bg1j.com/research/
- https://xn--80akd1bg1j.com/relay/
- https://xn--80akd1bg1j.com/relay/data/cases.json
- https://xn--80akd1bg1j.com/relay/data/retrievals.json
- https://xn--80akd1bg1j.com/relay/data/manifest.json

Compare the downloaded manifest and data hashes with the prepared release. Check case selection, claim/source links and retrieval-failure labels, plus desktop and phone navigation. Record the activated SHA, release directory, activation time and results after verification. A successful CI run or push is insufficient evidence of publication.

## Roll back

If release checks fail, atomically restore `current` to the exact previously recorded release target using the same deployment mechanism. Verify that the resolved target, Git SHA and public pages match the prior release. Retain both releases and diagnostic results; do not delete the previous release during activation or rollback.
