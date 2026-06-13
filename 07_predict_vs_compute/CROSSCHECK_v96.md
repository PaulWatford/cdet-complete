# CROSSCHECK_v96 — the coefficient program, phase 1: instrument validated, background alive, prediction test inconclusive

**Claims.** (1) FrozenCDet (window occupancies set by hand; far levels physical) reproduces the
v89 background (A(20) = +1.853(75) e-9 vs ~+2) and is faithful at the physical point: the
frozen value at (s_phys, μ_phys), the frozen value at μ_exp = 1.84, and the raw physical value
agree within errors at β=36 (max pairwise tension 0.9σ). (2) The per-config strip identity
fails through far-level antiperiodic images — the concrete creep carrier; typical-config
determinants scale exactly (e^0.1 to 1e-6); the τ-averaged object is honest. (3) The background
is alive: A(β) = 1.853(75)/0.839(102)/0.277(45)/0.167(36) e-9 at β = 20/28/36/44, A(44) at
4.6σ — no background-zero, no midpoint static in the (1,2) window. (4) Effective decay rate
0.10–0.12 with prefactor curvature; the asymptotic 1/7-vs-2/13 band is not reached — 13/7 vs
24/13 unchanged. (5) The naive {A, c̄₁} root prediction is inconclusive (~2.5× below the
physical f₂\*; A's heavy tails + small-s curvature), with the phase-2 spec computed (A to ±5%,
geometric s-grid below 0.002, μ_exp pinned per β).

**Reproduce.** `cd 08_2d_interacting && python3 coefficient_flow.py` (six gates incl. a live
frozen evaluation at β=28; PASS ~40 s).

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
