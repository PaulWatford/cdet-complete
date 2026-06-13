# Cross-check proof data (v11) — doped-tower deficit is finite-size (~1/L^2 -> exact 2)

v10 verified x_4 -> 2 K_rho on L=12 with a small raw deficit (~2-3%), flat in U, argued
to be finite-size. v11 proves it at the U=0 anchor, where the 4k_F gap and the charge
velocity are both exactly known at any L. Reproduce: `python doped_tower_scaling.py`.

## Why U=0 (and not a bigger interacting lattice)
The next closed shell at quarter filling is L=20 (N_up=N_dn=5): C(20,5)^2 = 240,374,016
states, beyond brute-force ED (L=12 is the only feasible closed shell; L=16 is open-
shell). At U=0 the model is free fermions, so the 4k_F gap is exact by DP over orbital
occupations and v_F = 2 sin k_F = sqrt2 at quarter filling -- exact at any L. v10 already
showed the deficit is ~U-independent, so U=0 convergence is the finite-size story.

## Validation (licenses the cheap route)
Free-fermion 4k_F gap at L=12, U=0 = 1.46410, EQUALS the many-body ED gap (1.46410,
doped_tower.py). The free-fermion calculation is exact for the gap, so it is the right
tool for the larger L the many-body ED cannot reach.

## Result — x_4(U=0,L) = gap(4k_F) L /(2 pi v_F), exact velocity v_F = sqrt2
| L | gap(4k_F) | x_4 | deficit x_4/2 - 1 |
|---|-----------|-----|-------------------|
| 12 | 1.46410 | 1.9772 | -1.14% |
| 20 | 0.88493 | 1.9918 | -0.41% |
| 28 | 0.63337 | 1.9958 | -0.21% |
| 36 | 0.49303 | 1.9975 | -0.13% |
| 44 | 0.40356 | 1.9983 | -0.08% |

1/L^2 fit: x_4(L) = 2.0000 - 3.277/L^2  ->  thermodynamic x_4 = 2.0000 (exact: 2).

## Reading it
- The deficit decays monotonically as ~1/L^2 (about 3.3/L^2) and the extrapolation hits
  the exact dimension 2 to four decimals. The v10 raw deficit is finite-size and vanishes
  in the thermodynamic limit -- not a model error.
- Note on velocities: x_4(U=0,L=12) here is 1.9772 (exact v_F), vs 1.9549 in v10 (which
  used the v8 finite-size u_rho). The ~1.1% difference is the finite-size error of the v8
  velocity itself -- a SEPARATE finite-size effect. v11 isolates the gap's convergence by
  using the exactly-known U=0 velocity, cleanly.

## Status
FINITE-SIZE-CONTROLLED (v11): the doped-tower charge dimension converges to the exact 2
as ~1/L^2 at U=0; with v10 (tracks 2 K_rho at finite U, deficit flat in U) this closes
the doped charge-tower result. Remaining ceiling, stated honestly: a large-L INTERACTING
confirmation needs L=20 (240M states) -- beyond brute force here, squarely where the
diagrammatic Monte Carlo engine, not exact diagonalisation, is the right instrument.
