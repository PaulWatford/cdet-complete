# CROSSCHECK_v73 — the learned orientation channel: closure from the learned side

**Claims.** (1) Frozen protocol: train on 9 cells (L=6; μ 0.5/1.0/2.0; extents 3–5; 108 labeled
line geometries), evaluate on held-out unseen μ=1.5 (all extents) and unseen L=4; gate pre-set at
75%. (2) L2-logistic with physics-informed features: train 74%, held-out mean 33% with consistent
anti-prediction at unseen μ (0% on one cell). (3) Nonlinear MLP (24 hidden, harmonics m=1,2,
pairwise interference features): train 74%, held-out 35%. (4) Structural mechanism identified: a
phase wraps in μ; smooth models cannot interpolate a wrap from sparse samples — predicting unseen-μ
orientation requires the μ-period, i.e., the law v69/v71 proved has no sub-engine form. (5) The
orientation channel is closed at this scope from both directions (derived ladder + learned models);
remaining routes named: dense tabulation, engine-derived features, or the μ-period analytically.

**Reproduce.** `cd 08_2d_interacting && python3 learned_orientation.py` → trains in-distribution
(>65%), fails held-out (<60%); "learned-orientation self-test ... PASS" (~30 s). The MLP variant
and full tables: LEARNED_ORIENTATION_RESULT.md.

**Scope (honest).** Axis lines, n=3, one β; 12 geometries × 16 τ-draws per cell (label noise where
r_g is small); two model classes — the wrap argument generalizes to smooth interpolators, not to
all conceivable learners.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
