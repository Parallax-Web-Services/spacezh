# Production deployment

Verified 17 October 2026. This records the existing host before the RELAY release; it does not certify that the new release is live.

| Item | Verified value |
| --- | --- |
| Canonical site | https://xn--80akd1bg1j.com/ |
| Existing host | `slipstream.host` (`104.248.52.126`), matching the canonical domain's A record |
| nginx document root | `/home/forge/xn--80akd1bg1j.com/current/public` |
| Active release observed | `current` points to `releases/80475209` |
| Active Git commit observed | `d197c18` |
| Ownership and working tree | Forge-owned; tracked files clean; an untracked `.env` symlink exists |
| Website payload | Static `public/`; no application build or npm installation required |

The server uses a Forge-style release layout. The configured Forge deployment mechanism and whether pushes trigger automatic deployment have **not yet been verified**. Repository CI checks publication integrity; it is not a deployment confirmation.

## Publish an exact revision

1. Run the repository publication checks and relevant tests. Review the generated RELAY export and ensure it matches its canonical registry.
2. Commit and push the reviewed changes. Record the full Git commit SHA intended for production; use that exact SHA rather than the moving `master` branch tip.
3. On the existing host, record the resolved `current` target and its commit before making changes. Preserve that release and the existing `.env` arrangement.
4. Prepare a separate Forge-owned release from the exact intended commit. Confirm `git rev-parse HEAD` matches the recorded SHA and the release contains `public/index.html`, `public/relay/index.html` and the generated RELAY data. Do not overwrite a dirty checkout or copy the repository root into the public directory.
5. Run publication checks in the prepared release, then activate it through the verified existing deployment mechanism or an atomic switch of `current`. The nginx root already resolves through `current/public`; changing DNS or provisioning hosting is unnecessary.
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
