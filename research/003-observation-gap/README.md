# SpaceЖ Research 003 — Independent observation and evidence limits

**16 October 2026 · Public feasibility research · No operational warning capability**

## Finding

**The public sources reviewed do not establish a current, non-U.S.-dependent capability to observe and correctly verify ballistic launches within 60 seconds for Ukraine.** That is an evidence-limited finding, not proof that no non-public capability exists. We cannot truthfully demonstrate the 60-second objective with a satellite catalog, general orbital tracking, a civilian warning-relay app, or software that reacts quickly to an existing third-party notice.

This study does not detect, identify, track, predict the impact of, or warn the public about missiles. It evaluates only abstract probabilities, timestamp uncertainty and the evidentiary limitations of published programmes. **Do not use any output to make a safety decision.**

## The public capability distinction

| Publicly documented category | What the evidence establishes | Does it establish launch verification within 60s? |
| --- | --- | --- |
| EU Space Surveillance and Tracking (EU SST) | Operational services for collision avoidance, fragmentation and re-entry of orbital objects | **No**; a different mission, no such service in its published portfolio |
| ODIN'S EYE II | European Defence Fund study and design work on space-based missile early warning | **No**; research/design classification is not a deployed sensor |
| French-German JEWEL | Programme to develop an independent European early-warning capability; initial space segment aimed at early 2030s | **No**; future capability, not documented as operational today |
| French 2026 military programming | Publicly planned precursor capability before 2030 and additional infrared space component before 2035 | **No**; budget/programme objectives are not proof of 2026 operation |
| EU GOVSATCOM | Initial secure governmental satellite communications in operation in 2026 | **No**; carrying data is not the same as independently sensing a launch |
| UK–Ukraine civil-space cooperation agreement | Framework for civil/commercial collaboration | **No**; a cooperation framework is not a warning sensor |

The machine-readable public references and maturity notes are in [`source_register.json`](source_register.json). Status is **as documented in sources reviewed on 16 October 2026**. Named programmes and organizations have not endorsed SpaceЖ.

## Hard result 1 — The dependence trap

Let \(A\) mean an independently usable timely observation exists from source A for a true event, and \(B\) the same for source B. The probability at least one is available is

\[
P(A\cup B)=P(A)+P(B)-P(A\cap B).
\]

If only the two marginal probabilities are known, without knowing common-mode failure or evidence overlap, the *sharp* Fréchet bounds are

\[
\boxed{\max(P(A),P(B))\le P(A\cup B)\le\min(1,P(A)+P(B)).}
\]

**Toy example (not sensor data):** for \(P(A)=P(B)=0.8\), two perfectly overlapping observations yield \(P(A\cup B)=0.80\), while unjustifiably assuming their independence yields \(0.96\). From the marginals alone, all we know is that the combined value lies **between 0.80 and 1.00**. Two subscriptions to the same upstream observation cannot count as two independent sensors.

The earlier result still holds:

\[
P(D_{60})=P(C)P(D_{60}\mid C)\le P(C),
\]

where \(C\) means *at least one authorized, independent, suitable observation* and \(D_{60}\) means correct verification by 60 seconds from the actual event. If the conditional verification figure were hypothetically 0.9, the example gives **0.72** with identical evidence and **0.864** with independent evidence. Neither number is a claim about any existing system.

## Hard result 2 — Timestamp uncertainty creates a third outcome

Let the event time be known only within \([t_{0,L},t_{0,U}]\), and completed verification only within \([t_{v,L},t_{v,U}]\). The actual interval between them is bounded by

\[
\Delta_{\min}=t_{v,L}-t_{0,U},\quad
\Delta_{\max}=t_{v,U}-t_{0,L}.
\]

A 60-second claim is **guaranteed within** only if \(\Delta_{\max}\le 60\); **guaranteed late** if \(\Delta_{\min}>60\); otherwise **unresolved**. An unresolved event must not silently be counted as a pass. Independent validation needs timestamp provenance, clock uncertainty, and an event-level complete denominator.

## Hard result 3 — Positive-only logs cannot establish sensitivity

