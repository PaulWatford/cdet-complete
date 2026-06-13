# CROSSCHECK_v124 — projector fast path, continuous freeze, run-to-log harness

**Claims.** (1) Projector fast path regroups g0 by distinct eigenvalue (precompute P[Δr][ε] for ~7
vertex displacements; propagator O(#distinct ε)). Exact: L=6 fast==direct (A=1.341555, c1=−234.4268).
Speedup L=12 59.5s→0.81s (73×); L=48 32.5s. (2) Continuous freeze (mode 2) for non-crystallographic L:
L=8 μ=1.0 lowest-empty eigenvalue=√2 (irrational); z rises 1.243/1.267/1.290/1.317 toward √2. (3)
run_to_log.py streams to a log (line-buffered+fsync), detects NONFINITE / nonzero exit / signal, logs
last_good_beta; engine NaN guard prints '# NONFINITE' and stops. (4) L=100 (1e6 sites) is a day-long
z-flow with the fast path; direct ceiling ~L=16.

**Reproduce.** `cd 08_2d_interacting && gcc -O2 -Wall -Werror -std=c11 -pedantic -o cpw
cdet_planewave_engine.c -lm`; `./cpw grid 24 24 1 12 2048 31 0.002 0 2 1 2 4 1.845 -L 6 -fast` (==direct);
`./cpw grid 24 72 24 12 2048 31 0.002 2 2 1 2 4 1.0 -L 8` (→√2); `python3 run_to_log.py selftest`;
`python3 hybrid_scaling_test.py`.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
