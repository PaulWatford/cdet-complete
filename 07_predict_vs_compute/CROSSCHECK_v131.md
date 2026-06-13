# CROSSCHECK_v131 — CoS prototype vs the engine + integration assessment

**Claims.** (1) cos_harness.c dumps the engine's per-subset D_corr/D_vac and ground-truth C_V (functions
exposed in cdet_engine.h). (2) A faithful Rossi port reproduces C_V exactly (0.0e+00, n=3..7). (3) A
CoS-style subset-convolution (O(2ⁿn²)) reproduces C_V to machine precision (2e-15). (4) Honest cost: 3ⁿ
combine overtakes 2ⁿn² only at n≥12; the shared 2ⁿn³ determinant cost dominates until ~n=16. (5) Ranked
integration list in the result (forward DP, SU(N), self-energy, MC symmetrization, subset-conv, R-pruning,
QTT).

**Reproduce.** `cd 08_2d_interacting && gcc -O2 -I../engine -o cosh cos_harness.c ../engine/cdet_engine.c
-lm && ./cosh 5`; `python3 cos_prototype.py`.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
