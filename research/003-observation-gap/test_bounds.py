"""Unit tests for abstract Research 003 bookkeeping, not a detection system."""
import unittest
from bounds import (
    TimeInterval,
    coverage_union_bounds,
    coverage_union_with_overlap,
    timely_success_probability,
    deadline_status,
    selection_bias_range,
    synthetic_reference,
)


class BoundsTests(unittest.TestCase):
    def test_union_lower_upper_sharp(self):
        self.assertEqual(coverage_union_bounds(0.8, 0.8), (0.8, 1.0))

    def test_identical_sources_add_nothing(self):
        self.assertAlmostEqual(coverage_union_with_overlap(.8, .8, .8), .8)

    def test_independent_assumption_alters_union(self):
        self.assertAlmostEqual(coverage_union_with_overlap(.8, .8, .64), .96)

    def test_no_overlap_possible_if_marginals_fit(self):
        self.assertAlmostEqual(coverage_union_with_overlap(.3, .4, 0), .7)

    def test_impossible_overlap_rejected(self):
        with self.assertRaises(ValueError):
            coverage_union_with_overlap(.8, .8, .5)

    def test_probability_range_rejected(self):
        with self.assertRaises(ValueError):
            coverage_union_bounds(1.1, .4)
        with self.assertRaises(ValueError):
            timely_success_probability(.8, float("nan"))

    def test_timely_never_exceeds_observation(self):
        self.assertAlmostEqual(timely_success_probability(.8, .9), .72)
        self.assertLessEqual(timely_success_probability(.8, .9), .8)

    def test_interval_guaranteed_within(self):
        self.assertEqual(deadline_status(TimeInterval(0, 2), TimeInterval(56, 59)), "guaranteed_within")

    def test_interval_guaranteed_late(self):
        self.assertEqual(deadline_status(TimeInterval(0, 1), TimeInterval(64, 70)), "guaranteed_late")

    def test_interval_ambiguous(self):
        self.assertEqual(deadline_status(TimeInterval(0, 3), TimeInterval(59, 63)), "unresolved")

    def test_interval_boundaries_inclusive(self):
        self.assertEqual(deadline_status(TimeInterval(0, 0), TimeInterval(60, 60)), "guaranteed_within")

    def test_bad_interval_rejected(self):
        with self.assertRaises(ValueError):
            TimeInterval(5, 4)

    def test_selection_denominator_necessary(self):
        self.assertEqual(selection_bias_range(100, 100), (0, 1.0))
        self.assertEqual(selection_bias_range(100, 1000), (0, .1))

    def test_invalid_counts(self):
        with self.assertRaises(ValueError):
            selection_bias_range(101, 100)

    def test_reference_synthetic_only(self):
        d = synthetic_reference()
        self.assertIsNone(d["real_sensor_performance"])
        self.assertEqual(d["time_case_uncertain"], "unresolved")
        self.assertAlmostEqual(d["independent_evidence_timely_probability"], .864)


if __name__ == "__main__":
    unittest.main()
