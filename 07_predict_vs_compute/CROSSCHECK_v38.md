# Cross-check (v38) — Can CDet buy extra useful orders before the wall hits?

Measured on the engine's actual Wick matrices (D_corr's (n+1)x(n+1) det). Reproduce: 08_2d_interacting (make buy-orders).

## What was measured
- COST: the determinant evaluates order n in O((n+1)^3); naive Wick-contraction enumeration is (n+1)!.
  Crossover ~order 5; naive/det = 79 (n=7), 3.6e3 (n=9), 5.1e9 (n=15). Past ~order 5 the determinant is
  the only way to evaluate the order at all.
- PER-ORDER VARIANCE: a contraction-sampler suffers cancellation perm(|M|)/|det(M)| (geo-mean over
  configs). 2x2: 1.51,2.19,3.11,4.46,6.44,9.45,14.89 for n=1..7; 4x4: 1.06..1.88. Grows with ORDER on
  every cluster; the determinant removes it exactly (no contraction sampling).
- WHAT IT DOES NOT BUY: at FIXED order n=3, perm/|det| SHRINKS with cluster size (3.11->1.24->1.23 for
  N=4,9,16) -- opposite to the v37 sign wall (R collapses, cost ~1/R^2 GROWS with N and beta at fixed
  order). Two different walls: within-config Wick cancellation (per-ORDER, removed by det) vs
  configuration-level cancellation (per-SYSTEM-size/temperature, untouched by det).

## Answer
YES for the ORDER axis: CDet makes high orders both evaluable (n^3 vs (n+1)!) and lower-variance per
evaluation (removes perm/|det|), reaching order ~10-15 where naive enumeration is impossible. NO for the
size/temperature wall: that configuration-level sign problem (v37) is a different wall the determinant
does not address. CDet climbs the order axis cheaply; the size/temperature axes -- where 2D Hubbard
physics lives -- stay blocked at fixed order and need different medicine (analytic-mean control variate,
importance sampling, or a better estimator).

## Honest scope
This compares the determinant against a contraction-sampling strawman via perm/|det| and the (n+1)! vs
n^3 cost -- the standard, faithful way to see the determinant's advantage on the engine's own matrices.
It is NOT a re-implementation of historical per-diagram DiagMC, and makes no claim about absolute
wall-clock vs a specific competing code; it isolates the mechanism and its order-vs-size dependence.
