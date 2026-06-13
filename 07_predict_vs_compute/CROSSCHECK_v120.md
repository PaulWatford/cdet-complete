# CROSSCHECK_v120 — full dual consolidation at the sign frontier; the integer-spectrum theorem

**Claims.** (1) Surrogate gains sign-side carriers: `surr_l6_gap_modes(lo,hi)`, `surr_l6_occupied(mu)`
over `ATLAS_L6_MULT` {1,6,12,14,27,36,24,36,27,14,12,6,1} (sum 216), + Friedel wavevector — all in C,
no eigendecomposition. (2) They match Python eig exactly: gap(1,2)=0, occ(1.3)=occ(1.9)=156,
occ(6.5)=216. (3) Sharper theorem: cube_hopping(6) is integer-spectrum → no mode in any open unit
interval → freeze exactly μ-rigid in any unit interval (generalizes v118/v119). (4) Brute-C re-stamped
v120 + sign pointer; stable CLI doc fixed. (5) Rebuild all green; side-by-side spans scale (z=2 across
layers) and sign (ρ=Python, A=C, μ-rigidity=surrogate).

**Reproduce.** `cd 08_2d_interacting && python3 csurrogate.py` (gate PASS); `python3
frozen_friedel_map.py` (elementary ρ); cross-check the carriers against `numpy.linalg.eigh(cube_hopping(6))`.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
