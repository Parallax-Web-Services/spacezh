# Independent peer review of SpaceЖ Research 001–004

**16 October 2026 · Review of repository commit `d13070e` and the live pages at `/research/` · Not an endorsement**

## Provenance of this review

This review was produced by Claude (Anthropic) at the maintainer's request, on the same day the four studies were published. The reviewer had no access to non-public material, no sensor data, and no contact with any organisation named in the studies. Every check below is reproducible from the public repository and public URLs; the maintainer decides what to accept. It is **not** the independent Ukrainian scientific review the studies ask for, and it does not change the studies' own status of *not demonstrated*.

## Verdict in one paragraph

The arithmetic is right, the tests pass, and the sources are real: every headline number reproduces from first principles, all 54 tests pass, and 15 of 18 study citations check out as labelled (two were mislabelled, one URL was dead, and one page carried a leaked template placeholder; all four are fixed in the commit that precedes this file). The weakness is not fabrication but *content*: the 60-second requirement that organises all four studies is asserted rather than derived, the "hard upper bound" is a tautology, the evidence register tests programmes that never claimed launch detection while omitting the sensing modalities a 60-second question actually turns on, and the statistical thresholds in Study 004 are invented inputs whose outputs are then reported to two decimal places. The studies are honest about being non-operational; they are less honest about being thin.

## 1. What reproduces

| Check | Result |
| --- | --- |
| `python3 -m unittest discover` for 001 / 002 / 003 / 004 | 6 / 9 / 15 / 24 pass (54 total, as claimed) |
| Study 001 reference case, recomputed independently from the stated assumptions | slant range 1 518.0 km, period 95.50 min, contact 6.49 min, FSPL 148.88 dB, received power −111.87 dBm, C/N₀ 58.13 dB·Hz, E_b/N₀ 18.30 dB, 467.3 kB: all match |
| Study 001 elevation sweep (5°/10°/15°/30°) | 9.82 / 7.94 / 6.49 / 3.79 min and 707 / 572 / 467 / 273 kB: all match |
| Study 002 PPV table (s = 0.99, f = 0.001) and Wilson lower bound for 100/100 | 9.0 % … 99.1 % and 96.30 %: match |
| Study 003 Fréchet bounds, 0.72 / 0.864 timely-probability example, chart table | match |
| Study 004: 59 / 299 / 2 995 zero-miss trials; 97.05 % for 100/100; 89.87 d; 368 and 110.67 d under a Bonferroni split of α = 0.05; 49.31 % for 8/10; 12.84 alarms/30 d for 0 alarms in 7 d; chart table | all match |
| Live pages versus repository HTML | identical modulo whitespace (the host minifies); all four `research-source-blob` fingerprints matched the committed Markdown |
| GitHub Actions "Research publication integrity" on `d13070e` | success |

## 2. Citation audit

| Study | Citation | Status |
| --- | --- | --- |
| 001 | NASA Small Spacecraft SOA, ground data systems | Reachable. Generic; not load-bearing. |
| 001 | CelesTrak "Orbital Coordinate Systems, Part II" (`v02n02`) | **Mislabelled.** Labelled "observer geometry"; Part II is coordinate systems. Observer look angles are Part III (`v02n03`). Fixed. |
| 001 | NASA/JPL DSN 810-005 handbook | Reachable, but a deep-space handbook is off-topic for a 437 MHz LEO link. |
| 002 | AP, 13 Oct 2026, Zelenskyy: no partner warning before the Kyiv ballistic strike | AP blocks automated fetch; the same AP story (same slug) is carried by the Washington Post and others. Claim confirmed, including the U.S. statement that intelligence sharing continued. |
| 002 | Reuters, 14 Oct 2026, Europe has no quick fix for U.S. satellite data | Reuters blocks automated fetch; syndicated copies confirm the story and the specific claim that Europe has no replacement for the U.S. Space-Based Infrared System. |
| 002, 003 | French MoD, JEWEL, 24 Oct 2025 | Confirmed: Franco-German letter of intent 15 Oct 2025; initial space-based early-warning capability targeted for the early 2030s. |
| 002, 003 | EDF ODIN'S EYE II factsheet | Confirmed: EDF 2022, "Studies, Design", 36 months, €90 M EU contribution, OHB coordinator. |
| 002 | EU SST remit page | Confirmed: collision avoidance, re-entry, fragmentation; no launch detection. |
| 002 | Lviv regional administration, Air Alert app | Page blocks automated fetch; the app is real and documented elsewhere. Source [6] is listed but never cited in the text. |
| 003 | EUSPA EU SST services | Confirmed (three services, none launch-related). |
| 003 | Légifrance, "military programming law, 16 August 2026, Article 57" | **Content confirmed, label wrong.** Loi n° 2026-791 of 16 Aug 2026 exists; its annexed report says the Nostradamus over-the-horizon radar could provide a first building block before 2030, to be completed before 2035 by a geostationary infrared detection satellite and mobile UHF alerting radars, as France's contribution to JEWEL. That text is in the annexed report approved by Article 1. Article 57 ratifies five old ordinances. Légifrance blocks automated retrieval; verified from the published law text and the Assemblée nationale's adopted text n° 325. Fixed. |
| 003 | EUSPA GOVSATCOM press release, March 2026 | Confirmed: initial Hub operations January 2026. |
| 003 | UK Space Agency – SSAU MoU, March 2026 | Confirmed: 18 March 2026, civil and commercial cooperation framework. |
| 004 | NIST exact binomial limits | Reachable and appropriate. |
| 004 | Cochrane Handbook v5.0.2 §16.9.4 at `training-noproxy.cochrane.org` | **Dead.** Host does not resolve; the archived page on the real host redirects away. Replaced by Hanley & Lippman-Hand, JAMA 1983, the primary source for zero-numerator bounds. |
| 004 | ISO 22322:2022 | Confirmed title and edition. Cited only as "context"; it supplies none of the thresholds used. |

