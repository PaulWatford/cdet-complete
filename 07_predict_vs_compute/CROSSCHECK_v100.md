# CROSSCHECK_v100 — the Delta sector: a cross-term, not a background; measured, β-growing, reconciling

**Claims.** (1) `Delta1Frozen` (level 1 kept physical) reproduces the raw physical value at the
physical point (−0.041(79) vs +0.030(108), 0.5σ); Δ(s; β) = Delta1Frozen(s) − FrozenCDet(s)
recovers Δ(s_phys; 36) = +0.334(81) vs the v99-inferred +0.369(109). (2) Δ(0; β) ≈ 0 at both β
(+0.036(29) at 28, −0.009(20) at 36): the hole sector vanishes when level 2 is empty, so the
v99 "second player" is a δ₁×f₂ cross-term, not an independent background — the true object is
the full (f₂, δ₁) polynomial. (3) Matched-s cross-slopes over [0, 0.00376]: d1(28) = +41.8(13.2),
d1(36) = +88.8(21.5) e-9, growing with β at 1.9σ. (4) Direction: c1_eff = c1_frozen + d1 moves
the linear root 0.00183 → 0.00327 toward the physical f₂\* = 0.00376. (5) The 13/7-vs-24/13
closure reduces to the assembled root flow z(β); spec (coefficient grid at β ∈ {36,44,52}) and a
directional prediction (z_assembled > z_pol, the assembled curve is what the pool measures)
registered.

**Reproduce.** `cd 08_2d_interacting && python3 delta_sector.py` (Δ0≈0; Δ real; growth;
direction; live gates; PASS ~25 s).

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
