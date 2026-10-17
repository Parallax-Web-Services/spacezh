# SPACEЖ RELAY — real-source verification record

## UNHCR delivery update and plain-language pass

The current registry has two real cases, 17 claims, 14 source records and eight open questions. The UNHCR comparison opens first. It adds seven plan/result comparisons, preserving the earlier 110-generator report alongside the later 186, and keeps unreported power-station and expenditure totals as unknown.

Two actual AI source reviews identify their methods, timestamps, scope and same-team limits. A Git-verified five-claim baseline carries no retrospective approval. Current snapshots preserve classification, wording, status, caveats, citations and locators. The log records one funding-wording clarification and five new evidence additions; it does not invent numerical mistakes or human approval.

Validation completed for this update: **46 tests passed**, deterministic export and source/history checks passed, the existing evidence brief and four research readers remain synchronized, and browser JavaScript syntax passed. A new real retrieval run attempted 18 public URLs: 11 retrieved and seven unavailable. Response bodies are not republished.

The UI now uses direct headings, including “Public evidence and source checks,” “Cases,” “Open questions,” and “Updates and corrections.” Comparisons retain units, periods and source locators. New claims explicitly have no earlier wording; imported and current revisions and AI review records are distinguishable.

Browser checks passed at 390, 820 and 1440 CSS pixels: no page overflow or console errors. Seven comparisons, two unknown totals, six actual changes, two AI reviews, source links and revision links were checked. [Desktop comparison](qa/unhcr-2026-10-17/comparisons-1440.jpg), [mobile comparison](qa/unhcr-2026-10-17/comparisons-390.jpg), [history](qa/unhcr-2026-10-17/history-1440.jpg), [reviews](qa/unhcr-2026-10-17/reviews-1440.jpg), and [browser results](qa/unhcr-2026-10-17/qa-results.json) record this pass.

Production release `80483794` at `a4e248e802700dfb5938060cbb67b5258eb76665` was verified after deployment. [Eighteen live file checks](qa/unhcr-2026-10-17/production-http.json) matched the commit exactly. The live browser confirmed seven comparisons, two unknown totals, six change records and two AI reviews. [Production comparison](qa/unhcr-2026-10-17/production-comparisons.jpg), [phone layout](qa/unhcr-2026-10-17/production-comparisons-390.jpg) and [history](qa/unhcr-2026-10-17/production-history.jpg) retain proof; the previous release remained available for rollback.

The initial release below is preserved as a dated record. Its counts and screenshots describe that earlier release.

**Updated:** 17 October 2026. **Branch:** `codex/relay-public-evidence`.

The fictional library case has been removed from the published registry. Synthetic records remain only in unit tests. The workbench opens on the real Starshield source dossier and also includes a historical civilian-energy case grounded in HRMMU, IAEA and UNHCR documents: **2 cases, 12 claims, 11 source records, 6 open verification questions**. Source records are not a count of independent investigations.

## Actual source work

- Reviewed the Starshield reporting through accessible original pages, public syndications/republications and indexed AP content. Four Reuters originals were inaccessible to direct retrieval; their public Reuters republications were inspected and fetched. The Telegraph original remained inaccessible, while the same Joe Barnes reporting was available through AOL. All copied source metadata and original caveats remain traceable to the dated editorial register.
- Downloaded and inspected the official HRMMU energy report and UNHCR winter plan and reviewed IAEA Update 247. Claims include precise document locators and distinguish documented reporting from direct observations, current conditions, and aid-delivery results.
- Executed `python scripts/ingest_relay_sources.py --timeout 15`: **15 real public URL attempts; 8 HTTP 200 responses fetched and SHA-256 fingerprinted; 7 unavailable** (four Reuters 401, Telegraph 402, AP 403, IAEA 403). These are the recorded results of that specific retrieval method. Public-web content access and the command's transport access can differ.
- The ingestion command appends a timestamped run to `data/relay/retrievals.json`. Source bodies are not republished or archived in the repository. Fingerprints identify the response bytes at that time, not factual truth or source authenticity.
- Content checks are explicitly AI-assisted. No human editorial approval, original interview, command-decision finding or correction history is invented. Syndications remain the same underlying reporting. Unresolved timing, technical-scope, authority, indirect-impact, recovery and aid-delivery questions form a cited verification queue.

## Checks

- **27 tests pass**: original provenance/revision tests plus publisher allowlisting, actual response-byte hashing, access failure handling, separation of HTTP access from claim verdicts, exclusion of synthetic public cases, required question citations and unavailable-response fingerprints.
- RELAY canonical/publication, source metadata and founding-plan fingerprint checks pass. Existing evidence and research publication checks pass; scientific model code is unchanged.
- JavaScript syntax and Git whitespace checks pass.
- Both real cases checked at **390, 750, 820, 1024 and 1440 CSS pixels**: no horizontal page overflow; correct case/source/question counts; no unexpected browser console warnings or errors.
- Verified default real case, record-type filtering, search/empty/reset behavior, primary-document locators, persistent claim deep links, reviewed-copy links, separate original/public-copy retrieval receipts and downloadable JSON receipt log.

## Current screenshots

- [Real Starshield dossier](qa/relay-2026-10-17/real-starshield-1440.jpg)
- [Reviewed source copies and access records](qa/relay-2026-10-17/real-source-access-1440.jpg)
- [Primary-source energy case on mobile](qa/relay-2026-10-17/real-energy-390.jpg)
- [Both real cases at all five widths](qa/relay-2026-10-17/real-evidence-layout.json)
- [Production Starshield dossier](qa/relay-2026-10-17/production-relay.jpg)
- [Production energy case at 390px](qa/relay-2026-10-17/production-energy-390.jpg)

## Site presentation before/after

The original Earth/Ukraine hero remains byte-identical (Git blob `e3d98ec377f9664138f11c3f83f7634ead508c20`). Supplied solidarity WEBP SHA-256: `e3e457e382203fb406e84bbe572da9f17d16f224f0ee2c6ef572037453eaa4ba`.

| Homepage | Before | After |
| --- | --- | --- |
| Mobile, 390px | [Before](qa/relay-2026-10-17/before-home-390.jpg) | [After](qa/relay-2026-10-17/after-home-390.jpg) |
| Tablet, 820px | [Before](qa/relay-2026-10-17/before-home-820.jpg) | [After](qa/relay-2026-10-17/after-home-820.jpg) |
| Desktop, 1440px | [Before](qa/relay-2026-10-17/before-home-1440.jpg) | [After](qa/relay-2026-10-17/after-home-1440.jpg) |

[Solidarity desktop](qa/relay-2026-10-17/solidarity-1440.jpg) and [mobile](qa/relay-2026-10-17/solidarity-390.jpg). The earlier fictional-interface screenshots are historical QA artifacts outside the public web root; they are not the current registry.

Production verification on 17 October 2026 confirmed Forge release `80483011` at commit `dd67d14ca52eea17a8d6c1a12a5c31d80c66370e`. [HTTP receipts](qa/relay-2026-10-17/production-http.json) record 18 critical routes and assets returning HTTP 200 with bytes matching the committed files. Live browser checks confirmed both cases work, no overflow at 390 CSS pixels, no broken homepage images and no console errors. See the [deployment record](PRODUCTION_DEPLOYMENT.md) for activation and rollback details. This verifies publication and documented public-source work; it does not establish an expert security review, legal determination, access-control service, confidential intake or warning capability. The retrieval command runs only when explicitly invoked; no recurring automation or deployed Parallax RELAY connection is implied.
