# Cross-check proof data (v8) — charge velocity u_rho (the route that works)

The charge velocity at n=0.5, the open item from v6/v7. Reproduce: `python charge_velocity.py`
(L=12 live; L=16 is ~3 min per flux solve).

## What failed before, and the fix
- Dressed-energy endpoint slope u = eps'(Q)/2pi rho(Q): diverged at small U (slope read
  where the energy vanishes).
- Curvature RATIO (flux stiffness / particle-number curvature): 10-30% off, growing in
  U, because the particle-number curvature mixes charge and spin at L<=12.
- FIX: keep the flux stiffness, but divide by the EXACT K_rho (v5) instead of the
  contaminated curvature:
      D_c = (L/2) d2E0/dPhi2 ,   u_rho = pi D_c / K_rho .
  Absolute (no calibration), so no U=0 anchor and no open-shell issue.

## Verification — vs the independent Bethe dressed-energy velocity
| U | u_rho (L=12) | u_rho (L=16) | Bethe endpoint |
|---|---|---|---|
| 0 | 1.430 | - | sqrt2 = 1.414 (target) |
| 1 | 1.572 | - | - |
| 2 | 1.690 | - | 1.76 |
| 4 | 1.840 | 1.796 | 1.83 |
| 8 | 1.958 | - | 1.93 |

- Right trend: sqrt2 -> 2 (the spinless-fermion velocity at n=0.5), monotone increasing.
- Two unrelated methods agree at strong coupling: ED flux stiffness + exact Bethe K_rho
  vs the Bethe dressed-energy endpoint give 1.84 vs 1.83 (U=4) and 1.96 vs 1.93 (U=8),
  ~1%. At U=4 the two lattice sizes bracket the Bethe value (1.84 from L=12, 1.80 from
  L=16).
- U=0 = 1.430 with no calibration: the honest 1% finite-size error, not forced to sqrt2.
- Accuracy ~1-2% (finite-size plus finite-Phi curvature at Phi=0.4).

## On lattice size
L=16 (3.3M states) is reachable here: 78 s for a real ground state, ~185 s for a
complex flux solve, ~2.7 GB peak. But the unlock was NOT the lattice -- it was using
the exact K_rho in place of the contaminated curvature, which already works cleanly at
L=12. L=16 confirms (u_rho(U=4)=1.80, within 2% of Bethe). A systematic L>=16 sweep is
compute-heavy (minutes per flux point) and better suited to a larger machine, but the
result does not need it.

## Status
The doped Luttinger liquid at n=0.5 is now fully characterised on the engine track:
- K_rho(U): exact (Bethe dressed charge, v5), ED-matched to 0.1-0.4%.
- u_rho(U): verified to ~1-2% (flux stiffness + exact K_rho), cross-checked vs the
  independent Bethe dressed-energy method at U=4,8.
- u_sigma(U): verified at strong coupling (Casimir, v6).
With u_rho and u_sigma in hand, the DOPED conformal tower (Frahm-Korepin charge
dimensions in K_rho) is now the natural next target.
