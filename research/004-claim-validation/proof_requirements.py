"""SpaceЖ 004: confidence bounds for ABSTRACT, synthetic evaluation outcomes.

No sensor integration, missile observations, trajectory calculation, or live alerts.
The model checks what finite statistical evidence could justify *a claim*
under explicitly hypothetical iid-binomial / stationary-Poisson assumptions.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Iterable

VALID_OUTCOMES = frozenset({"on_time", "late", "missed", "unresolved"})


def _probability(value: float, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a number between zero and one (exclusive)")
    value = float(value)
    if not (math.isfinite(value) and 0.0 < value < 1.0):
        raise ValueError(f"{name} must be a finite number between zero and one (exclusive)")
    return value


def _count(value: int, name: str, *, allow_zero: bool = True) -> int:
    if type(value) is not int or value < (0 if allow_zero else 1):
        raise ValueError(f"{name} must be an integer >= {0 if allow_zero else 1}")
    return value


def _positive(value: float, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a positive finite number")
    value = float(value)
    if not math.isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be a positive finite number")
    return value


def _logsumexp(log_terms: Iterable[float]) -> float:
    terms = list(log_terms)
    maximum = max(terms)
    return maximum + math.log(sum(math.exp(x - maximum) for x in terms))


def binomial_tail_at_least(k: int, n: int, p: float) -> float:
    """P(X >= k) for X ~ Binomial(n,p); use the shorter tail for stability.

    Intended for methodological / modest-sized inputs, not massive data analysis.
    """
    _count(n, "n")
    _count(k, "k")
    if k > n:
        raise ValueError("k cannot exceed n")
    if isinstance(p, bool) or not isinstance(p, (int, float)) or not math.isfinite(p) or not 0 <= p <= 1:
        raise ValueError("p must be in [0,1]")
    if k == 0:
        return 1.0
    if p == 0:
        return 0.0
    if p == 1:
        return 1.0
    if k == n:
        return math.exp(n * math.log(p))

    def logpmf(x: int) -> float:
        return (math.lgamma(n + 1) - math.lgamma(x + 1) - math.lgamma(n - x + 1)
                + x * math.log(p) + (n - x) * math.log1p(-p))

    if n - k + 1 <= k:
        return min(1.0, math.exp(_logsumexp(logpmf(j) for j in range(k, n + 1))))
    log_cdf = _logsumexp(logpmf(j) for j in range(0, k))
    # Stable evaluation of 1-exp(log_cdf), where log_cdf is near zero.
    return min(1.0, max(0.0, -math.expm1(min(0.0, log_cdf))))


def exact_one_sided_sensitivity_lower(successes: int, trials: int, *, alpha: float = 0.05) -> float:
    """Clopper-Pearson one-sided lower confidence limit for binomial success p.

    Requires an externally complete, representative trial census and iid trials.
    Otherwise it is NOT a valid operational sensitivity estimate.
    """
    _count(trials, "trials", allow_zero=False)
    _count(successes, "successes")
    if successes > trials:
        raise ValueError("successes cannot exceed trials")
    alpha = _probability(alpha, "alpha")
    if successes == 0:
        return 0.0
    if successes == trials:
        return math.exp(math.log(alpha) / trials)
    lo, hi = 0.0, 1.0
    for _ in range(65):
        mid = (lo + hi) / 2.0
        if binomial_tail_at_least(successes, trials, mid) >= alpha:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2.0


def zero_miss_sample_size(target_sensitivity: float, *, alpha: float = 0.05) -> int:
    """Smallest iid sample with 0 misses and CP lower bound >= target."""
    target = _probability(target_sensitivity, "target_sensitivity")
    alpha = _probability(alpha, "alpha")
    n = max(1, math.ceil(math.log(alpha) / math.log(target)))
    # Correct floating-point edge cases so *minimal* size is guaranteed.
    while math.exp(math.log(alpha) / n) < target:
        n += 1
    while n > 1 and math.exp(math.log(alpha) / (n - 1)) >= target:
        n -= 1
    return n


def zero_false_alarm_rate_upper(exposure_days: float, *, alpha: float = 0.05) -> float:
    """One-sided upper Poisson rate in alarms/day after 0 observed alarms.

    Only interpretable with continuous observation and a stationary Poisson process.
    """
    exposure = _positive(exposure_days, "exposure_days")
    alpha = _probability(alpha, "alpha")
    return -math.log(alpha) / exposure


def zero_alarm_days_required(max_mean_alarms_per_30_days: float, *, alpha: float = 0.05) -> float:
    """Continuous exposure days for the upper bound on mean 30-day count."""
    maximum = _positive(max_mean_alarms_per_30_days, "max_mean_alarms_per_30_days")
    alpha = _probability(alpha, "alpha")
    return -30.0 * math.log(alpha) / maximum


def simultaneous_no_failure_requirements(
    target_sensitivity: float = 0.99,
    max_mean_alarms_per_30_days: float = 1.0,
    *,
    joint_confidence: float = 0.95,
) -> dict:
    """Two one-sided bounds with Bonferroni joint confidence >= 1-alpha.

    Bonferroni does not assume the two estimates independent, but the
    *individual* iid binomial and stationary Poisson assumptions still apply.
    """
    confidence = _probability(joint_confidence, "joint_confidence")
    alpha_each = (1.0 - confidence) / 2.0
    target = _probability(target_sensitivity, "target_sensitivity")
    maximum = _positive(max_mean_alarms_per_30_days, "max_mean_alarms_per_30_days")
    n = zero_miss_sample_size(target, alpha=alpha_each)
    exposure = zero_alarm_days_required(maximum, alpha=alpha_each)
    return {
        "joint_confidence_lower_bound": confidence,
        "one_sided_alpha_each": alpha_each,
        "target_sensitivity": target,
        "zero_miss_independent_trials_required": n,
        "max_expected_false_alarms_per_30_days": maximum,
        "zero_alarm_continuous_exposure_days_required": round(exposure, 6),
        "stationarity_and_iid_assumed": True,
        "real_world_detection_validated": False,
    }


def conservative_event_tally(outcomes: Iterable[str]) -> dict:
    """Treat uncertain/late/missing events as NONsuccess for evidence claims."""
    counts = {x: 0 for x in ("on_time", "late", "missed", "unresolved")}
    for outcome in outcomes:
        if outcome not in VALID_OUTCOMES:
            raise ValueError(f"Unknown abstract outcome: {outcome!r}")
        counts[outcome] += 1
    if not sum(counts.values()):
        raise ValueError("Event census cannot be empty")
    counts["known_events"] = sum(counts.values())
    counts["guaranteed_on_time"] = counts["on_time"]
    counts["conservative_non_success"] = counts["known_events"] - counts["on_time"]
    return counts


def assess_synthetic_scenario(scenario: dict) -> dict:
    """Demonstrate WHY a toy data set cannot establish launch detection.

    A `synthetic` trial source is permanently ineligible for operational claims.
    No live inputs are supported and no alerts are emitted.
    """
    if scenario.get("data_kind") != "synthetic":
        raise ValueError("Only synthetic demonstration data are accepted by this example")
    tally = conservative_event_tally(scenario["abstract_outcomes"])
    days = _positive(scenario["non_event_exposure_days"], "non_event_exposure_days")
    false_alarms = _count(scenario["false_alarms"], "false_alarms")
    if false_alarms != 0:
        return {
            "tally": tally,
            "false_alarms": false_alarms,
            "zero_alarm_formula_applicable": False,
            "operational_qualification": "NOT ELIGIBLE — SYNTHETIC DATA",
        }
    return {
        "tally": tally,
        "95pct_one_sided_lower_sensitivity_if_iid_and_complete": round(
            exact_one_sided_sensitivity_lower(tally["on_time"], tally["known_events"]), 8),
        "95pct_one_sided_upper_expected_false_alarms_per_30d_if_poisson": round(
            30 * zero_false_alarm_rate_upper(days), 8),
        "source_independence_proved": False,
        "population_census_validated": False,
        "operational_qualification": "NOT ELIGIBLE — SYNTHETIC DATA",
    }


def demonstration() -> dict:
    example = json.loads(Path(__file__).with_name("synthetic_example.json").read_text(encoding="utf-8"))
    return {
        "study": "SpaceZh Research 004 — Requirements for a 60-second evidence claim",
        "methodological_not_operational": True,
        "required_zero_miss_trials_95pct_one_sided": {
            f"{100*q:.1f}%": zero_miss_sample_size(q) for q in (0.95, 0.99, 0.999)
        },
        "joint_95pct_example_requirements": simultaneous_no_failure_requirements(),
        "illustrative_scenario": assess_synthetic_scenario(example),
    }


if __name__ == "__main__":
    print(json.dumps(demonstration(), indent=2, ensure_ascii=False, sort_keys=True))
