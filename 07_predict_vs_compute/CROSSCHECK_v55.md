# CROSSCHECK_v55 — slice-stratified evaluation (unbiased; 22–44× where concentration beats budget)

**Claim.** Stratifying the cube site sum by the exact span-dimension label (enumerate heavy small
strata, Neyman-sample the rest) is unbiased and cuts variance at matched evaluation budget:
n=2 (strata 1/243/3852, exact fold+cache ground truth −0.010690): plain MC std ~5.0e-03 →
stratified 7.6e-04–1.1e-03 = 22–44× variance reduction across seeds, stratified bias ≤0.5σ
(−3.9e-04 … +2.5e-05). Neyman allocation exceeded the d≤1 stratum sizes, i.e. the optimal design
enumerates the heavy slices exactly. n=3 (strata 1/807/53262/208074; heavy stratum unenumerable at
budget ~320; 6 reps): 2.1× variance reduction, means consistent (|diff| 8e-04 vs plain sem 1.7e-03).

**Reproduce.** `cd 08_2d_interacting && python3 slice_stratified.py` → strata sizes, exact truth via
the proven v53 fold+cache, both estimator stds, gain, bias; gate `gain > 3x` and `|bias| < 3σ`;
prints "slice-stratified self-test: PASS" (~2 min).

**Scope (honest).** Gain tracks weight concentration relative to budget: large when heavy strata are
enumerable, modest (2×) when they must be sampled; unbiased in both regimes; the n=3 ratio is from
few repetitions. Sign R untouched — a variance tool on the slice structure.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875). Wraps the engine via validated `cdet_port.py` (0.00e+00).
