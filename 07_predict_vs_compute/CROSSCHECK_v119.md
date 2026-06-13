# CROSSCHECK_v119 — the full 2D Friedel sign-map, resolved at the elementary level

**Claims.** (1) The full A-map over (x,y,0) is structured but messy (multi-propagator superposition;
fixed sites break symmetry). (2) The elementary object ρ(0,r)=Σ_{occ k}U[0,k]U[r,k] = FT of the
occupied region has a cube-symmetric sign-map. (3) Short wavelength ~2–3 sites; dominant wavevector
(120°,180°) = the level-1|2 boundary modes (ε=+1 at k=2,4; ε=+2 at k=3). (4) μ-invariance is analytic
and exact: zero modes in the gap (1,2) → occupied set rigid → ρ identical for all μ∈(1,2). (5)
Reconciles v117: the elementary wavelength is short; A's sign superposes these, giving the longer
apparent envelope (v117 core survives).

**Reproduce.** `cd 08_2d_interacting && python3 frozen_friedel_map.py` (self-test PASS); the A-map via
`./cse grid 24 24 1 16 2048 31 0.002 0 2 43 80 <idx>` for idx=x+6y over the plane.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
