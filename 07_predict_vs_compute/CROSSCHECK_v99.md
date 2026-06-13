# CROSSCHECK_v99 — phase 2: the IS estimator, the frozen polynomial, the two-sector discovery

**Claims.** (1) The plain τ-estimator at the frozen point has infinite variance (tail index
α ≈ 0.55; top 1% of samples carry 95.5% of the mass at clustered times; a 24-draw brute mean
swung −0.178 → +0.023 on late spikes). The mixture importance sampler (weights ≤ 2, mean 1)
is validated analytically (0.5σ over 300k) and gives ~31× variance reduction. (2) The frozen
polynomial at β=36, μ_exp=1.845: A = +0.3700(108) [supersedes v96's tail-biased +0.277(45)],
grid measured to 3–7%, root s\* = 0.00183(8) → z_pol = 1.8249(12), internally smooth
(frozen(s_phys) = −0.3391(143) sits on it). (3) The registered root-flow branch is excluded at
~10σ (slope ≈ −200 e-9 persists to s = 0.0005). (4) The two-sector discovery: v96 faithfulness
is falsified at 3.4σ (physical(1.845) = +0.030(108) vs frozen-at-the-physical-point
−0.3391(143)); the freeze kills the δ₁ antiperiodic images (O(1) in the τ→β corner), which
form the hole-image sector Δ(s_phys; 36) = +0.369(109) e-9; the physical zero is the root of
[frozen polynomial + Δ]. (5) Consequences: literal-rate menu bookkeeping suspect for hole
monomials (τ-integrated re-derivation queued); v96 #106 downgraded in-module; the decisive
13/7-vs-24/13 object is now Δ(s; β); the FROZEN_CURVE_Z8 prediction carries the one-sector
caveat.

**Reproduce.** `cd 08_2d_interacting && python3 coefficient_phase2.py` (weights; analytic;
root; two-sector; live IS gates; PASS ~80 s). Revised modules still pass: coefficient_flow.py,
exponent_balance.py.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
