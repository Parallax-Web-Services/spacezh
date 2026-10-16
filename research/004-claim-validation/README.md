# SpaceЖ Research 004 — What would justify a 60-second detection claim?

**16 October 2026 | Independent statistical validation of proposed performance claims | NOT an operational system**

## The engineering decision

We want to support Ukraine's defense and civilian resilience without relying on indispensable U.S. military sensing, U.S.-origin intelligence feeds or U.S.-controlled operational services. The research requirement remains **correct, independently sourced launch verification within 60 seconds of actual launch**. We have **not** demonstrated that capability, found an authorized independent sensor that meets it, or obtained a real event census.

**This study asks:** If a future, separately authorized team presented performance results, how much evidence would be required to *support* its claims? What would force us to reject an impressive but unreliable benchmark?

The model handles only **abstract pre-labeled fictional outcomes and mathematical summaries**. It never receives launch imagery or telemetry, estimates missile trajectories, selects sensor locations, provides detection logic, or issues alerts. **It cannot be used for civilian safety decisions or operational claims.**

## Finding 1 — A perfect trial record is not proof of perfect reliability

If a truly complete, representative set of \(n\) **independent** real-world event trials is correctly classified within the 60-second threshold with **zero failures**, the exact one-sided \((1-\alpha)\) Clopper–Pearson lower confidence bound on success probability \(s\) is

\[
\boxed{s_L = \alpha^{1/n}}.
\]

This follows by inverting the binomial probability \(P(n\;\mathrm{successes}\mid s)=s^n\). To achieve \(s_L\ge s_0\):

\[
\boxed{n_{\min}=\left\lceil \frac{\ln\alpha}{\ln s_0}\right\rceil}. 
\]

With one-sided 95% confidence (\(\alpha=0.05\)), the *minimum* independent, completely enumerated, **real** zero-miss trials are:

| Desired lower bound on sensitivity | Required zero-miss independent trials |
|---|---:|
| 95% | 59 |
| 99% | **299** |
| 99.9% | **2,995** |

After 100/100 apparent successes, the exact lower confidence bound is only **97.05%**, not 99%. One failure or one uncertain case changes the calculation. The code also implements the exact binomial lower limit for arbitrary counts by inverting \(P(X\ge k\mid p)\), rather than treating an incomplete set of positive detections as the whole population.

**The important qualifier:** these formulas only infer a population success probability under an appropriate sampling model. Real launches may be rare, clustered, non-exchangeable, and unobservable to the evaluator. A thousand simulations or a log containing only successfully spotted events **cannot** establish sensitivity to actual launches. Effective sample size may be drastically lower than raw event count under correlated trials. Do not substitute a naive statistical effective-sample-size guess for an independently valid test design.

## Finding 2 — Zero observed false alerts does not mean zero false-alert risk

Under an **assumed stationary Poisson model** for falsely issued independent notifications, if \(N=0\) false alarms are observed over complete continuous monitoring exposure \(D\) days, the exact one-sided upper bound on rate \(\lambda\) (false alarms/day) is

\[
\boxed{\lambda_U=\frac{-\ln\alpha}{D}}.
\]

To bound the **mean number** of false alarms in a 30-day interval by at most \(m\), with no observed false alarms:

\[
\boxed{D\ge \frac{-30\ln\alpha}{m}}.
\]

At one-sided 95% confidence and \(m=1\) expected false alarm per 30 days, even zero alarms would require **89.87 consecutive, fully observed days** of relevant exposure. This is a bound on the Poisson *mean*, not a guarantee that a future calendar month cannot contain two or more false alarms. Gaps, changing alert thresholds, correlated spurious signals, maintenance, seasonality, and changes to the operating environment invalidate an uncritical Poisson interpretation.

False alarms must be assessed over the *entire non-event exposure*, not only brief windows selected around known incidents or after a system has already issued an alert. An evaluation that only counts correct alerts can hide a high false-alert burden.

## Finding 3 — Two credibility claims consume a joint confidence budget

Suppose a future study requires BOTH:

- Correct launch verification by 60 seconds with population sensitivity \(s\ge 0.99\), and
- An expected false-alert rate no greater than **one per 30 days**.

To bound **both jointly at at least 95% confidence**, allocate a one-sided error budget of 2.5% to each. By the union bound (Bonferroni), the chance either statistical statement misses its nominal coverage is at most \(0.025+0.025=0.05\). This step does **not** require the two confidence events to be independent, but each individual sampling model **must** be valid.

Under the extremely favorable scenario of zero misses and zero false alarms:

| Hypothetical evidence criterion | One-sided 95% *separate* | Joint 95% with split alpha |
|---|---:|---:|
| Independent, complete event trials for ≥99% sensitivity | 299 | **368** |
| Continuous monitoring days to bound mean false alarms ≤1/30 days | 89.87 | **110.67** |

