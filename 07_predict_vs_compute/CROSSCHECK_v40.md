# Cross-check (v40) — is single-order R the right observable? Testing aggregate candidates

Reproduce: 08_2d_interacting (make robust). Follows v39 (per-order R is shell-contaminated).

## What was checked (fixed density n=0.80, beta=4)
- INTEGRATED average sign S over orders (the cost-controlling quantity for G(U)): L=2 +0.056, L=3 -0.118,
  L=4 +0.021 -- sign-alternating, NOT cleaner than per-order R. Mechanism: order weights
  U^n N(N beta)^n/n! are non-uniform, so the sum is dominated by ONE order (U=0.5->order1, U=2->order4)
  and inherits its shell structure.
- CROSSOVER order n* and per-order R_n: R_n non-monotonic in n; n* jumps with cluster (L=2 n*=4; L=3,4
  none in range). Inherits the per-order a_n shell jumps.
- R(mu) on 4x4 oscillates and changes sign across mu=-3..3, non-smooth even between shell levels.
- Free-energy differences: a different (thermodynamic-integration) computation, not tested.

## Verdict
None of the measurable aggregate observables scales cleanly at accessible sizes. Integrating over orders
cannot help (single-order domination); n*/R_n inherit shell jumps; R(mu) is filling-sensitive within one
cluster. The contaminant is partial-shell FILLING at small N; the principled cure is fixing the filling
fraction (closed-shell families) or large N -- both out of reach with the current toolkit. The honest
status from v39 stands, now stress-tested: no clean sign-scaling benchmark exists at accessible sizes.

## Scope
Small clusters (N<=16-25), orders <=5, density 0.80, single external-time choice. A negative, mechanistic
result: the obstruction is small-cluster shell structure shared by all these observables, not a poor choice
among them. No claim about free-energy estimators or about large-N asymptotics.
