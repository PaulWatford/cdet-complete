# The no-brute-force simulator (v66): zero-evaluation structure prediction, guided estimation, and the wall in estimator form

> **SCOPE CLARIFICATION (v74):** the headline "OOS R² = 0.75" is mixture-dependent — it reflects a
> line-heavy test set whose between-class spread inflates R²; on a standardized bulk-heavy split the
> same model scores 0.55. The mixture-independent quality metric, median per-config error ≈ 1.7×,
> is unchanged. See SURROGATE2_RESULT.md for the standardized protocol and the transferable v2 model.

**The ask:** push prediction/simulation as close to brute-force results as possible without brute
force. **The honest shape of the answer:** the laws predict the *magnitude geography* — where weight
lives — but not the sign of each term; so the ceiling is set by how cancellation-dominated the target
is. We pushed to that ceiling and measured it.

**The surrogate.** ln⟨|C|⟩_τ ≈ a − b·MST + c·ℓ_coll + d·span_dim, calibrated on ~85 τ-averaged
geometries (the *only* true evaluations used). **Out-of-sample R² = 0.75–0.76**, median per-config
error 1.7× (train/test split; the mixed bulk+line ensemble breaks the v63 multicollinearity in
practice).

**Result 1 — zero-evaluation reproduction of brute-force structure.** The v54 brute-force
weight-share table, predicted with no C_V calls at all:

| span dim | predicted | measured (v54 brute) | concentration pred / meas |
|---|---|---|---|
| 1 | 4.8–4.9% | 5.6% | 14.5× / 18.5× |
| 2 | 47.4–48.4% | 43.0% | 2.40× / 2.09× |
| 3 | 46.7–47.8% | 51.5% | 0.59× / 0.65× |

Every class within ~5 points; concentrations within ~30%.

**Result 2 — guided estimation where the sign is mild.** n=2 cube vs exact fold+cache truth, budget
400 of 4096: stratifying by *predicted* weight gives **33× variance reduction** over uniform MC in
the survey run (5× at the self-test seeds — heavy-tail seed spread, gate >5×), bias ≤1σ — tying the
hand-built v55 stratification while generalizing to any lattice/order without redesign. Defensive
importance sampling (surrogate proposal + 30% uniform guard): 12× — weaker; sign flips inside heavy
strata hurt C/p; stratified mode is the recommendation.

**Result 3 — the honest boundary, measured.** n=3 cube, against the exact 262,144-config truth —
itself a flagship of the consolidated stack: **computed in 11 s, 24,958 determinants vs 4.2M brute
(168× fewer)**. Guided estimation at 0.23% budget: **no gain (0.7×)**. Mechanism: the n=3 total is
cancellation-dominated, so estimator variance is *sign-driven*, not magnitude-driven — and a
magnitude predictor cannot guide what it cannot see. This is the sign wall expressed as an estimator
theorem, measured rather than asserted.

**One line:** without brute force we now reproduce the brute-force weight geography well enough to
design measurements, and reproduce signed totals cheaply wherever the sign is mild — and we can say
precisely where and why that stops.

Reproduce: `python3 surrogate.py` (gates: R²>0.5; zero-eval table within ±12 points/class; guided
gain >5× and unbiased <3σ; PASS, ~2 min). Frozen engine untouched (194/194).
