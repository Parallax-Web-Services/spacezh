"""SpaceЖ Research 002: non-operational, synthetic early-warning metric audit.

This program does not detect, track or classify missiles. It reads a
pre-labeled, synthetic sample of known events and quiet control windows to
check how detection and alert latencies would be scored. No sensor interfaces,
network listeners, geography, or real-time alert outputs are provided.
"""
from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Optional

# Approximate two-sided 95% normal quantile used for Wilson intervals.
Z95 = 1.959963984540054


def wilson_interval(k: int, n: int, z: float = Z95) -> tuple[float, float]:
    """Wilson binomial proportion interval; not a substitute for unbiased trials."""
    if n <= 0 or not (0 <= k <= n) or z <= 0:
        raise ValueError("Expected n>0, 0<=k<=n and z>0")
    p = k / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1-p) / n + z*z / (4*n*n)) / denom
    return max(0.0, center-half), min(1.0, center+half)


def alert_precision(sensitivity: float, false_alert_rate: float, event_prevalence: float) -> float:
    """Toy Bayes calculation: probability event was real, given an alert.

    All three inputs refer to the *same unit* of observation. They must not be
    inferred from an ad hoc list of selected observations.
    """
    for x in (sensitivity, false_alert_rate, event_prevalence):
        if not 0 <= x <= 1:
            raise ValueError("Probabilities must be in [0, 1]")
    a = sensitivity * event_prevalence
    b = false_alert_rate * (1 - event_prevalence)
    if a + b == 0:
        raise ValueError("No alerts in this hypothetical configuration")
    return a / (a + b)


@dataclass(frozen=True)
class KnownLaunch:
    """A synthetic event with independently supplied launch ground truth.

    verified_detection_s is launch-to-verified-detection latency, not latency
    measured from first report. None means no verified detection exists.
    official_notice_s is total launch-to-official-notice latency, if any.
    """
    observed: bool
    verified_detection_s: Optional[float]
    official_notice_s: Optional[float]

    def validate(self) -> None:
        for value in (self.verified_detection_s, self.official_notice_s):
            if value is not None and (not math.isfinite(value) or value < 0):
                raise ValueError("Latencies must be finite and nonnegative")
        if not self.observed and self.verified_detection_s is not None:
            raise ValueError("Verified detection requires an actual observation")
        if self.official_notice_s is not None and self.verified_detection_s is None:
            raise ValueError("An official notice cannot be scored without verification")
        if self.official_notice_s is not None and self.official_notice_s < self.verified_detection_s:
            raise ValueError("Official notice cannot precede verified detection")


def evaluate(launches: list[KnownLaunch], quiet_windows: list[bool],
             threshold_s: float = 60.0) -> dict[str, Any]:
    """Score truth-labeled synthetic inputs; does not perform detection.

    Quiet windows are equal length by the caller's definition. Those labeled
    True contained a *false publicly issued alert*. Never compare windows of
    different durations as though they had a common false-alert rate.
    """
    if not launches or not math.isfinite(threshold_s) or threshold_s <= 0:
        raise ValueError("At least one known launch and a positive threshold required")
    for item in launches:
        item.validate()
    n = len(launches)
    seen = sum(item.observed for item in launches)
    verified = sum(item.verified_detection_s is not None for item in launches)
    within = sum(item.verified_detection_s is not None
                 and item.verified_detection_s <= threshold_s for item in launches)
    noticed = sum(item.official_notice_s is not None
                  and item.official_notice_s <= threshold_s for item in launches)
    if noticed > within or within > verified or verified > seen:
        raise AssertionError("Invalid event accounting")
    if any(type(x) is not bool for x in quiet_windows):
        raise ValueError("Quiet controls must be booleans")
    negatives = len(quiet_windows)
    false_alarms = sum(quiet_windows)
    return {
        "known_launches": n,
        "observable_launches": seen,
        "verified_detections": verified,
        "verified_by_60_seconds": within,
        "official_notices_by_60_seconds": noticed,
        "observation_coverage_fraction": seen / n,
        "correct_detection_by_60_fraction": within / n,
        "correct_detection_by_60_95pct_wilson": list(wilson_interval(within, n)),
        "notices_by_60_fraction": noticed / n,
        "quiet_control_windows": negatives,
        "false_public_alerts": false_alarms,
        "false_public_alert_rate_per_control_window": false_alarms / negatives if negatives else None,
        "false_public_alert_rate_95pct_wilson": list(wilson_interval(false_alarms, negatives)) if negatives else None,
        "sensor_cannot_be_fixed_by_software": "P(detection<=60s) <= P(launch observable)",
        "status": "SYNTHETIC ILLUSTRATION; NOT A REAL MISSILE-WARNING PERFORMANCE ESTIMATE",
    }


def read_example(path: Path) -> tuple[list[KnownLaunch], list[bool]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if raw.get("classification") != "SYNTHETIC_ONLY":
        raise ValueError("Only explicitly synthetic examples are accepted by this tool")
    items = [KnownLaunch(**item) for item in raw["known_launches"]]
    quiet = raw.get("quiet_control_windows", [])
    return items, quiet


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--example", type=Path, default=Path(__file__).with_name("synthetic_example.json"))
    args = parser.parse_args()
    launches, quiet = read_example(args.example)
    print(json.dumps({"research_id": "SpaceZh-002", "test_input": args.example.name,
                      "evaluation": evaluate(launches, quiet)}, indent=2))


if __name__ == "__main__":
    main()
