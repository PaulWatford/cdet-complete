# CROSSCHECK_v139 — hybrid stress test + robustness guards

**Claims.** (1) Hybrid robust: validation == stable @L6 (0.00e+00); fast == direct bit-identical; 2.7M sites
(L=140) in 193 s; probe_val at L=100 = 1.000192 = surrogate; NaN guard fires cleanly. (2) f64 walls at β≈100,
long-double reaches β≥200 (use -DUSE_LD deep). (3) Three input failure modes found + guarded (input-only,
val stays 0.00e+00): non-crystallographic L + mode 0/1 (z~1e23), large delta (c1 sign flip), delta=0 (c1=NaN).

**Reproduce.** `cd 08_2d_interacting && python3 stress_test_v139.py` (fast checks). Scans: `./cpw grid 36 36 1
6 256 31 0.002 2 2 1 2 4 1.0 -L 100 -fast` (1e6 sites); deep-β f64 vs `cpwld`.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875). Hybrid val gate stays 0.00e+00 after the guards.
