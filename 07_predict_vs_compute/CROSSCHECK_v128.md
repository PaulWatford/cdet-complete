# CROSSCHECK_v128 — the c1 sign in L is arithmetic jitter, not a Friedel period

**Claims.** (1) sign(c1) sequence L=24..52: − + + + − − + −, seed-stable. (2) Period-16 falsified: 28/44
(+/−) and 36/52 (+/−) mismatch; breakers L=28,36,44 seed-stable (seeds 31/17). (3) Cause: the lowest-empty
multiplet's dominant |kx|/L jumps number-theoretically (0.29,0.13,0.05,0.0,0.07,0.0,0.0,0.06 for L=24..52),
no period. (4) v119 contrast: A integrates the whole sea → clean continuum wavevector, sign converges; c1
picks one lowest-empty multiplet → jitter. (5) No period to derive; the v116 rule is arithmetic at finite L,
marginal in the continuum.

**Reproduce.** `cd 08_2d_interacting && gcc -O2 -Wall -Werror -std=c11 -pedantic -o cpw
cdet_planewave_engine.c -lm`; for L in 24,28,...,52: `./cpw grid 24 24 1 10 1536 31 0.002 2 2 1 2 4 1.0 -L
<L> -fast` (signed c1 col 4); seed-check with seed 17; `python3 probe_jitter_analysis.py`.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
