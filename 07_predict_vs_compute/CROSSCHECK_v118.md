# CROSSCHECK_v118 — move μ: prediction falsified; the frozen Fermi surface is discrete and rigid

**Claims.** (1) Engine grid takes optional μ (arg 14). (2) Moving μ∈{1.3,1.6,1.9}: the x-scan sign(A)
= (−,−,−,+,+) at *every* μ (reproducible across seeds; A barely moves) — μ-invariant. (3) The z-flow
is μ-invariant too (z=1.786/1.853/1.887 at μ=1.3, within 0.005 of μ=1.845 and 1.9), all → 2. (4) The
registered continuous-2k_F prediction (λ: 3.64→9.89 sites) is falsified. (5) Root cause: the freeze
makes occupations discrete, so the Fermi surface is the level-1|level-2 boundary, fixed for all μ in
(1,2). (6) Corrects v117: the 2k_F(μ) wavelength match was coincidental; one discrete object governs
both scale and sign, rigid in μ.

**Reproduce.** `cd 08_2d_interacting && python3 mu_unification_test.py` (self-test PASS); scans via
`./cse grid 24 24 1 16 2048 31 0.002 0 2 8 43 <j> <mu>` (sign) and `./cse grid 24 72 24 10 2048 31
0.002 0 2 1 2 4 <mu>` (z-flow).

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
