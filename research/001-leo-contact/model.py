"""SpaceЖ research 001: first-order circular-LEO contact and downlink budget.

This is a mathematical *screening model*, not flight software, radio
permission, link authorization, a pass predictor, or an operational guarantee.
No third-party Python dependencies.
"""
from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass, replace

C_M_PER_S = 299_792_458.0
THERMAL_NOISE_DBM_PER_HZ = -174.0  # approximation for 290 K reference


@dataclass(frozen=True)
class Assumptions:
    earth_radius_km: float = 6371.0
    earth_mu_km3_s2: float = 398_600.4418
    altitude_km: float = 550.0
    elevation_deg: float = 15.0
    frequency_mhz: float = 437.0
    satellite_power_w: float = 2.0
    satellite_antenna_gain_dbi: float = 0.0
    receiver_antenna_gain_dbi: float = 9.0
    miscellaneous_loss_db: float = 5.0
    receiver_noise_figure_db: float = 4.0
    raw_bit_rate_bps: float = 9600.0
    # Link closure is judged against ideal coherent BPSK with no coding and no
    # implementation loss at this bit-error rate. Framing, preamble and bit
    # stuffing enter only as one illustrative efficiency factor.
    target_bit_error_rate: float = 1e-5
    framing_efficiency: float = 0.8


@dataclass(frozen=True)
class Result:
    slant_range_km: float
    orbit_period_min: float
    central_angle_half_width_deg: float
    ideal_nonrotating_overhead_contact_min: float
    free_space_path_loss_db: float
    received_power_dbm: float
    carrier_to_noise_density_db_hz: float
    energy_per_bit_to_noise_density_db: float
    required_energy_per_bit_to_noise_density_db: float
    link_margin_db: float
    ideal_raw_kilobytes_per_pass: float
    useful_kilobytes_per_pass: float


def bpsk_bit_error_rate(ebn0_db: float) -> float:
    """Ideal coherent BPSK bit-error rate: BER = erfc(sqrt(Eb/N0)) / 2."""
    return 0.5 * math.erfc(math.sqrt(10 ** (ebn0_db / 10)))


def required_ebn0_db(target_bit_error_rate: float) -> float:
    """Eb/N0 in dB at which ideal coherent BPSK meets the target bit-error rate."""
    if not (0 < target_bit_error_rate < 0.5):
        raise ValueError("Target bit-error rate must be between 0 and 0.5")
    low, high = -20.0, 40.0
    for _ in range(100):
        mid = (low + high) / 2
        if bpsk_bit_error_rate(mid) > target_bit_error_rate:
            low = mid
        else:
            high = mid
    return (low + high) / 2


