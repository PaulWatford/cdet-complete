# The Delta sector (v100): the v99 "second player" is a cross-term, not a background — measured, growing with β, reconciling

**The instrument.** `Delta1Frozen` keeps level 1 physical (antiperiodic images alive) while
freezing level 2 → s, level 3 → 0. At (s_phys, μ) it keeps every window level physical, so it
must equal the raw physical value — gate passed (−0.041(79) vs +0.030(108), 0.5σ). The sector
is isolated by subtraction: Δ(s; β) = Delta1Frozen(s) − FrozenCDet(s), recovering
Δ(s_phys; 36) = +0.334(81), consistent with the v99-inferred +0.369(109).

**The structural discovery.** Δ(0; β) ≈ 0 at both β (+0.036(29) at 28, −0.009(20) at 36): when
level 2 is empty the hole-image sector **vanishes**. So Δ is not an independent background added
to the frozen polynomial (the literal v99 framing) — it is a **δ₁×f₂ cross-term**, the
coefficient the single-level freeze structurally omits. The correct object at the zero is the
full (f₂, δ₁) polynomial; the v99 freeze captured only its f₂-diagonal.

**The cross-slope, measured.** Matched-s secants over the identical interval [0, 0.00376]
(legitimate since Δ(0)≈0): d1(28) = +41.8(13.2), d1(36) = +88.8(21.5) e-9 — the cross-coupling
**grows with β** (~2.1× over Δβ=8, 1.9σ). Direction check: at β=36 the frozen slope c1 ≈ −202
becomes c1_eff ≈ −113, moving the linear root from the frozen 0.00183 to ~0.00327 — toward the
physical f₂\* = 0.00376 (the residual is s² curvature, consistent with v99's smooth grid). The
two-sector picture is confirmed and corrected: one polynomial, one β-growing cross-coefficient.

**The open (registered, with spec).** The 13/7-vs-24/13 identification is now the β-flow of the
assembled root z(β) = 2 − ln(s\*(β))/β with s\*(β) the root of A(β) + c1_eff(β)s + c2(β)s² —
needing A, c1_frozen, d1, c2 on a common β-grid (only β=36 complete; d1 at 28, 36). Spec: the
full coefficient grid at β ∈ {36, 44, 52} to ±5% (IS, ~50 s/point), then assemble z(β) and test
against the empirical pool's deep points (48, 52, 56) as a frozen prediction. **Prediction
registered (directional):** the cross-term keeps s\* above the frozen root at all β, so
z_assembled(β) > z_pol(β), and the assembled curve — not the one-sector frozen root — is what
the pool measures.

Reproduce: `python3 delta_sector.py` (Δ0≈0; Δ real; growth; direction; live gates; PASS ~25 s).
Frozen engine untouched (194/194).
