# SpaceЖ Research 002 — Independent ballistic early warning in 60 seconds

**Public feasibility research · 16 October 2026 · Research stage, not an operational detection or alert service**

## The problem

**Can Ukraine obtain independently verified evidence of a ballistic missile launch within 60 seconds of the actual launch, with no U.S. military sensing, intelligence, or required U.S.-controlled service?**

The 60-second stopwatch starts at **launch**, not when another provider submits a notification. A system that merely republishes an existing alert more quickly does not satisfy the requirement.

The mission is Ukrainian civilian protection and sovereign public-interest infrastructure. This research does **not** provide a ballistic detection algorithm, sensor placement, threat tracks, impact prediction, targeting, or live citizen-facing alerts. No capability is claimed before independent proof.

## Why it is a real capability gap

- On October 13, 2026, President Zelenskyy said Ukraine received no prior intelligence warnings from partners about ballistic missiles striking Kyiv. The U.S. stated that it continued sharing intelligence; the reason for the missing warnings was disputed or unresolved. [1]
- Reuters reported October 14 that Europe had no operational equivalent to the United States' space-based infrared early-warning capability. [2]
- France and Germany's JEWEL work aims for an initial European space-based early-warning capability in the **early 2030s**. The EU-funded ODIN'S EYE II programme was a design and simulation effort, not evidence that a complete launch-detection constellation is ready to deploy. [3][4]
- EU Space Surveillance and Tracking supports orbiting-space-object collision avoidance, reentry and fragmentation analyses. It is **not** a public instantaneous ballistic-launch detection service. [5]

## Define the measurement honestly

Let launch time be \(t_0\). The full launch-to-verification latency is

\[
T_{\rm detect}=T_{\rm observe}+T_{\rm ingest}+T_{\rm verify}.
\]

Here, \(T_{\rm observe}\) includes any delay before the **first usable independent sensor observation**. Missing observation is a detection failure, even if later software runs instantly.

If a verified detection could be passed to Ukrainian civilian warning authorities, a *separate* total time would be

\[
T_{\rm public}=T_{\rm detect}+T_{\rm authorize}+T_{\rm distribute}+T_{\rm device}.
\]

**Research target:** \(T_{\rm detect}\leq60\,\mathrm{s}\) for actual, independently verified launches, with meaningful reliability and false-alert bounds. An alert after the 60-second limit does not meet this requirement even if it was delivered quickly from the first notification.

The 60-second figure is SpaceЖ's own research target, set by the maintainer against ballistic flight times to Ukrainian cities of only a few minutes. It is not taken from a civil-protection standard or a published flight-time analysis; reviewers are invited to challenge it.

### First hard upper bound

Define \(C\) = “the launch is observable by at least one suitable, authorized, independent source” and \(D_{60}\) = “a launch was correctly verified by 60 seconds.”

Because \(D_{60}\subseteq C\),

\[
\boxed{P(D_{60})=P(C)P(D_{60}\mid C)\leq P(C).}
\]

If suitable observation coverage is absent, compute power, AI models, networking and dashboards **cannot create missing evidence**. Do not confuse orbit catalogs, earth-observation images or a public OSINT report with a capable launch sensor.

### The false-alarm base-rate trap

For sensitivity \(s\), false-positive rate \(f\), and true-event prevalence \(\pi\) over identical time windows:

\[
P(\text{real event}\mid\text{alert})=\frac{s\pi}{s\pi+f(1-\pi)}.
\]

**Illustration only:** \(s=0.99\), \(f=0.001\), \(\pi=0.0001\) gives only about 9% probability that a raised alert represents a genuine event. Those are **invented values**, not sensor measurements or Ukrainian attack frequencies. This illustrates why a high claimed detection rate alone is insufficient for civilian public safety.

### Unbiased sampling and confidence

Count **all known launches**, including events with no sensor observation, no verification and late verification. Do not compute accuracy only from events already spotted. Include independent non-event control windows of a defined common duration to measure false alarms. The simple Python harness includes Wilson 95% confidence intervals, whose assumptions must be reviewed for dependent events and non-random sampling.

Even if all 100 known synthetic events are detected, the 95% Wilson lower bound is about 96.3% — not 100%. A published probability cannot be stronger than its evidence base.

