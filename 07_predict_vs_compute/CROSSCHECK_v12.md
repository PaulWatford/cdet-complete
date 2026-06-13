# Cross-check proof data (v12) — spin-charge separation made quantitative

v9 detected spin-charge separation as a rising 2k_F/4k_F ratio; v12 extracts the two
velocities behind it from the same gaps and shows them split. Reproduce:
`python spin_charge_velocities.py`.

## Method (two gaps, one exact input, two velocities)
- 4k_F is pure charge:   gap(4k_F) = (2 pi/L)(2 K_rho u_rho)  -> u_rho = gap(4k_F)L/(4 pi K_rho)
- 2k_F is charge+spin:   gap(2k_F) = (2 pi/L)(K_rho u_rho/2 + u_sigma/2)
                         -> u_sigma = gap(2k_F)L/pi - K_rho u_rho
K_rho is the exact Bethe value (v5); gaps from doped_tower.py (L=12, n=0.5).

## Anchor — U=0 (no separation, free fermions): u_rho = u_sigma = v_F = sqrt2
Extraction gives u_rho = u_sigma = 1.3981 (1.1% below sqrt2 = 1.4142, finite-size). The
two velocities coincide exactly at U=0, as they must; they split only once U>0.

## Result (L=12, n=0.5)
| U | u_rho (spectral) | u_rho (v8 flux) | u_sigma | u_rho/u_sigma | K_rho | cross-check |
|---|------------------|-----------------|---------|---------------|-------|-------------|
| 0 | 1.3981 | 1.4304 | 1.3981 | 1.000 | 1.0000 | 2.3% |
| 1 | 1.5334 | 1.5718 | 1.1484 | 1.335 | 0.9006 | 2.4% |
| 2 | 1.6429 | 1.6896 | 0.9799 | 1.677 | 0.8187 | 2.8% |
| 4 | 1.7821 | 1.8403 | 0.7519 | 2.370 | 0.7118 | 3.2% |
| 8 | 1.8958 | 1.9582 | 0.5007 | 3.786 | 0.6166 | 3.2% |

## Reading it
- u_rho RISES (1.40 -> 1.90), u_sigma FALLS (1.40 -> 0.50); the separation ratio
  u_rho/u_sigma grows from 1.0 to ~3.8. This is the quantitative content of the v9 break.
- CROSS-CHECK: u_rho from the 4k_F spectral gap agrees with the INDEPENDENT v8 charge
  velocity (flux stiffness / exact K_rho) to ~2-3% across U -- two unrelated routes,
  finite-size consistent. This is what makes the u_rho leg trusted, not merely extracted.
- u_sigma at quarter filling is a NEW observable (v6 gave u_sigma only at half filling).
  Its hard anchor is U=0 (= v_F); its U>0 values are an extraction (2 gaps + 1 exact K_rho
  fix 2 velocities, so u_sigma is determined, not over-determined). Honest scope: it is
  not yet independently cross-checked at U>0.

## Status & next (v13)
SEPARATION-QUANTIFIED (v12): both Luttinger velocities extracted from the doped tower;
coincident at U=0, splitting with U; u_rho confirmed against v8. Open: an INDEPENDENT
quarter-filling u_sigma -- the lowest TRIPLET (S=1) gap at 2k_F, which needs S^2
resolution -- to upgrade u_sigma from extracted to verified. Separately, a large-L
INTERACTING tower point (L=20 = 240M states) stays beyond ED; from the DiagMC engine it
needs a dynamical charge correlator + analytic continuation, with the per-order 2^n cost
the documented wall -- a distinct effort, flagged honestly, not an ED run.
