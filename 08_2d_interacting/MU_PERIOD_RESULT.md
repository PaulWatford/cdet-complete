# The μ-period law (v77): charge-1 fugacity winding — Friedel falsified, the wrap solved, the offset now the bottleneck

**The protocol** (the route v76 named: coherence-boosted lines): controlled axis-line geometries at
L=6/8, orientation sign(⟨C⟩_τ) on a *dense* μ-grid (step 0.1, μ∈[0,3]) — dense sampling reads the
wrap off directly instead of interpolating across it (the v73 trap). Flips = persistent block
boundaries; **r_g dips at flip positions** — the flips are physical zeros.

**Friedel falsified for the μ-dependence** (pre-registered gates): flip spacing is
**R-independent** (G1 fail — Friedel predicts rate ∝ extent); flip positions don't collapse on
2k_F(μ)R = mπ (G2 fail — winding ~5× faster than free-k_F accumulation); spacing is strongly
β-dependent (Friedel predicts β-flat).

**The thermal law (the discovery).** Median flip spacing across the battery:

| β | 2 | 4 | 6 | 8 |
|---|---|---|---|---|
| measured | 1.00 | 0.70 | 0.50 | 0.40 |
| π/β | 1.57 | 0.79 | 0.52 | 0.39 |
| implied q | (censored) | 1.12 | 1.05 | 0.98 |

**Δμ\* = π/(qβ), q → 1: charge-1 fugacity winding** — R-independent, L-independent (L=6 at β=4 also
gives 0.70). The phase that resisted every geometric reduction has a form, and it lives in (μ,β):
dφ/dμ ≈ β, as if the τ-integrated 3-vertex coefficient carries the e^{iβμ} rotation of a single
particle-hole unit. *Deriving q=1 joins the theory queue.*

**The channel, half-reopened.** Calibrate flips at μ<1.5, continue the alternation at the period,
predict held-out signs: across 3 seeds × 3 geometries, 73–76% mean (one-period horizon) with large
per-run variance (0–100%) — **at** the 75% bar every previous attempt failed, not robustly above
it. v73's failure mode (anti-prediction from wrap-blind interpolation: 33–44%) is *cured* by the
period; the residual is **offset calibration** — a half-grid flip error is 8–15% of the 0.65 period
and compounds with horizon. Law-finding is done here; what remains is calibration-precision
engineering.

> **READING REFINED (v78):** the "charge-1 fugacity winding" reading is superseded by the analytic
> mechanism: ⟨C⟩_τ is exactly rational in z=e^{βμ} (cancellation lemma) with poles on Matsubara
> combs at height π/β anchored at the levels — detected directly by complex-μ continuation. The
> 1/β scaling and R/L-independence are comb geometry; "charge 1" is the z-degree of each Fermi
> denominator; π is the antiperiodicity phase. The literal charge-staircase picture was falsified
> by the ln|C| slope test. See FUGACITY_STRUCTURE_RESULT.md.

> **BOUNDARY RETRACTED (v80):** the "β≥12 unmeasurable" statement below is superseded — the
> disagreeing extractions were intra- vs inter-cluster spacings of the RESONANCE REGIME (flips
> level-attracted, p=0.025, and geometry-independent, p=0.03–0.04 at β=16). The protocol boundary
> was the second regime announcing itself. See RESONANCE_REGIME_RESULT.md.

**Limits (honest).** β≥12 is unmeasurable with this estimator (independent extractions disagree:
0.40 vs 1.50) — banked as the protocol's validity boundary; a level-spacing-floor hypothesis was
raised and its cross-predictions failed or were unmeasurable — recorded as falsified-or-undecidable.
β=2 is censored (window ≈ period). Axis lines, n=3, engine to/ti shifts throughout.

Reproduce: `python3 mu_period.py` (gates: β=4 spacing in [0.55,0.95]; half-reopening > the v73
baseline and ≥55%; β-monotonicity; PASS, ~1 min). Frozen engine untouched (194/194).
