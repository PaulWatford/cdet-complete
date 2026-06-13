# The L=6 shell fold (v75): first exact totals at 10M-config scale, the rings at L=6 — and the wrap-collinearity correction

**The wrap discovery (correction banked; the wrap-safe rule now extends to definitions).**
Min-image collinearity is ill-defined on even-L tori: the line through (5,1,0) at L=6 wraps through
the antipode, where the min-image convention flips signs — {0,(5,1,0),(3,3,0)} *is* collinear
((3,3,0)=3×(5,1,0) mod 6) yet its min-image rows aren't parallel. The per-config min-image rank is
therefore not orbit-consistent, and **the v67/v70 "rank≤1 sector" was the min-image-parallel subset
of the true torus-line sector.** Wrap-safe definition: common cyclic line through the origin
(generator-mask test; manifestly group-invariant). Corrected: **L=4 sector = 1,618 configs carrying
82%** (was 808/77%); **L=6 sector = 16,950 (0.17%)** (was 3,774). The old numbers were true
statements about a smaller subset; notes added to the v67/v70 docs.

**The fold.** 240,464 orbit reps of 10,077,696 configs, evaluated at both fillings (~25 min):

| | μ=0.5 | μ=1.5 |
|---|---|---|
| **exact total** | **−2.498377e-3** | **−2.224768e-3** |
| true sector | −1.055844e-3 (42%) | +4.842304e-4 (**−22%**: opposes the total) |

The v70 pilot (−2.3e-3 ± 4.5e-3) is **validated dead-on**. The μ=0.5 total is negative — the phase
flip vs L=4 (+0.00385) holds for the *full total*. And the size trend is stark: the sector carries
82% at L=4 but only 42% at L=6, and can even oppose the total — **the remainder grows in relative
importance with size: the sign problem scaling faster than the machinery, now in exact arithmetic.**

**The rings at L=6.** Oscillation persists (2 sign changes per filling at unit bins; patterns
[−−+−−−] at μ=0.5, [−+−−−−] at μ=1.5), and half-unit bins give **μ-dependent node positions**
(μ=0.5: ~3.0, 4.5, 5.5…; μ=1.5: ~3.5, 4.0, 5.0…). **Honest verdict on the period:** spacings are
irregular (0.5–1.5) — the right *scale* relative to the frozen π/k_F ≈ 1.1–1.2, but the period is
**not resolved** at this size/binning. The μ-period theory item stays open with new constraints;
named refinement: MST is a crude radial coordinate for a 3-body object (per-leg extent was cleaner
in v68).

Reproduce: `python3 shell_fold.py` (cheap gates: sector counts 1,618/16,950; L=4 sector sum
+0.003165; group-invariance over sampled orbits; stored-table arithmetic both fillings; PASS,
~1 min). The full fold reproduces from the staged pipeline documented here (~25 min of evaluation).
Frozen engine untouched (194/194).