## Operational independence audit

The independent critical path would have to work without:

- Any indispensable U.S. satellite launch-detection feed or U.S. military intelligence, including repackaged data whose original sensor is U.S.-controlled.
- U.S. government sensor tasking, alert-routing approval, or restricted military API credentials.
- U.S.-controlled operational hosting, authorization, timing, or connectivity as a single point of failure.

A European distributor of U.S.-origin sensor information does **not** become independent merely by changing the endpoint. Research repositories being publicly mirrored on a U.S.-based host are not themselves operational dependencies, but supply-chain sovereignty and actual running infrastructure still need a separate audit. We assume **no partners or sensor access have been committed**. Work with consenting Ukrainian and non-U.S. scientific/public-safety partners only; do not approach U.S. defense-industry partners.

## What we can research publicly now

1. **Capability inventory:** distinguish genuine launch sensors from orbit catalogs, delayed OSINT, ordinary optical observations, and existing official air-raid alert systems; document sources, permissions, updates and independence.
2. **Coverage gap:** identify whether there is any independently documented and appropriately shareable evidence proving immediate observation. Without that, publish the gap instead of assuming coverage.
3. **Timestamp and reliability standards:** define ground-truth launch time, trusted clock/uncertainty, negative controls, completeness of known events, launch-to-detection vs launch-to-public-notice, and false-alarm accounting.
4. **Ukrainian civilian safety review:** evaluate only with authorized Ukrainian experts. Never spoof, override, or originate public air-raid warnings; do not request sensitive operational information.
5. **Scientific review:** publish methodology, limitations, negative findings and approved aggregate metrics. Do **not** publish real-time threat locations, operational sensor layouts, targeting data, sensitive station coordinates, or restricted feeds.

**No-go rule:** We must not claim a 60-second operational capability without lawful, independently validated sensing evidence and a statistically credible unbiased evaluation. Fast response to synthetic data is not launch detection.

## Reproducible evaluator

`metrics.py` evaluates only **synthetic pre-labeled input**. It does not accept an operational feed, sense a launch, or issue an alert. The synthetic dataset contains no actual Ukraine or missile data.

```sh
python3 research/002-independent-early-warning/metrics.py
python3 -m unittest discover -s research/002-independent-early-warning -p 'test_*.py' -v
```

Nine tests passed locally before publication. This validates only the bookkeeping and statistical helpers, not the sensing requirement.

## The decisive next questions

- What independent, lawful, suitably early **observation** source exists or can realistically be established without U.S. assistance?
- Can qualified Ukrainian experts define an authorized evidence/ground-truth validation without disclosing protected information?
- Could any feasible independent observation coverage ever satisfy the 60-second requirement for the full stated threat set?
- What missed-warning and false-alarm risks will civilian protection authorities consider acceptable?
- Which operational facts should stay confidential under appropriate Ukrainian review rather than be published on GitHub?

If these cannot be answered, that is the finding—not a reason to produce an impressive simulation.

## Sources

1. [Associated Press — Kyiv missile-warning failure reported, 13 October 2026](https://apnews.com/article/russia-ukraine-war-zelenkyy-no-warning-missile-strike-10c54e55f31aded2db95242fdb4fd153)
2. [Reuters — Europe's limited options to replace U.S. missile-warning data, 14 October 2026](https://www.reuters.com/business/media-telecom/ukraine-struggles-with-starlink-us-satellite-data-europe-has-no-quick-fix-2026-10-14/)
3. [French Ministry of Armed Forces — JEWEL cooperation objective](https://www.defense.gouv.fr/en/news/jewel-france-and-germany-lay-foundation-european-early-warning-capability)
4. [European Defence Fund — ODIN'S EYE II factsheet](https://defence-industry-space.ec.europa.eu/system/files/2023-06/ODINS%27EYE%20II-Factsheet_EDF22.pdf)
5. [European Union — EU Space Surveillance and Tracking remit](https://eu-space.europa.eu/space-safety/space-situational-awareness-ssa/space-surveillance-and-tracking-sst)
6. [Lviv Regional State Administration — Ukrainian civilian Air Alert application](https://loda.gov.ua/en/services/text/18131)