If a system sees 100 events and correctly handles all 100, the observed-positive accuracy is 100%. But without an independently assembled count of **all events**, the population detection rate is unidentified. The same 100 positive records are consistent with 100 out of 100 events or 100 out of 1,000. This is selection bias, not a lack of confidence in an otherwise complete dataset. The correct answer is **unknown**, not “100%”.

False alarms require independently selected negative windows, and an agreed, non-manipulable observation definition. Such data have not been obtained by SpaceЖ.

## Hard result 4 — Independence is an entire chain

Review must establish the nationality, authority, legal ability to operate, and ultimate upstream origin of each **essential** component: observation; source provenance; permission to access/use data; processing/hosting; timing; communications; operational authority; and safe public release. A non-U.S. API that republishes indispensable U.S.-origin early-warning data fails the user's full-independence criterion. Likewise, a satellite communications network is not an observation capability.

We have **not** validated an independent, authorized sensor source, independent ground-truth event population, complete operational dependency chain, or lawful civilian alert interface. Thus the 60-second requirement remains **NOT DEMONSTRATED**.

## Reproduction

This standard-library Python evaluator uses exclusively *invented abstract probabilities and timestamp intervals*, not missile or satellite observations. It cannot consume telemetry, perform tracking, or issue alerts.

```sh
python3 research/003-observation-gap/bounds.py
python3 -m unittest discover -s research/003-observation-gap -p 'test_*.py' -v
```

The model was tested locally with **15 deterministic unit tests**. Passing tests establish only the implementation of the mathematics, **not** a real warning capability.

## Review / falsification requirements

1. An authoritative Ukrainian scientific/public-safety reviewer defines which *lawfully shareable, aggregate* evidence would be acceptable. No classified feed, coordinates, operational data, or sensitive station siting should be requested or published.
2. The asserted source must be shown to be genuine launch observation rather than inference from delayed reports or another party's alert.
3. Provenance must exclude U.S.-controlled **indispensable** sensing, military intelligence and operational dependencies; unresolved provenance is not independent.
4. Evaluate with externally established complete event counts, event-time uncertainty, verifiably separate positive/negative controls, correlated-outage analysis, false alarms, and proper uncertainty intervals.
5. Separate first sensing, completed verification, authorized civil warning, and arrival at the user's device. SpaceЖ issues **none** of these operational notices.
6. If evidence is missing, report **not demonstrated**. No fabricated point estimates, no safety-critical promises, and no autonomous alert distribution.

## Next scientific decision

The immediate deliverable is an **independently reviewed evidence register and validation protocol**, not a hardware purchase or unsupported 60-second claim. Only authorized Ukrainian institutions should assess whether a protected evaluation is appropriate. The public repository should receive approved methodology and aggregate conclusions, never protected operational records.

## Primary public sources

- [EU Agency for the Space Programme — EU SST services](https://www.euspa.europa.eu/eu-space-programme/ssa/eu-sst)
- [European Defence Fund — ODIN'S EYE II factsheet (study/design)](https://defence-industry-space.ec.europa.eu/system/files/2023-06/ODINS%27EYE%20II-Factsheet_EDF22.pdf)
- [French Ministry of Armed Forces — JEWEL, 24 October 2025](https://www.defense.gouv.fr/en/news/jewel-france-and-germany-lay-foundation-european-early-warning-capability)
- [Légifrance — Loi n° 2026-791 du 16 août 2026 (military programming update), annexed report approved by Article 1, section « Alerte avancée »](https://www.legifrance.gouv.fr/jorf/article_jo/JORFARTI000054694924) — accessible copy: [Assemblée nationale, texte adopté n° 325](https://www.assemblee-nationale.fr/dyn/opendata/PRJLANR5L17BTA0325.html). Article 57 of the law itself only ratifies earlier ordinances.
- [EUSPA — GOVSATCOM initial operations, March 2026](https://www.euspa.europa.eu/pressroom/press-releases/cyprus-completes-first-operational-use-eu-govsatcom-hub-services-marking)
- [UK Space Agency — UK–Ukraine civil-space agreement, March 2026](https://www.gov.uk/government/news/uk-space-agency-signs-landmark-agreement-with-ukraine-to-strengthen-civil-space-cooperation)
