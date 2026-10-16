"""Deterministic checks for SpaceЖ LEO first-order screening model."""
import math
import unittest
from dataclasses import replace
from model import Assumptions, solve


class GeometryAndLinkTests(unittest.TestCase):
    def test_reference_case(self):
        r = solve()
        self.assertAlmostEqual(r.slant_range_km, 1518.016718, places=4)
        self.assertAlmostEqual(r.orbit_period_min, 95.502118, places=4)
        self.assertAlmostEqual(r.ideal_nonrotating_overhead_contact_min, 6.489606, places=4)
        self.assertAlmostEqual(r.free_space_path_loss_db, 148.882943, places=4)
        self.assertAlmostEqual(r.received_power_dbm, -111.872643, places=4)
        self.assertAlmostEqual(r.energy_per_bit_to_noise_density_db, 18.304645, places=4)
        self.assertAlmostEqual(r.ideal_raw_kilobytes_per_pass, 467.251648, places=4)

    def test_minimum_elevation_tradeoff(self):
        a = solve(replace(Assumptions(), elevation_deg=5))
        b = solve(replace(Assumptions(), elevation_deg=30))
        self.assertGreater(a.ideal_nonrotating_overhead_contact_min, b.ideal_nonrotating_overhead_contact_min)
        self.assertLess(a.energy_per_bit_to_noise_density_db, b.energy_per_bit_to_noise_density_db)
        self.assertGreater(a.slant_range_km, b.slant_range_km)

    def test_doubling_frequency_adds_six_db_path_loss(self):
        a = Assumptions()
        b = replace(a, frequency_mhz=2 * a.frequency_mhz)
        self.assertAlmostEqual(solve(b).free_space_path_loss_db - solve(a).free_space_path_loss_db,
                               20 * math.log10(2), places=9)

    def test_doubling_power_adds_three_db_received_and_ebn0(self):
        a = Assumptions()
        b = replace(a, satellite_power_w=2*a.satellite_power_w)
        self.assertAlmostEqual(solve(b).received_power_dbm - solve(a).received_power_dbm,
                               10 * math.log10(2), places=9)
        self.assertAlmostEqual(solve(b).energy_per_bit_to_noise_density_db - solve(a).energy_per_bit_to_noise_density_db,
                               10 * math.log10(2), places=9)

    def test_higher_altitude_longer_ideal_pass_but_weaker_edge_signal(self):
        a = solve(replace(Assumptions(), altitude_km=400))
        b = solve(replace(Assumptions(), altitude_km=1200))
        self.assertLess(a.ideal_nonrotating_overhead_contact_min, b.ideal_nonrotating_overhead_contact_min)
        self.assertGreater(a.energy_per_bit_to_noise_density_db, b.energy_per_bit_to_noise_density_db)

    def test_invalid_inputs_rejected(self):
        for a in (replace(Assumptions(), elevation_deg=-1),
                  replace(Assumptions(), elevation_deg=90),
                  replace(Assumptions(), altitude_km=0),
                  replace(Assumptions(), raw_bit_rate_bps=0),
                  replace(Assumptions(), frequency_mhz=-1),
                  replace(Assumptions(), receiver_noise_figure_db=-2)):
            with self.subTest(a=a), self.assertRaises(ValueError):
                solve(a)


if __name__ == "__main__":
    unittest.main()
