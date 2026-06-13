# Derivation attempt (v59): predict the concentration from propagator geometry — FALSIFIED

**The bar (frontier advice, applied):** not another gain, not another symmetry — a derivation that
predicts the scaling, with the constant frozen *before* the measurement it must match.

**The derivation tested.** Connected weight should decay exponentially with the minimal connecting
network: ln|C| ≈ a − ℓ_MST/ξ, with ξ measured independently from the bare propagator; the class ratio
then follows from pure geometry with zero further parameters. (Motivated by the data's own form: the
v57 ln-ratio is linear in L — exponential, not power law.)

**What the measurements returned (L=8, β=4, μ=0.5, n=3):**
1. Independent ξ = 0.91 (τ-averaged |G|, axial, wrap-safe range).
2. Per-config law: MST length is the best of three geometry variables (R²=0.17; closed tour 0.12,
   max external leg 0.01) — but the slope is **half** the prediction (−0.51 vs −1/ξ = −1.10;
   effective decay length ≈ 2ξ, unexplained), and geometry explains only ~17% of ln|C| variance.
3. **Zero-further-parameter prediction vs measurement:** predicted class-median ratios 3×/5×/7× at
   L=4/6/8; measured 16×/62×/30×. Under-prediction by 5–10×. **The single-variable law is falsified
   as the explanation of the concentration.** (Self-test reproduces the falsification at L=6:
   predicted 2×, measured 6×.)
4. Auxiliary honest finding: per-class medians fluctuate strongly across runs (L=8: 30× here vs
   52–82× in v58) — the 1d class is a *mixture* (axis vs diagonal lines) with heavy tails; even
   medians wander with mixture proportions. Future class statistics must stratify by line type.

**Verdict.** Prediction and measurement disagree — the line is not crossed. What survives: the
exponential *form* in L, and MST geometry as a real but **minor** ingredient. The dominant mechanism
of the (universal, robust) weight concentration is **unidentified**. Open (v60): line-class
commensuration with the free spectrum (1d sub-lattice shell effects), edge-count/compactness,
τ-adjacency — and stratify the 1d class by direction type before further claims.

A falsified derivation, issued before measurement, is the record working as intended.

Reproduce: `python3 decay_law.py` (gates: law direction real, R² in range, AND the quantitative
falsification itself; PASS, ~2 min). Frozen engine untouched (194/194).
