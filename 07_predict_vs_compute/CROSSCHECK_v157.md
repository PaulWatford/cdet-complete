# CROSSCHECK_v157 — triple-run benchmark + hybrid auto-fast

**Claims.** (1) All three models agree against the frozen anchor: surrogate dev 3.55e-15 (exact on coverage);
hybrid val 0.00e+00 vs reference; brute force 194/194. (2) The hybrid projector fast path is bit-identical to the
default (val 0.00e+00 and grid output unchanged) and is now auto-enabled for crystallographic L → ~26× grid
speedup (0.34s vs 8.83s, NT=1500), with a -nofast escape. (3) The frozen reference source is untouched.

**Reproduce.** `cd 08_2d_interacting && python3 triple_benchmark.py` (~6s); `./cpw val < cdet_stable_engine_refs.txt`
→ 0.00e+00.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
