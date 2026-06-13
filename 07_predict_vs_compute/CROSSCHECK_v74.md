# CROSSCHECK_v74 — surrogate refinements: ceilings, mixture-honest protocol, transfer, regime map

**Claims.** (1) Noise ceilings by split-half reliability: ln⟨|C|⟩_τ ρ=0.95 (NT=20); ln r_g ρ=0.40
(NT=20) / ≈0.57 (NT=40) — the prior r_pred 0.32 was ~80% of its ceiling. (2) Scope correction:
v66's "OOS R²=0.75" was mixture-flattered (line-heavy test spread); same model 0.55 on a
standardized bulk-heavy split; the mixture-independent median per-config error (≈1.7×) stands;
note added atop SURROGATE_RESULT.md. (3) Transferable magnitude model: 10 linear features;
in-distribution a wash; L=4→L=6 transfer R² 0.33→0.57 and median error 2.88×→1.81× with an 8-shot
intercept; quadratic interactions destroy transfer; two pipeline bugs caught (garbled CV; quadratic
extrapolation). (4) r_pred regime map (NT=40, within-class OOS R²): rank-1 +0.32, rank-2 +0.27,
rank-3 −0.57 — predictability coextensive with coherence; the deep bulk strictly unpredictable.

**Reproduce.** `cd 08_2d_interacting && python3 surrogate2.py` → v1/v2 transfer comparison with
gates (Δ≥0.10; v2≥0.45); "surrogate-v2 self-test ... PASS" (~1 min). Ceiling and regime-map survey
scripts are documented in SURROGATE2_RESULT.md (seeds 120/130/131/140).

**Scope (honest).** L=4 calibration, L=6 transfer; one β/μ for the regime map; 8-shot intercept is
part of the transfer protocol, stated; in-distribution magnitude 0.59 vs ceiling 0.95 — real signal
remains uncaptured, plausibly the τ-structure family of the phase.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
