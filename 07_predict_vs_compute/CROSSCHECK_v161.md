# CROSSCHECK_v161 — consolidation of the v157–160 arc (frozen baseline retained for parity)

**Claims.** (1) Health gate `consolidation_v161.py` re-proves coherence: v147 invariants, frozen-baseline parity
(hybrid 0.00e+00 vs reference), v157 auto-fast bit-identical (~28×), v158 chaining, v159 two-particle exclusion
(10/10), v160 conformal-Borel beats Padé. (2) Triple-run benchmark recorded with the frozen reference as the parity
anchor (surrogate 3.55e-15 / hybrid 0.00e+00 / brute force 194/194). (3) Improvement cycle: the safe set_freeze
precompute is bit-identical but negligible (~0.6%, not added); the low-rank freeze update is identified and deferred
as parity-risky. (4) Frozen reference untouched.

**Reproduce.** `cd 08_2d_interacting && python3 consolidation_v161.py` (~4 s) and `python3 triple_benchmark.py` (~6 s).

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
