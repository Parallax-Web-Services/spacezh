"""SpaceЖ Research 003: abstract evidence bounds, NOT a launch detector.

This standard-library-only module has no sensors, interfaces, clocks, networking,
tracking, location, missile parameters, or alert functions. Input probabilities
and times are hypothetical or externally aggregated research measurements.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Literal
import json


def _probability(value: float, name: str) -> float:
    if not isinstance(value, (float, int)) or isinstance(value, bool):
        raise TypeError(f"{name} must be a number")
    if not isfinite(value) or not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be finite and between 0 and 1")
    return float(value)


def coverage_union_bounds(p_a: float, p_b: float) -> tuple[float, float]:
    """Sharp bounds for P(A union B) knowing only the marginal probabilities.

    Frechet bounds: max(p_a,p_b) <= P(A U B) <= min(1,p_a+p_b).
    No independence between the sources is presumed.
    """
    a = _probability(p_a, "p_a")
    b = _probability(p_b, "p_b")
    return max(a, b), min(1.0, a + b)


def coverage_union_with_overlap(p_a: float, p_b: float, p_both: float) -> float:
    """Exact probability of at least one observation given measured P(A and B)."""
    a = _probability(p_a, "p_a")
    b = _probability(p_b, "p_b")
    both = _probability(p_both, "p_both")
    low_intersection = max(0.0, a + b - 1.0)
    high_intersection = min(a, b)
    if not low_intersection - 1e-12 <= both <= high_intersection + 1e-12:
        raise ValueError("p_both is incompatible with the two marginal probabilities")
    return min(1.0, max(0.0, a + b - both))


def timely_success_probability(p_observed: float, p_timely_given_observed: float) -> float:
    """Identity P(timely correct verification)=P(observed)*P(timely|observed).

    This identity presumes a correctly verified report requires observation;
    neither input is measured by this code.
    """
    return _probability(p_observed, "p_observed") * _probability(
        p_timely_given_observed, "p_timely_given_observed"
    )


@dataclass(frozen=True)
class TimeInterval:
    """Uncertainty interval for a timestamp, in seconds on a common reference clock."""
    earliest: float
    latest: float

    def __post_init__(self) -> None:
        if not all(isinstance(x, (int, float)) and not isinstance(x, bool) and isfinite(x)
                   for x in (self.earliest, self.latest)):
            raise ValueError("Timestamp endpoints must be finite numbers")
        if self.earliest > self.latest:
            raise ValueError("Timestamp earliest cannot exceed latest")


def deadline_status(
    event_time: TimeInterval,
    verification_time: TimeInterval,
    threshold_s: float = 60.0,
) -> Literal["guaranteed_within", "guaranteed_late", "unresolved"]:
    """Safely classifies an aggregate timing claim using uncertainty intervals.

    If even the maximum possible elapsed time is <= threshold: guaranteed within.
    If the minimum possible elapsed time > threshold: guaranteed late.
    Otherwise the evidence is insufficient to classify. No timing measurements
    are captured or generated here.
    """
    if not isinstance(threshold_s, (int, float)) or not isfinite(threshold_s) or threshold_s < 0:
        raise ValueError("threshold_s must be nonnegative and finite")
    earliest_elapsed = verification_time.earliest - event_time.latest
    latest_elapsed = verification_time.latest - event_time.earliest
    if latest_elapsed <= threshold_s:
        return "guaranteed_within"
    if earliest_elapsed > threshold_s:
        return "guaranteed_late"
    return "unresolved"


def selection_bias_range(observed_correct: int, total_known_events: int) -> tuple[float, float]:
    """Coverage bounds for a given complete, independently known denominator.

    Correct observations could still be late; thus the upper bound is NOT an
    estimate of timely detection. With NO independent total, no non-trivial
    population sensitivity bound follows from the observed positive cases.
    """
    if (not isinstance(observed_correct, int) or isinstance(observed_correct, bool)
            or not isinstance(total_known_events, int) or isinstance(total_known_events, bool)):
        raise TypeError("Counts must be integers")
    if observed_correct < 0 or total_known_events <= 0 or observed_correct > total_known_events:
        raise ValueError("Counts must satisfy 0 <= observed_correct <= total_known_events")
    r = observed_correct / total_known_events
    return 0.0, r


def synthetic_reference() -> dict:
    """Two illustrative worlds with the SAME marginal source probabilities.

    The numbers are invented teaching assumptions, not evidence of any real
    nation's sensor coverage or ballistic-warning performance.
    """
    a = b = 0.8
    conditional_timely = 0.9
    independent_overlap = a * b
    shared_overlap = a
    shared = coverage_union_with_overlap(a, b, shared_overlap)
    independent = coverage_union_with_overlap(a, b, independent_overlap)
    return {
        "purpose": "synthetic_math_only",
        "marginal_observation_probability_a": a,
        "marginal_observation_probability_b": b,
        "unknown_dependence_union_interval": coverage_union_bounds(a, b),
        "identical_evidence_union": shared,
        "independent_evidence_union": independent,
        "assumed_timely_conditional": conditional_timely,
        "identical_evidence_timely_probability": timely_success_probability(shared, conditional_timely),
        "independent_evidence_timely_probability": timely_success_probability(independent, conditional_timely),
        "time_case_within": deadline_status(TimeInterval(0, 2), TimeInterval(56, 59)),
        "time_case_uncertain": deadline_status(TimeInterval(0, 3), TimeInterval(59, 63)),
        "time_case_late": deadline_status(TimeInterval(0, 1), TimeInterval(64, 70)),
        "real_sensor_performance": None,
    }


if __name__ == "__main__":
    print(json.dumps(synthetic_reference(), indent=2, ensure_ascii=False))