def solve(a: Assumptions = Assumptions()) -> Result:
    """Compute an idealized *downlink* for a circular orbit and overhead pass.

    The ground point does not rotate with Earth in this toy geometry; this is
    not a real pass schedule nor a universal bound on maximum contact time.
    The link margin compares the modelled edge-of-pass Eb/N0 with what ideal
    BPSK needs at the target bit-error rate; it is not a demodulator test.
    """
    if a.earth_radius_km <= 0 or a.earth_mu_km3_s2 <= 0:
        raise ValueError("Earth radius and gravitational parameter must be positive")
    if a.altitude_km <= 0:
        raise ValueError("Orbital altitude must be positive")
    if not (0 <= a.elevation_deg < 90):
        raise ValueError("Minimum elevation must be in [0, 90) degrees")
    if a.frequency_mhz <= 0 or a.satellite_power_w <= 0 or a.raw_bit_rate_bps <= 0:
        raise ValueError("Frequency, transmitter power and raw bit rate must be positive")
    if a.miscellaneous_loss_db < 0 or a.receiver_noise_figure_db < 0:
        raise ValueError("Loss and noise figure cannot be negative")
    if not (0 < a.framing_efficiency <= 1):
        raise ValueError("Framing efficiency must be in (0, 1]")

    r = a.earth_radius_km
    orbit_radius = r + a.altitude_km
    e = math.radians(a.elevation_deg)
    # The line of sight geometry follows from the cosine rule in the triangle
    # Earth center - ground site - spacecraft.
    slant_km = math.sqrt(orbit_radius**2 - (r * math.cos(e))**2) - r * math.sin(e)

    # Central angle between nadir ground point and observer, at the cutoff.
    half_angle_rad = math.acos(r * math.cos(e) / orbit_radius) - e
    mean_motion_rad_s = math.sqrt(a.earth_mu_km3_s2 / orbit_radius**3)
    orbital_period_s = 2 * math.pi / mean_motion_rad_s
    ideal_contact_s = 2 * half_angle_rad / mean_motion_rad_s

    # Friis free-space loss with SI units inside the logarithm.
    frequency_hz = a.frequency_mhz * 1e6
    loss_db = 20 * math.log10(4 * math.pi * slant_km * 1e3 * frequency_hz / C_M_PER_S)
    tx_dbm = 10 * math.log10(a.satellite_power_w * 1000)
    rx_dbm = (tx_dbm + a.satellite_antenna_gain_dbi
              + a.receiver_antenna_gain_dbi - a.miscellaneous_loss_db - loss_db)
    n0_dbm_per_hz = THERMAL_NOISE_DBM_PER_HZ + a.receiver_noise_figure_db
    cn0_db_hz = rx_dbm - n0_dbm_per_hz
    ebn0_db = cn0_db_hz - 10 * math.log10(a.raw_bit_rate_bps)
    required_db = required_ebn0_db(a.target_bit_error_rate)
    raw_kb = a.raw_bit_rate_bps * ideal_contact_s / 8 / 1000

    return Result(
        slant_range_km=slant_km,
        orbit_period_min=orbital_period_s / 60,
        central_angle_half_width_deg=math.degrees(half_angle_rad),
        ideal_nonrotating_overhead_contact_min=ideal_contact_s / 60,
        free_space_path_loss_db=loss_db,
        received_power_dbm=rx_dbm,
        carrier_to_noise_density_db_hz=cn0_db_hz,
        energy_per_bit_to_noise_density_db=ebn0_db,
        required_energy_per_bit_to_noise_density_db=required_db,
        link_margin_db=ebn0_db - required_db,
        ideal_raw_kilobytes_per_pass=raw_kb,
        useful_kilobytes_per_pass=raw_kb * a.framing_efficiency,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--altitude-km", type=float, default=550)
    parser.add_argument("--elevation-deg", type=float, default=15)
    parser.add_argument("--frequency-mhz", type=float, default=437)
    parser.add_argument("--power-w", type=float, default=2)
    parser.add_argument("--raw-bps", type=float, default=9600)
    parser.add_argument("--sweep", choices=("none", "elevation", "altitude"), default="none")
    args = parser.parse_args()
    a = Assumptions(altitude_km=args.altitude_km, elevation_deg=args.elevation_deg,
                    frequency_mhz=args.frequency_mhz, satellite_power_w=args.power_w,
                    raw_bit_rate_bps=args.raw_bps)
    if args.sweep == "none":
        print(json.dumps({"assumptions": asdict(a), "result": asdict(solve(a))}, indent=2))
        return
    cases = (5, 10, 15, 30) if args.sweep == "elevation" else (400, 550, 800, 1200)
    print("parameter,slant_km,contact_min,ebn0_db,margin_db,ideal_raw_kB,useful_kB")
    for value in cases:
        case = replace(a, elevation_deg=value) if args.sweep == "elevation" else replace(a, altitude_km=value)
        x = solve(case)
        print(f"{value},{x.slant_range_km:.1f},{x.ideal_nonrotating_overhead_contact_min:.2f},"
              f"{x.energy_per_bit_to_noise_density_db:.2f},{x.link_margin_db:.2f},"
              f"{x.ideal_raw_kilobytes_per_pass:.1f},{x.useful_kilobytes_per_pass:.1f}")


if __name__ == "__main__":
    main()
