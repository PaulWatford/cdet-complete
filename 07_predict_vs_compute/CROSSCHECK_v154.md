# CROSSCHECK_v154 — the SU(N) production route in the 2D thermodynamic limit

**Claims.** (1) The record is lattice-independent: the leading EoS coefficient n₁(N) = −(N−1)d·d' (record × free
single-flavor density d and compressibility d') matches direct SU(N) cluster ED to 1e-7..1e-9 on a 2-site, a 1D
ring-4, and a genuine 2D square cluster (2×3). (2) Thermodynamic limit: the free 2D square-lattice d, d' are
converged k-integrals (nk 120 vs 240 identical) → d=0.671378, d'=0.152391 → 2D SU(6) n₁ = −0.511561 with no
diagonalization. (3) The atomic strong-coupling anchor is lattice-independent, so the v153 two-point construction
extends to 2D.

**Reproduce.** `cd 08_2d_interacting && python3 sun_eos_2d.py` (self-test, ~25s).

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