No fabricated source was found. Note that the two most load-bearing factual claims (AP, Reuters) are behind bot-blocking and were confirmed only through syndication; a future reader without web access cannot check them from the page.

## 3. Defects fixed alongside this review

1. `/research/003-observation-gap/` rendered the literal text `ZZZHOLD0ZZZ` (a link-protection placeholder from the Markdown-to-HTML step) where the link to `source_register.json` belongs.
2. The Cochrane URL in Study 004 pointed at a hostname that does not exist.
3. The CelesTrak citation in Study 001 pointed at the wrong column.
4. The French law was cited as "Article 57"; see the audit table.
5. `scripts/check_research_publication.py` hashed working-tree bytes, so it failed on any checkout with `core.autocrlf=true` (it failed on the maintainer's own machine while passing in CI). It now hashes LF-normalised bytes, matching what git stores.

## 4. Substantive critique

### 4.1 The 60-second requirement is asserted, not derived

Every study is organised around *verified detection within 60 seconds of launch*, and nothing in the four documents says where 60 seconds comes from. It is not derived from flight time, from shelter-reaching time, from the existing air-raid alert chain's latency budget, or from any civil-protection source; ISO 22322 is cited as context but sets no such number. A requirement with no derivation cannot be falsified, so "60-second detection: NOT DEMONSTRATED" on the front page is a statement about an arbitrary threshold. The first thing an external reviewer will ask is "why 60?", and the answer has to be on the page. Either derive it (publicly available flight-time and warning-chain figures suffice for a first cut) or present it as a placeholder.

**Maintainer's response, 17 October 2026:** the threshold is the project's own operational target, set against ballistic flight times to Ukrainian cities of a few minutes. Study 002 now says so and invites challenge; the front-page wording stays by decision.

### 4.2 The "first hard upper bound" is a definition

P(D₆₀) ≤ P(C) follows from D₆₀ ⊆ C, which is how C was defined. It is correct, and it is a useful rhetorical point against dashboards, but it is not a result and the front page should not present it as "the research constraint". The same applies to Study 003's "hard results" 2 and 3 (interval arithmetic and selection bias): sound, elementary, and not findings.

### 4.3 The evidence register answers a question nobody asked, and skips the one that matters

Study 003's six-entry register evaluates EU SST (collision avoidance), GOVSATCOM (communications), a UK–Ukraine civil-space MoU, two future space-based warning programmes and one national roadmap against the criterion "does this establish 60-second launch verification today?" None of them claims to, so the finding "no reviewed public source establishes it" is guaranteed by the selection, not discovered by the review.

Meanwhile the modalities a 60-second question actually turns on are absent: ground-based air-surveillance and early-warning radar (Ukraine's own, and allied radars with coverage of the launch areas), over-the-horizon radar, infrasound and seismic networks (CTBTO infrasound stations have published launch detections), and distributed acoustic sensor networks of the kind Ukraine already fields against drones. The register's own best source makes the point: the French programming law names an over-the-horizon radar and mobile UHF alerting radars as the *first* European early-warning building blocks, with the infrared satellite coming later. A study titled "the independent observation gap" that never mentions radar has not looked at the gap.

The physics that decides the question is simple enough to publish. For a smooth-Earth, 4/3-refraction radar horizon with the radar at ground level, a target at ground distance *d* is visible only above altitude *h* ≈ *d*² / (2 · 4/3 · R⊕):

| Radar-to-launch-point distance | Minimum target altitude for line of sight |
| ---: | ---: |
| 200 km | ≈ 2.4 km |
| 300 km | ≈ 5.3 km |
| 500 km | ≈ 14.7 km |
| 700 km | ≈ 28.8 km |

A ballistic missile climbs through these altitudes early in boost, so time-to-first-radar-detection is set by radar siting and geometry, not by whether Europe has an infrared satellite. Whether that time plus track confirmation fits inside any particular budget is exactly the computation a feasibility study should contain, and it is the one that is missing. (This table uses public textbook geometry only; it says nothing about any specific sensor.)

### 4.4 Study 004 quantifies requirements it invented

The sample-size results are correct, but their inputs (≥ 99 % sensitivity, ≤ 1 expected false alarm per 30 days, 95 % joint confidence) are chosen by the authors, not taken from any warning authority or standard. "368 trials" and "110.67 days" are then reported to a precision the inputs do not support. Two further points:

* The Bonferroni split is a convention, not a necessity. The two bounds come from disjoint data (event trials versus non-event exposure); under independence the joint level is the product, giving 366 trials and 110.3 days. The difference is immaterial, which is the point: the headline numbers are sensitive to a bookkeeping choice at the ±1 % level and to the invented thresholds at the order-of-magnitude level.
* The study does not note that in the current war an event census of several hundred launches accrues in months (Study 002 itself quotes a single night with more than 39 ballistic missiles). The binding constraint is therefore not *n* but the iid and completeness assumptions the study rightly flags; say so, or readers will take 368 as the obstacle.

### 4.5 Internal inconsistency between 002 and 004

For 100 observed successes out of 100, Study 002 reports a 95 % Wilson lower bound of 96.3 % and Study 004 reports an exact one-sided Clopper–Pearson lower bound of 97.05 %. Both are correct, but they are different intervals at different sidedness for the same case, presented without reconciliation. Pick one convention and state it once.

### 4.6 Study 001 is disconnected from the thesis and stops short of a conclusion

* Nothing on the research page explains what a 437 MHz telemetry downlink has to do with ballistic early warning; 001 reads as a leftover from the earlier "satellite communications" framing of the site.
* It reports E_b/N₀ = 18.3 dB but never states a required E_b/N₀ for any modulation and coding, so the question it poses ("enough data to be useful?") is not answered. For reference, uncoded BPSK at 10⁻⁵ needs about 9.6 dB, so the toy link closes with margin even after a 3 dB polarisation loss; that sentence belongs in the study.
* "467 kB raw" is airtime × bit rate; it omits framing overhead and does not say so in the result table.
* Ignoring Earth rotation changes the ideal contact time by up to about 7 % (ground speed 0.47 km/s against a ground-track speed of 6.99 km/s); it is fine to ignore, but the magnitude should be stated.

**Resolved, 17 October 2026:** Study 001 now derives the required E_b/N₀ for ideal BPSK at a stated bit-error rate, reports the link margin at every elevation mask, applies an explicit framing-efficiency factor to the raw byte count, states the Earth-rotation magnitude, and is labelled as part of the Link (communications) workstream on the research page. Four tests were added for the new quantities.

### 4.7 "54 published model tests" is a vanity metric

Test count is advertised on the front page as a credibility signal. Roughly a third of the 54 tests check input validation (rejecting negative counts, non-boolean flags, unknown labels) or assert that a string contains the word "SYNTHETIC". They establish that the code does what the code does; they are not evidence about anything in the world. Keep the tests, drop the number from the hero section.

### 4.8 Provenance and presentation

* All four studies were written and published on 16 October 2026, all four within two hours (commits at 11:19, 12:27 and 12:55 local time), with LLM assistance. A site whose principle is "every claim should include its evidence, source, and limitations" should say that on the research page.
* The footer and FAQ state that SpaceЖ is "initiated by Varta Industries, a division of Tryzantha LLC". No public record of either name was found. The sibling package in the Varta repository brands the same work "Volya research". The maintainer should confirm which entity is real and use one name everywhere; a reviewer from a named Ukrainian institution will check. **Resolved, 17 October 2026:** the initiating entity is Parallax Web Services, Inc., now stated on every page.
* The public git history and repository description still carry the site's parody-era content. Anyone invited to review will read it. **Maintainer's decision, 17 October 2026:** it stays.
* Study 002's source [6] is listed but never cited; Study 004's ISO citation supplies nothing used in the study.

## 5. Recommendations, in order

1. Derive or label the 60-second threshold (4.1). Until then, change the front page from "NOT DEMONSTRATED" to "requirement under definition".
2. Replace the programme register with a modality register (4.3), and add the radar-horizon computation as the first quantitative study that actually bears on the question.
3. Source the thresholds in 004 or present 368 / 110.67 as worked examples rather than requirements (4.4); reconcile the interval conventions (4.5).
4. Either connect 001 to the thesis and finish it (required E_b/N₀, overhead, margin) or move it out of the early-warning track (4.6).
5. Remove the test count from the hero; disclose authorship method and date on the research page; settle the initiating entity's name (4.7, 4.8).
6. Keep the integrity check, and add a link checker for external citations; two of eighteen had rotted or were mislabelled on day one.
