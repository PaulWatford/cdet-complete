# CROSSCHECK_v159 — two-particle chained two-round run

**Claims.** (1) The two-particle chained-continuation walk sweeps the full pair-config space (10/10, C(5,2)) with
exclusion (Pauli) held throughout (never double-occupies). (2) The chained continuation's ~√2 error reduction
reaches both the one-body amplitude A (1.44×) and the two-body interaction response c₁ (1.39×), vs an NT=20000
reference — so chaining helps the interaction, not just the amplitude. (3) The frozen reference is untouched.

**Reproduce.** `cd 08_2d_interacting && python3 two_particle_run.py` (~20s); `./cpw val < cdet_stable_engine_refs.txt`
→ 0.00e+00.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
