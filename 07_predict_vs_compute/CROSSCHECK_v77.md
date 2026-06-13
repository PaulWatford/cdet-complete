# CROSSCHECK_v77 — the μ-period law: charge-1 fugacity winding

**Claims.** (1) Protocol: coherence-boosted axis lines (L=6/8), orientation sign(⟨C⟩_τ) on a dense
μ-grid (0.1), persistence-filtered flips; r_g dips at flip positions (physical zeros). (2) Friedel
falsified on pre-registered gates: flip spacing R-independent; positions don't collapse on
2k_F(μ)R = mπ (winding ~5× faster); spacing strongly β-dependent. (3) The law: median spacing
1.00/0.70/0.50/0.40 at β=2/4/6/8 vs π/β = 1.57/0.79/0.52/0.39; implied charge q = 1.12/1.05/0.98 →
**Δμ\* = π/(qβ), q→1** — charge-1 fugacity winding, R- and L-independent (β=2 censored: window ≈
period). (4) The channel half-reopens: period-based calibrate-then-predict lifts held-out sign
accuracy from v73's 33–44% to 73–76% across 3 seeds × 3 geometries — at the 75% bar, not robustly
above; residual = offset calibration (half-grid flip error is 8–15% of the period). An initial
79% single-seed claim was downgraded by the seed-robustness sweep before banking. (5) Limits: β≥12
unmeasurable with this estimator (independent extractions disagree 0.40 vs 1.50 — protocol validity
boundary); a level-floor hypothesis's cross-predictions failed or were unmeasurable. (6) New theory
target: derive q=1 from the τ-integrated integrand.

**Reproduce.** `cd 08_2d_interacting && python3 mu_period.py` → β=4 spacing in [0.55,0.95];
half-reopening above the v73 baseline; β-monotonicity; "mu-period self-test ... PASS" (~1 min).
Battery scripts and the seed sweep are documented in MU_PERIOD_RESULT.md.

**Scope (honest).** Axis lines, n=3, engine to/ti shifts; β-window 2–8 (cleanest 4–8); prediction
accuracies carry large per-run variance; offsets remain per-geometry calibrations — the law fixes
the period, not the offset.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
