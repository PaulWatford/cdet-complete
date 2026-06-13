# CROSSCHECK_v123 — phase 2 of the hybrid: plane-wave determinant engine; multi-lattice scale law

**Claims.** (1) `cdet_planewave_engine.c` computes A, c1 at arbitrary L on the plane-wave propagator
g0=(1/N)Σ cos(2π k·Δr/L)·val — no eigenvectors, no spectrum file. (2) At L=6 PROBE=2 it reproduces the
stable engine exactly (A=1.341555, c1=−234.4268; val worst rel dev 0.00e+00). (3) Scale law
z(∞)=lowest-empty-level: L=4 PROBE=2 μ=1.0 → z 1.678/1.800/1.846→2; L=6 PROBE=3 μ=2.5 →
z 2.773/2.852/2.862→3. (4) z(∞) is the lowest-empty level (size- and probe-general), not constant 2.
(5) Cost ~linear in N. (6) Open: non-crystallographic L needs a continuous-threshold freeze.

**Reproduce.** `cd 08_2d_interacting && gcc -O2 -Wall -Werror -std=c11 -pedantic -o cpw
cdet_planewave_engine.c -lm && ./cpw val < cdet_stable_engine_refs.txt` (L=6 validation);
`./cpw grid 24 72 24 12 2048 31 0.002 0 2 1 2 4 1.0 -L 4` (test 1); `python3 hybrid_phase2_test.py`.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
