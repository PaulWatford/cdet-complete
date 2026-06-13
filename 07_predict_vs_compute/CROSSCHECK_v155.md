# CROSSCHECK_v155 — the second-order EoS coefficient, record-decomposed

**Claims.** (1) n₂(N) = (N−1)²·a + (N−1)·b. (2) a = d(d′² + ½·d·d″) is the self-consistent Hartree iteration
(free single-flavor derivatives only); it matches the fitted (N−1)² coefficient to 1.8e-7. (3) The decomposition
(a exact + b fitted) predicts n₂(N=6) = 1.046125 vs direct SU(6) ED 1.046266 (err 1.4e-4). (4) Thermodynamic limit:
a from converged 2D k-integrals → a_2D(μ=1,β=2)=0.005622, so the dominant (N−1)² part of the 2D SU(6) n₂ is
25·a_2D=0.140544, exact with no diagonalization; the bubble b is the subleading correction.

**Reproduce.** `cd 08_2d_interacting && python3 sun_eos_n2.py` (self-test, N≤5, ~6s). N=6 row in SUN_EOS_N2_RESULT.md.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
