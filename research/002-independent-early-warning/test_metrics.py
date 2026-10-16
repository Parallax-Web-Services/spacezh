"""Test synthetic-only statistical accounting for SpaceЖ Research 002."""
import math
import unittest
from dataclasses import replace
from metrics import KnownLaunch, alert_precision, evaluate, wilson_interval


class AuditMetricTests(unittest.TestCase):
    def test_detection_clock_starts_at_launch_not_sensor_report(self):
        sample = [KnownLaunch(True, 61, 63), KnownLaunch(True, 59, 65)]
        r = evaluate(sample, [False])
        self.assertEqual(r["verified_by_60_seconds"], 1)
        self.assertEqual(r["official_notices_by_60_seconds"], 0)

    def test_missing_observation_is_counted_as_failure(self):
        r = evaluate([KnownLaunch(False, None, None), KnownLaunch(True, 1, 2)], [])
        self.assertEqual(r["known_launches"], 2)
        self.assertEqual(r["observable_launches"], 1)
        self.assertEqual(r["correct_detection_by_60_fraction"], 0.5)
        self.assertIsNone(r["false_public_alert_rate_per_control_window"])

    def test_impossibility_bound(self):
        sample = [KnownLaunch(True, 20, 35), KnownLaunch(False, None, None),
                  KnownLaunch(True, 75, 85)]
        r = evaluate(sample, [False, True, False])
        self.assertLessEqual(r["correct_detection_by_60_fraction"], r["observation_coverage_fraction"])
        self.assertEqual(r["false_public_alerts"], 1)

    def test_wilson_no_observed_failure_still_below_one(self):
        lo, hi = wilson_interval(100, 100)
        self.assertAlmostEqual(lo, 0.9630065, places=5)
        self.assertEqual(hi, 1)

    def test_wilson_edge_cases(self):
        self.assertEqual(wilson_interval(0, 1)[0], 0)
        self.assertEqual(wilson_interval(1, 1)[1], 1)
        with self.assertRaises(ValueError):
            wilson_interval(1, 0)
        with self.assertRaises(ValueError):
            wilson_interval(3, 2)

    def test_rare_event_precision_base_rate(self):
        expected = (0.99 * 0.0001) / (0.99*0.0001 + 0.001*0.9999)
        self.assertAlmostEqual(alert_precision(.99,.001,.0001),expected)
        self.assertLess(alert_precision(.99,.001,.0001),.10)

    def test_reject_invalid_timeline(self):
        cases = [KnownLaunch(False, 20, None),KnownLaunch(True, 20, 15),
                 KnownLaunch(True,None,25),KnownLaunch(True,-1,None),
                 KnownLaunch(True,float("nan"),None)]
        for item in cases:
            with self.subTest(case=item),self.assertRaises(ValueError):
                evaluate([item],[])

    def test_reject_nonboolean_quiet_control(self):
        with self.assertRaises(ValueError):
            evaluate([KnownLaunch(True, 12, 20)], [0])

    def test_no_live_realtime_interface(self):
        r = evaluate([KnownLaunch(True, 1, 2)], [False])
        self.assertIn("SYNTHETIC", r["status"])


if __name__ == "__main__":
    unittest.main()
