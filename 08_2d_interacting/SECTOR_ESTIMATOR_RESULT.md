# Folding the sign model into the surrogate (v70): scalable exact-sector machinery, an exact-variance methodology — and a correction to our own v67 claim

> **WRAP CORRECTION (v75):** the "rank≤1 sector" used here (808 at L=4; 3,774 at L=6, via min-image
> rank / direction classes) is the min-image-parallel SUBSET of the true torus-line sector —
> min-image collinearity is ill-defined on even-L tori (lines wrap through the antipode). The
> wrap-safe sector (common cyclic line through the origin): **1,618 configs / 82% at L=4; 16,950 at
> L=6.** All exact sums quoted here remain correct for the subsets as defined. See
> SHELL_FOLD_RESULT.md and shell_fold.true_sector.

**The fold-in, made algorithmic.** The sign findings (v67/v68) become machinery that works at any
lattice size, because of one structural fact: **the coherent (rank≤1) sector is polynomially small
by construction** and directly constructible from direction classes in O(N²) — no enumeration of
the N³ config space. Sizes: 808 of 262,144 at L=4 (0.31%); **3,774 of 10,077,696 at L=6 (0.037%)**.
Per-config rank classification is O(1) and vectorizes: exact strata counts over all 10M L=6 configs
in ~6 s. Estimator: exact sector sum + signed-σ pilot-Neyman over rank2/rank3 — unbiased, principled
error bar, any L. The r_pred sign-survival channel (OOS R²=0.32, implied ξ_s=2.2 vs measured 3.0) is
banked as the surrogate's sign channel; its role is to *identify the enumeration target*, not to
serve as a numerical weight.

**The correction (per protocol, openly).** Exact second moments are computable by the same orbit
fold as exact sums (C is group-invariant) — so every design's variance can be computed **exactly**,
no seeds. At L=4, B=1200: uniform exact std **1.08e-2** (measured across seed sets: 2.75e-3 …
3.0e-2 — both unreliable); v67-design exact std **4.30e-3**. **TRUE gain ≈ 6×. The banked v67
figure of 87–110× was inflated by a lucky-high uniform baseline**; this session's opposite seed set
was lucky-low by 4×. v67's structural facts (77% of the signed total in the sector; the bootstrap
CIs; coherence) are untouched — only the gain factor corrects. Exact noise decomposition: **96% of
uniform's E[C²] is the rank≤1 sector's rarity** (the single all-external config alone: 34%); the
bulk carries 4%. Removing the sector exactly is the whole magnitude-side win; the remaining bulk
noise is sign-driven and magnitude-incompressible (v66's theorem, confirmed exactly).

**New standing rule (bought with this correction):** in heavy-tailed systems, estimator comparisons
must be exact-moment-based wherever exact moments are computable; rep-spread comparisons of
heavy-tailed estimators are not measurements.

**L=6 demonstration (10M-config scale, ~4,600 evals = 0.045%).** Exact sector sum **−5.87e-4 —
negative: the μ=0.5 orientation flip of v68 appearing in exact arithmetic** (L=4 sector: positive;
self-test gates the flip). Total estimate −2.3e-3 ± 4.5e-3: the error bar exceeds the value — the
bulk noise dominates the signed total at L=6. Honest reading: **the machinery scales; the sign
problem scales faster.** Two construction bugs were caught by own gates en route (a 13-direction
family conflated with the full rank-1 sector — 5% vs 77% of truth; and a dropped all-external
config — off-by-one against the exact classification count).

Reproduce: `python3 sector_estimator.py` (gates: sector 808/+0.002949; exact total to 1e-7; exact
gain in [3,12]; L=6 sector 3,774 with sign flip; PASS, ~2 min). Frozen engine untouched (194/194).
