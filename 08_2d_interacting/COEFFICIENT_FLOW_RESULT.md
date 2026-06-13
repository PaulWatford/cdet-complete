# The coefficient program, phase 1 (v96): the freeze instrument, the background alive, the prediction test honestly inconclusive

**The instrument.** `FrozenCDet` — FastCDet with window-level occupancies set by hand (levels ≤1
→ 1, level 2 → free s, level 3 → 0, far levels physical) — is built, validated against v89
(A(20) = +1.853(75) e-9 vs the ~+2 extrapolation), and proven **faithful**: at the physical
point (s = 0.003758, μ = 1.8450, β = 36) the frozen value, the frozen value at μ_exp = 1.84,
and the raw physical value agree within errors, all consistent with the physical zero. The
per-config strip identity fails through far-level antiperiodic images — the creep carrier
identified concretely (the determinants on typical configs scale exactly; the τ-averaged object
is the honest one).

**The background is alive.** A(β) = 1.853(75), 0.839(102), 0.277(45), 0.167(36) e-9 at
β = 20/28/36/44 — **A(44) > 0 at 4.6σ**: the (1,2) window carries no background-zero, hence no
midpoint static (consistent with no flip at 3/2 and the exponent-balance picture). The decay's
effective rate is ~0.10–0.12 with visible prefactor curvature (pair rates 0.099(16), 0.139(25),
0.063(34)) — the asymptotic rate, which in the root-flow picture equals 2−z∞ (1/7 for 13/7,
2/13 for 24/13), is **not yet reached or resolved**. The 13/7-vs-24/13 status is unchanged.

**The prediction test, honestly.** The naive {A, c̄₁} root lands ~2.5× below the physical f₂\*
— inconclusive, not failed: faithfulness passes, and the gap sits in A's heavy-tailed
estimation (two batches at 2σ tension) plus small-s curvature under the grid's resolution.
Phase-2 spec, computed: A to ±5% (~500 draws × 2048 per β), a geometric s-grid below 0.002, and
μ_exp pinned per β — then the polynomial root is a parameter-free prediction of the zero.

Reproduce: `python3 coefficient_flow.py` (six gates incl. a live frozen evaluation; PASS ~40 s).
Frozen engine untouched (194/194).
