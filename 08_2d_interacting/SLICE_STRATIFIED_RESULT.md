# Slice-stratified evaluation: the v54 hierarchy turned into an unbiased estimator (v55)

**The move.** Stratify the site sum by the exact span-dimension label (which slice through the
external the config lives on), enumerate the small heavy strata exactly, Neyman-sample the rest.
Stratification by an exactly-known label is unbiased by construction; only the gain is in question,
so the gain is what was measured — at matched evaluation budget, against exact ground truth where
feasible.

**Measured, n=2 on the 4×4×4 cube** (strata: 1 point / 243 lines / 3852 planes; ground truth from the
proven v53 fold+cache):

| estimator | std (matched ~500–600 evals) | bias vs truth |
|---|---|---|
| plain MC | 5.0–5.3e-03 | −1.3e-03 |
| **stratified** | **7.6e-04 – 1.1e-03** | **−3.9e-04 … +2.5e-05 (≤0.5σ)** |

Variance reduction **22×–44×** across seeds/budgets (self-test reproduces ~43× at seed set 1000+,
threshold gate >3×). A detail worth keeping: the Neyman allocation *demanded more samples than the
d≤1 strata contain* — the optimizer itself orders the heavy slices enumerated exactly. The hierarchy
asserting itself.

**Measured, n=3 (the regime with a 3d bulk):** strata 1 / 807 / 53262 / 208074. At budget ~320 with
6 repetitions (exact truth not feasible at this size in Python): variance reduction **2.1×**, means
consistent (|diff| 8e-04 vs plain sem 1.7e-03). Honest scope: few reps (the ratio itself is noisy),
and the heavy d=2 stratum no longer fits the enumeration budget, so it must be sampled — the gain
shrinks exactly as the concentration argument predicts.

**The honest law of it:** the gain is large when the weight concentration is steep *relative to
budget* (heavy strata enumerable: 22–44×), real but modest otherwise (2×). Unbiased in both regimes.
Composable with the orbit fold and subset cache (the strata are unions of orbits; the ground truth
here is computed with them). The physical sign R is untouched — this is a variance/prefactor tool
living on the structure the slices revealed.

Reproduce: `python3 slice_stratified.py` (PASS, ~2 min). Frozen engine untouched (194/194).
