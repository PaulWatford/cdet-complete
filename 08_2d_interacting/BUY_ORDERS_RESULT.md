# Can CDet buy extra useful orders before the wall hits? (v38)

Short answer, from measurements on the engine's actual Wick matrices: YES for the ORDER axis -- decisively
-- and NO for the system-size / temperature wall, which is a different wall the determinant does not touch.

## What the determinant actually does
At order n the engine evaluates det(M) of the (n+1)x(n+1) propagator matrix M[i,j]=G0(row_i,col_j)
(D_corr; row/col 0 are the external legs). det(M) = sum over (n+1)! signed Wick contractions, computed
EXACTLY by LU in O((n+1)^3). The connected recursion C_V then combines subset determinants. So the unit of
work is a determinant -- a quantity a naive method would instead build by summing/sampling (n+1)! signed
contraction terms. The question is what the determinant buys over that.

## Pillar 1 -- COST (the decisive one): O((n+1)^3) vs (n+1)!
   n     (n+1)! ops        cube ops     naive/det
   3            24              64        0.4
   5           720             216        3.3
   7         40320             512       79
   9       3628800            1000     3.6e3
  12    6227020800            2197     2.8e6
  15  20922789888000          4096     5.1e9
Past order ~5 the determinant is not just faster -- it is the only way to evaluate the order at all.
This is the primary mechanism by which CDet "buys orders": it makes high orders reachable.

## Pillar 2 -- PER-ORDER VARIANCE: the determinant removes perm(|M|)/|det(M)|
A method that sampled the (n+1)! contractions stochastically suffers a sign problem of severity
perm(|M|)/|det(M)| (sum of |terms| over |signed sum|). Geometric mean over sampled configs (beta=4):
  order:        1     2     3     4     5     6     7
  2x2 (N=4):  1.51  2.19  3.11  4.46  6.44  9.45 14.89
  4x4 (N=16): 1.06  1.14  1.23  1.34  1.48  1.65  1.88
It grows with ORDER on every cluster (universal; base depends on lattice density). The determinant
computes det exactly with no contraction sampling, so it removes this variance entirely. CDet's high
orders are therefore not only evaluable but lower-variance per evaluation than a naive sampler's.

## Pillar 3 -- what it does NOT buy: this is an ORDER effect, not size/temperature
perm(|M|)/|det(M)| at FIXED order n=3, vs cluster size: N=4 -> 3.11, N=9 -> 1.24, N=16 -> 1.23.
It SHRINKS with cluster size -- the exact opposite of the v37 sign wall, where the configuration-level
cancellation ratio R collapses and the cost (~1/R^2) GROWS geometrically with cluster size and inverse
temperature at fixed order (2x2->4x4 ~260x; beta 2->8 on 3x3 ~570x). These are two different walls:
- WICK-contraction cancellation: within a configuration, grows with ORDER -> removed by the determinant.
- CONFIGURATION-level cancellation: across the MC integral's sampled configs, grows with SYSTEM SIZE and
  inverse TEMPERATURE -> NOT touched by the determinant.

## Conclusion (honest)
CDet buys the ORDER axis cheaply: high orders that are impossible to enumerate naively (n^3 vs (n+1)!)
and that a contraction-sampler couldn't resolve (perm/|det| variance) are evaluated exactly and reached.
But extra orders only help if the perturbation series is useful in your regime, and the path to the
interesting physics -- larger clusters, lower temperature -- is blocked by the configuration-level sign
wall (v37) at FIXED order, which the determinant does not address. So: CDet climbs the order axis; the
size and temperature axes, where 2D Hubbard physics lives, need different medicine (a real analytic-mean
control variate, importance sampling, or a better estimator). Reproduce: make buy-orders.
