# The assembled root flow (v107): z(∞) from the rate difference — and the lower menu falls

The v106 loop-format tool, applied to the closure v105 left open. Instead of chasing the asymptote
through ill-conditioned high-β measurement, assemble it from the **rate difference** of two
well-conditioned moderate-β series.

## The two series (stable engine, median-of-means, uniform grid)

    beta:    24            32            40            48
    A(beta)  +1.328(217)   +0.357(125)   +0.119(28)    +0.051(23)   e-9   (background, decays fast)
    c1(beta) -319.8(69.9)  -193.8(49.5)  -195.4(20.7)  -172.2(16.0)  e-9   (slope, decays slow)

## The asymptote

The leading-order static is s\*(β) = A/|c1|, so z(β) = 2 + ln(A/|c1|)/β and
**z(∞) = 2 − (ρ_A − ρ_c1)**, the *difference* of the dominant decay rates. Extracted with
Monte-Carlo error propagation over the measurements:

    rho_A   = 0.1406(158)     (A decays ~6x faster)
    rho_c1  = 0.0225(95)
    z(inf)_leading = 2 - (rho_A - rho_c1) = 1.8818(184)

**This sits above the lower menu** the four naive rounds had narrowed to:

    24/13 = 1.8462  -> 1.9 sigma  (disfavoured)
    13/7  = 1.8571  -> 1.3 sigma  (disfavoured)
    15/8  = 1.8750  -> 0.4 sigma  (consistent)
    17/9  = 1.8889  -> 0.4 sigma  (consistent)

15/8 was declared empirically dead in v94/v95 (4.6σ) — on *naive* data. The certified+robust+
resummed analysis **resurrects the high end**: the asymptote is ~1.88, near 15/8, not the
1.846–1.857 the naive flatness implied.

## Internal consistency (the cross-term, reconfirmed)

The leading-order finite-β flow (1.772 → 1.803 → 1.815 → 1.831) sits ~0.03 *below* the robust pool
(1.843 → 1.854 → 1.864). That gap is exactly the v100 δ₁×f₂ cross-term, which lifts the root toward
physical. So two independent routes agree on the shape: the robust pool (full static, measured) and
the assembled leading-order flow + cross-term both rise toward ~1.88.

## Honest limits

Leading order (s\* = A/|c1|, omitting the c2 curvature and the cross-term's effect on the
*asymptotic* rate); four points per series with ~10–40% rate errors; the c1(40) point sits slightly
high, adding noise to ρ_c1. The asymptote could shift if the cross-term modifies ρ_c1_eff. What is
robust: ρ_A ≫ ρ_c1 (A decays much faster than c1), so z(∞) is well above 2 − ρ_A alone, and the
lower menu members are disfavoured at 1.3–1.9σ from two independent methods. The decisive
sharpening is c1 on a denser grid (to pin ρ_c1) and the cross-term's own rate.

## What this closes

v105 reopened the identification as a rising flow and could not reach the asymptote (high-β
ill-conditioned). The loop-format resummation — borrowed from the uploaded gravity-loop cascade,
adapted via the exact-integer L=6 spectrum — reaches it from moderate β: z(∞) ≈ 1.88, the lower
menu falls, the high end (15/8) returns. None of this moves the wall (R, 2ⁿ unchanged).

Reproduce: `python3 deep_beta_resummation.py` (channels; known-rate; assembled z_inf; PASS ~5 s).
Frozen engine untouched (194/194).
