# SpaceЖ Research 001 — Low Earth orbit contact and link-budget screening

**16 October 2026 | Reproducible first-order model | Not an operational satellite link**

## Actual engineering question

Can one **authorized, cooperating** low-Earth-orbit satellite downlink deliver enough low-rate data during a pass to be useful for telemetry or small store-and-forward messages? This is **not** a Starlink replacement, a satellite service, a statement of spacecraft availability, or evidence of a built communications network.

### Hypothetical assumptions

| Assumption | Value |
| --- | ---: |
| Spherical Earth radius | 6,371 km |
| Gravitational parameter | 398,600.4418 km³/s² |
| Circular satellite orbit altitude | 550 km |
| Ground-station minimum elevation | 15 degrees |
| Downlink carrier | 437 MHz, illustrative **not assigned** frequency |
| Satellite RF transmit power | 2 W |
| Satellite antenna gain | 0 dBi |
| Receiver antenna gain | 9 dBi |
| Miscellaneous losses | 5 dB |
| Receiver noise figure | 4 dB |
| Raw bit rate | 9,600 bit/s |

The toy model assumes a nonrotating spherical Earth, Keplerian circular orbit, and perfect overhead pass. It **cannot** predict actual contact times or useful throughput. The model excludes antenna pointing, polarization losses, terrain, interference, Doppler, coding, packet loss, and access authorizations.

### Geometry and radio equations

With Earth radius \(R\), orbital altitude \(h\), and ground-station cutoff elevation \(\varepsilon\),

\[
\rho=\sqrt{(R+h)^2-R^2\cos^2\varepsilon}-R\sin\varepsilon.
\]

The maximum central-angle excursion within the cutoff is

\[
\psi=\arccos\left(\frac{R\cos\varepsilon}{R+h}\right)-\varepsilon.
\]

For circular mean motion \(n=\sqrt{\mu/(R+h)^3}\), the illustrative overhead contact duration is \(t_{\rm ideal}=2\psi/n\). The free-space downlink loss is

\[
L_{\rm FS}=20\log_{10}\!\left(\frac{4\pi\rho f}{c}\right).
\]

At roughly 290 K, the receiver noise density is approximated as \(-174 + NF\) dBm/Hz. Received power, signal energy density and ideal raw data follow from the link-budget assumptions (see `model.py`).

### Reference result

| Result | Hypothetical model output |
| --- | ---: |
| Slant range at 15° cutoff | **1,518.0 km** |
| Orbital period | **95.50 minutes** |
| Ideal overhead contact | **6.49 minutes** |
| Free-space loss | **148.88 dB** |
| Received power | **−111.87 dBm** |
| \(C/N_0\) | **58.13 dB-Hz** |
| \(E_b/N_0\) | **18.30 dB** |
| Ideal raw contact bytes | **467.3 decimal kB** |

### Elevation-mask sensitivity

| Elevation | Slant range | Ideal contact | Edge \(E_b/N_0\) | Ideal raw data |
| --- | ---: | ---: | ---: | ---: |
| 5° | 2,205 km | 9.82 min | 15.06 dB | 707 kB |
| 10° | 1,815 km | 7.94 min | 16.75 dB | 572 kB |
| 15° | 1,518 km | 6.49 min | 18.30 dB | 467 kB |
| 30° | 993 km | 3.79 min | 21.99 dB | 273 kB |

**Interpretation:** Lower elevation provides more theoretical contact time but worse weakest-point link margin and often more local obstruction. Contact length alone does not predict successful data delivery.

### Falsifiable next experiment

Select one *authorized, publicly receivable* educational or research telemetry signal. Determine legal/data-license permissions. Record actual acquisition/loss of signal, error rates, decoded frames and useful payload bytes; compare these with an SGP4 pass prediction using approved station information. Publish only permissible aggregate findings. A receive-only demonstration does not prove two-way communications or satellite broadband.

### Reproduce

No third-party dependencies; Python 3.9+.

```sh
python3 research/001-leo-contact/model.py
python3 research/001-leo-contact/model.py --sweep elevation
python3 research/001-leo-contact/model.py --sweep altitude
python3 -m unittest discover -s research/001-leo-contact -p 'test_*.py' -v
```

Six deterministic tests passed on 16 October 2026 and the reference model output matched `baseline_result.json`. Do not treat a passing test as an RF field measurement.

### Sources
- [NASA — Small Spacecraft Ground Data Systems and Mission Operations](https://www.nasa.gov/smallsat-institute/sst-soa/ground-data-systems-and-mission-operations/)
- [CelesTrak — Orbital coordinate and observer geometry](https://www.celestrak.org/columns/v02n02/)
- [NASA/JPL — Deep Space Network Telecommunications Link Design Handbook](https://deepspace.jpl.nasa.gov/dsndocs/810-005/)
