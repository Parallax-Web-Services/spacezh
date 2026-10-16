"""Pure mathematical regression tests; no missile, satellite or sensor data."""
import importlib.util
import math
from pathlib import Path
import unittest

P = Path(__file__).with_name("proof_requirements.py")
spec = importlib.util.spec_from_file_location("proof_requirements", P)
model = importlib.util.module_from_spec(spec)
spec.loader.exec_module(model)


class ProofTests(unittest.TestCase):
    def test_pure_zero_and_one(self):
        self.assertEqual(model.binomial_tail_at_least(0, 5, .2), 1)
        self.assertEqual(model.binomial_tail_at_least(3, 5, 0), 0)
        self.assertEqual(model.binomial_tail_at_least(3, 5, 1), 1)

    def test_binomial_tail_small_exact(self):
        self.assertAlmostEqual(model.binomial_tail_at_least(2, 3, .5), .5, places=12)

    def test_binomial_tail_one_trial(self):
        self.assertAlmostEqual(model.binomial_tail_at_least(1, 1, .2), .2, places=12)

    def test_exact_bound_all_success(self):
        self.assertAlmostEqual(model.exact_one_sided_sensitivity_lower(100, 100), .05 ** .01)

    def test_exact_bound_zero_success(self):
        self.assertEqual(model.exact_one_sided_sensitivity_lower(0, 100), 0)

    def test_exact_bound_nonzero_failure(self):
        lower = model.exact_one_sided_sensitivity_lower(19, 20)
        self.assertLess(lower, 19 / 20)
        self.assertAlmostEqual(model.binomial_tail_at_least(19, 20, lower), .05, places=7)

    def test_required_samples_for_95pct(self):
        self.assertEqual(model.zero_miss_sample_size(.95), 59)

    def test_required_samples_for_99pct(self):
        self.assertEqual(model.zero_miss_sample_size(.99), 299)

    def test_required_samples_for_999pct(self):
        self.assertEqual(model.zero_miss_sample_size(.999), 2995)

    def test_minimality(self):
        for q in (.95, .99, .999):
            n = model.zero_miss_sample_size(q)
            self.assertGreaterEqual(model.exact_one_sided_sensitivity_lower(n, n) + 1e-12, q)
            self.assertLess(model.exact_one_sided_sensitivity_lower(n - 1, n - 1), q)

    def test_zero_alarm_poisson(self):
        self.assertAlmostEqual(30 * model.zero_false_alarm_rate_upper(30), -math.log(.05))

    def test_90_day_requirement(self):
        self.assertAlmostEqual(model.zero_alarm_days_required(1), -30 * math.log(.05))

    def test_alpha_joint_split(self):
        a = model.simultaneous_no_failure_requirements()
        self.assertAlmostEqual(a["one_sided_alpha_each"], .025)
        self.assertEqual(a["zero_miss_independent_trials_required"], 368)
        self.assertAlmostEqual(a["zero_alarm_continuous_exposure_days_required"], 110.666384, places=6)

    def test_uncertain_counted_as_not_on_time(self):
        a = model.conservative_event_tally(["on_time", "late", "unresolved", "missed"])
        self.assertEqual(a["known_events"], 4)
        self.assertEqual(a["guaranteed_on_time"], 1)
        self.assertEqual(a["conservative_non_success"], 3)

    def test_unknown_status_rejected(self):
        with self.assertRaises(ValueError):
            model.conservative_event_tally(["on_time", "verified_by_satellite"])

    def test_empty_census_rejected(self):
        with self.assertRaises(ValueError):
            model.conservative_event_tally([])

    def test_false_alarm_nonzero_no_zero_count_formula(self):
        example = model.demonstration()
        self.assertEqual(example["illustrative_scenario"]["tally"]["known_events"], 10)
        self.assertEqual(example["illustrative_scenario"]["tally"]["guaranteed_on_time"], 8)
        self.assertIn("SYNTHETIC", example["illustrative_scenario"]["operational_qualification"])

    def test_nonzero_alarm_branch(self):
        data={"data_kind":"synthetic","abstract_outcomes":["on_time"],"non_event_exposure_days":1,"false_alarms":1}
        r = model.assess_synthetic_scenario(data)
        self.assertFalse(r["zero_alarm_formula_applicable"])

    def test_real_data_rejected(self):
        data={"data_kind":"real","abstract_outcomes":["on_time"],"non_event_exposure_days":1,"false_alarms":0}
        with self.assertRaises(ValueError):
            model.assess_synthetic_scenario(data)

    def test_invalid_alpha_rejected(self):
        with self.assertRaises(ValueError):
            model.zero_miss_sample_size(.99, alpha=1)
        with self.assertRaises(ValueError):
            model.zero_false_alarm_rate_upper(5, alpha=0)

    def test_invalid_counts_rejected(self):
        with self.assertRaises(ValueError):
            model.exact_one_sided_sensitivity_lower(101,100)
        with self.assertRaises(ValueError):
            model.exact_one_sided_sensitivity_lower(0,0)
        with self.assertRaises(ValueError):
            model.binomial_tail_at_least(3,2,.5)
        with self.assertRaises(ValueError):
            model.conservative_event_tally(["on_time", None])

    def test_invalid_exposure_rejected(self):
        for x in (0, -1, math.inf, math.nan):
            with self.assertRaises(ValueError):
                model.zero_alarm_days_required(x)

    def test_joint_level_more_conservative_than_single(self):
        joint = model.simultaneous_no_failure_requirements()
        self.assertGreater(joint["zero_miss_independent_trials_required"],model.zero_miss_sample_size(.99))
        self.assertGreater(joint["zero_alarm_continuous_exposure_days_required"],model.zero_alarm_days_required(1))

    def test_positive_rate_finite(self):
        self.assertTrue(math.isfinite(model.zero_false_alarm_rate_upper(1)))


if __name__ == "__main__":
    unittest.main()
