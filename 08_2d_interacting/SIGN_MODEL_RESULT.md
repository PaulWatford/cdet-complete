# The sign model (v67): the v58 question settled, the sign of the line sector predictable, the ceiling moved

> **CORRECTION (v70):** the gain figure "87–110×" below was inflated by a lucky-high uniform
> baseline; exact second-moment analysis (sector_estimator.py) gives the TRUE gain of this design as
> **≈6× at B=1200**. The structural facts (77% of the signed total in the d≤1 sector; the bootstrap
> CIs; sign coherence) are unaffected. See SECTOR_ESTIMATOR_RESULT.md.
>
> **WRAP CORRECTION (v75):** the "d≤1 sector, 808 configs, 77%" is the min-image-parallel subset of
> the true torus-line sector, which is 1,618 configs carrying 82% (wrap-safe definition; see
> SHELL_FOLD_RESULT.md). The 77% remains a true statement about the smaller subset.

**The knock.** v66 ended at a measured ceiling: magnitude guidance gives no gain on
cancellation-dominated totals because their variance is sign-driven. The open v58 question (is the
sign hierarchy real, once measured trustworthily?) and the surrogate's missing sign channel were the
same door. Knocked.

**Result 1 — the v58-downgraded question, settled with the statistics it demanded.** The right
object is the per-geometry sign survival r_g = |⟨C⟩_τ|/⟨|C|⟩_τ (how much weight escapes a geometry's
own τ-cancellation — v60's 40%-of-variance channel). Bootstrap-bounded, survey sample sizes:

| class | median r_g | 90% CI | sign(+) fraction |
|---|---|---|---|
| 1d lines | 0.70 | [0.59, 0.81] | **92%** |
| 2d planes | 0.70 | [0.58, 0.82] | 70% |
| 3d bulk | 0.34 | [0.25, 0.47] | 45% |

**Non-overlapping CIs** between low-dim and bulk: the sign hierarchy is real at the τ-integrated
per-geometry level. (The v58 downgrade targeted unstable per-*sample* R estimators; this is the
stable object.) And the **sign itself is predictable for lines** — 92% positive vs a bulk coin flip.
r_g correlates with span-dim (−0.45) and MST (−0.50): a sign-survival model is fittable.

**Result 2 — the structural fact.** The d≤1 sector — **808 of 262,144 configs, 0.3% of the space —
carries +0.002949 of the +0.003846 exact signed total: 77% of the entire answer.** Sign coherence
concentrates the *signed* sum even harder than magnitude concentrates the unsigned one; the bulk's
208,074 configs mostly cancel into a small remainder.

**Result 3 — the ceiling moved.** Hybrid estimator (enumerate the sign-coherent d≤1 sector exactly,
pilot-Neyman the rest with signed-σ pilots) at budget ~1200 (0.46% of configs) against the exact
truth: **87–110× variance reduction over uniform** (survey/self-test seeds), bias ≤1σ — where v66's
magnitude-only guidance gave 0.7×. v55's 2.1× was this design starved of the budget to enumerate the
line sector; the v67 measurements are what justify spending it there.

**Flagged, not banked:** a magnitude-bin arm in the survey printed "231×" but ran on a frozen 20k
subsample whose selection variance is absent from its std — rejected as a claim.

**Bonus methodology catch:** the first self-test failed because trimmed sample sizes broke the
bootstrap CI separation — the v58 lesson applied to our own gate design; restored to survey sizes.

**Honest scope.** One lattice/order/μ/β. The 92% line-sign predictability is measured, not derived —
re-measure before reuse elsewhere. The bulk remainder is still a coin flip: the wall stands there,
its territory now mapped to 0.3% precision.

Reproduce: `python3 sign_model.py` (gates: CI(1d) above CI(bulk); 1d sign(+) >75%; hybrid gain >10×
and unbiased <3σ vs the exact truth; PASS, ~2 min). Frozen engine untouched (194/194).
