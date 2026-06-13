# Cross-check proof data (v4) — charge Luttinger parameter K_rho

New observable: the charge Luttinger parameter of the DOPED 1D Hubbard ring
(n=0.5, L=12), the U-dependent quantity that governs the 2k_F/4k_F competition.
Reproduce: `python luttinger_K.py`.

Path A (ED): K_rho from the charge structure-factor slope N(q)->(K_rho/pi)|q|,
calibrated so U=0 gives 1. Path B: weak-coupling formula + exact strong-coupling limit.

| U | K_ED (Path A) | K weak-coupling (Path B) | rel.diff |
|---|---|---|---|
| 0  | 1.0000 | 1.0000 | 0.0% (calibration) |
| 1  | 0.8971 | 0.9035 | 0.7% |
| 2  | 0.8167 | 0.8304 | 1.7% |
| 4  | 0.7111 | 0.7254 | 2.0% |
| 8  | 0.6163 | 0.5975 | 3.1% |
| 16 | 0.5578 | 0.4662 | 19.7% (formula breaks) |

## Reading
- Weak-to-moderate U (<=8): ED and the weak-coupling formula agree to a few percent.
  Independent validation of the ED extraction where the analytic handle is valid.
- Strong U (16): the weak-coupling formula leaves the physical range (0.466 < 1/2),
  while ED stays above 1/2 (0.558), heading to the exact strong-coupling value 1/2.
  Here it is the FORMULA that fails; the cross-check locates its regime boundary.

K_rho falls monotonically from 1 (free) toward 1/2 (strong coupling), the textbook
doped-Luttinger-liquid behaviour, bracketed by both analytic limits.

## Status
- K_rho is a new observable, ED-extracted, with a two-sided analytic cross-check.
- It is NOT yet machine-precision exact: the exact Path B is the Bethe-ansatz
  dressed-charge integral equation, which would give K_rho(U) analytically to compare
  point-by-point. That is the next step and ties directly to the Bethe benchmark.
- Honest label: ED-validated to a few percent against weak coupling, exact in both
  limits; the full exact-Bethe cross-check is pending.