This is **a mathematical minimum under idealized assumptions**, not an achievable-test schedule or proposed number of real launches. Fewer false alerts or missed observations do not excuse missing source independence, unbiased event sampling, timing certainty or Ukrainian authorization.

## Finding 4 — Unresolved timestamps are not silent successes

A verified event may have uncertain time bounds. Research 003 classifies events as *guaranteed within 60 s*, *definitely late*, or *unresolved*. For a conservative published performance claim in Research 004:

- **on_time:** only an independently verified, guaranteed ≤60s completion counts as success;
- **late, missed, unresolved:** count as non-success when computing conservative evidence bounds;
- **event census unknown:** no population sensitivity claim is permitted;
- **source independence unknown:** no claim that the system meets the non-U.S. requirement;
- **synthetic data only:** cannot validate operational detection, regardless of the numeric result.

Treating unresolved cases as non-success lowers a statistical bound conservatively; it is **not** a factual conclusion that those events were late. The file `synthetic_example.json` contains fictional outcomes, not actual Ukrainian or missile data.

## Results of the deliberately inadequate synthetic example

The sample contains eight `on_time`, one `late`, one `unresolved` fictional trial; seven fictional days of no false alarms. Even **if** it were a valid iid/Poisson sample (it is not):

- 8/10 has a one-sided 95% exact lower sensitivity limit of about **49.31%**.
- Zero false alarms over seven days allows a one-sided 95% upper bound of about **12.84 expected false alarms per 30 days**.
- The evaluator explicitly returns **`NOT ELIGIBLE — SYNTHETIC DATA`**.

The sample deliberately demonstrates why a visually encouraging mini-demo is an unacceptable basis for announcing civilian protection capability.

## Reproducibility

No third-party packages. Python 3.9+.

```bash
python3 research/004-claim-validation/proof_requirements.py
python3 -m unittest discover -s research/004-claim-validation -p 'test_*.py' -v
```

**24 deterministic tests passed locally at publication.** They cover exact tail inversion, boundary cases, sample-size minimality, joint confidence allocation, Poisson exposure, unresolved-case handling, and rejection of nonsynthetic data in the demo. Tests validate the *math and implementation*, not the existence or reliability of launch sensors.

`synthetic_reference.json` records the model's fictional baseline; it is not evidence of field performance.

## An independently reviewable acceptance gate

| Evidence required | Status | Why it matters |
|---|---|---|
| Independent, authorized source genuinely observing launches | **Not demonstrated** | No algorithm can certify events never observed |
| Verifiable absence of indispensable U.S.-origin operational sensing/intelligence | **Not demonstrated** | A non-U.S. reseller may depend on U.S. sources |
| Complete ground-truth event census, including all misses and unknowns | **Not obtained** | Positive-only logs cannot measure sensitivity |
| Event-time and verification-time uncertainty bounds | **Not obtained** | A reported elapsed time may not certify ≤60s |
| Independently sampled continuous non-event exposure | **Not obtained** | False-alarm risk cannot be measured from detections alone |
| Correlation, drift, change-control and subgroup methodology | **Not approved** | iid/Poisson confidence may fail under clustering |
| Ukrainian expert/appropriate public-safety authorization | **Not obtained** | Any live safety-related evaluation needs authorized oversight |

**Current result: NOT DEMONSTRATED.** Do not publish an implied probability of actual detection or issue public alerts. This is a research protocol for independent critique, not a military sensor design.

## Consequential next step

Request a narrowly scoped review from qualified Ukrainian scientific/public-safety experts of the **minimum permissible evidence and statistical acceptance criteria**. The request should seek no protected sensor locations, classified event logs, actionable targeting information, or operational time/location patterns. Restricted details, if any, must remain under appropriate institutional control; public outputs should consist only of vetted methods and aggregate conclusions.

Until a real independent observation route is documented and vetted, further effort on visualizations or detector algorithms cannot close the actual gap. This is our stop/go finding, not a reason to inflate a project milestone.

## References

1. [NIST — Exact binomial confidence limits](https://itl.nist.gov/div898/software/dataplot/refman2/auxillar/exacbino.htm) — small-sample exact one-sided binomial uncertainty.
2. [Cochrane Handbook §16.9.4 — Confidence intervals when no events are observed](https://training-noproxy.cochrane.org/handbook/archive/v5.0.2/chapter_16/16_9_4_confidence_intervals_when_no_events_are_observed.htm) — zero-event rate upper limits and Poisson approximations.
3. [ISO 22322:2022 — Emergency management, guidelines for public warning](https://committee.iso.org/standard/84558.html) — context for responsible warning governance; this research is **not** a claim of compliance.
4. [SpaceЖ Research 003 — Independence, correlation and timestamp limitations](../003-observation-gap/README.md).

All statistics in this note are mathematical results under disclosed assumptions. No cited organization has reviewed or endorsed SpaceЖ.
