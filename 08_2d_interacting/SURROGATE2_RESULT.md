# Surrogate refinements (v74): ceilings first, the R²-mixture artifact corrected, a transferable magnitude model, and the r_pred regime map

**1. Measure the ceiling before chasing R² (new standing practice).** Split-half label reliability:
ln⟨|C|⟩_τ has ρ=0.95 at NT=20 — real headroom existed above the old 0.75. ln r_g has ρ=0.40 at
NT=20 (≈0.57 at NT=40): **the "weak" r_pred R²=0.32 was ~80% of what its labels permitted** —
mostly label noise, not model failure. An honest reframe banked before any fitting.

**2. The R²-mixture artifact (scope correction of our own reporting).** v66's "OOS R²=0.75" was
test-composition-flattered: a line-heavy test set has enormous between-class spread that any
line/bulk separator converts into high R². On a standardized bulk-heavy split the same model scores
0.55. The number was real; its interpretation was mixture-dependent. Standing protocol now:
fixed-split comparisons with **median per-config error as co-headline** (1.7×, mixture-independent,
unchanged). Clarification note added to SURROGATE_RESULT.md.

**3. The transferable magnitude model (the real gain).** Ten features, linear ridge with proper CV,
apples-to-apples on one split: in-distribution a wash (0.55 → 0.59), but **transfer L=4 → L=6
(slopes frozen, intercept from 8 L=6 geometries): R² 0.33 → 0.57, median error 2.88× → 1.81×.** The
new features (dmax, anisotropy, lattice adjacency, dmin) carry across lattice size; the old three
don't. Quadratic interactions destroy transfer (extrapolation blowup) — linear is the model. Two
pipeline bugs caught en route (a garbled CV formula that silently broke λ selection; the quadratic
transfer catastrophe).

**4. The r_pred regime map (the channel's true shape).** Within-class OOS R² at NT=40:
**rank-1 +0.32, rank-2 +0.27, rank-3 −0.57.** Sign-survival predictability lives *exactly where
coherence lives* — graded and learnable inside the coherent and near-coherent sectors (the ξ_s
decay), strictly unpredictable (worse than the mean) in the deep bulk. The v73 orientation-channel
closure, now visible quantitatively in the survival channel. Earlier overall-R² figures were
mixture-dependent blends of these regimes.

**Honest scope.** L=4 calibration + L=6 transfer; one β/μ for the regime map; the 8-shot intercept
is a stated requirement; in-distribution magnitude (0.59 vs ceiling 0.95) still leaves real
geometry signal uncaptured — plausibly the τ-structure family the phase belongs to.

Reproduce: `python3 surrogate2.py` (gates: v2 transfer beats v1 by ≥0.10 and ≥0.45; PASS, ~1 min;
ceilings and regime map reproduce from /tmp survey scripts documented here). Frozen engine
untouched (194/194).
