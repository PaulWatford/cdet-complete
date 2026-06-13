# CROSSCHECK_v145 — SU(N) step 4 + the gravity-loop hint realized in N

**Claims.** (1) Step 4: the 2-site SU(N) second-order EoS coefficient n2(N) is a low-degree polynomial in N
(deg-3 fit N=2..5 predicts N=6 to ~3e-4) — the record persists to second order. (2) The gravity-loop hint: the
record makes the coefficients polynomial in N, so they obey a finite linear recurrence in N (c1's 3rd
finite-difference is 7e-15), their N-generating-function is rational (denominator (1−x)^{d+1}, residual 7e-15),
and the all-N dependence resums exactly — from c1 at N=1,2,3 reconstruct c1(6) exactly and the large-N rate
(−β·d²). Same mechanism as the gravity loops (finite recurrence → rational GF → exact resummation), realized in
N not U; characteristic root 1 (polynomial) vs gravity's cubic (exponential). This is why CoS is N-independent.

**Reproduce.** `cd 08_2d_interacting && python3 sun_resummation_N.py`.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
