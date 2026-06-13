# Is single-order R the right observable at all? Testing the aggregate candidates (v40)

v39 found the per-order sign-cancellation ratio R is contaminated by finite-size shell structure, so the
sharper question is whether a more aggregate observable scales cleanly instead. The proposed candidates:
average sign integrated over orders, sign at fixed density and filling, free-energy differences, effective
variance growth rates, crossover order n*. We tested the ones measurable with this engine's Green's-
function MC. Honest finding: at accessible cluster sizes, none scales cleanly -- and there is a clear
mechanism for why integrating over orders cannot help.

## (A) Average sign integrated over orders -- NOT cleaner
The integrated sign S = sum(w)/sum(|w|) with w = U^n N(N beta)^n/n! C_V (the quantity that actually controls
the cost of computing G(U)), at fixed density n=0.80, U=1, nmax=5:
  L=2: S=+0.056   L=3: S=-0.118   L=4: S=+0.021   -- still sign-alternating and non-monotonic.
WHY (the key point): the per-order weights U^n N(N beta)^n/n! are wildly non-uniform, so the "integral over
orders" is dominated by a SINGLE order and just inherits that order's shell structure. Exact 2x2 weights:
  U=0.5: [0.29,0.12,0.02,0.03,0.01] -> order 1 dominates;  U=2.0: [1.16,1.87,1.09,7.47,6.86] -> order 4.
For U inside the convergence radius the lowest order dominates; outside it the highest computed order does.
Either way one order carries the sign, so aggregation does not average shell effects away.

## (B) Crossover order n* and (C) per-order structure -- also contaminated
Per-order R_n (fixed density n=0.80) does not decay monotonically in n, and the first order where |R_n|<0.05
("unresolvable") jumps with cluster:
  L=2: R_n = -0.44,+0.81,-0.79,-0.01,+0.77   n*=4
  L=3: R_n = -0.64,+0.30,+0.34,-0.29,-0.12   n*=none in range
  L=4: R_n = -0.16,+0.46,-0.36,+0.08         n*=none in range
n* inherits the per-order a_n shell jumps; it is a robust scalar but not a cleanly scaling one here.

## (D) R(mu) on a single cluster oscillates and changes sign
4x4, order 3, beta=4: R(mu) over mu=-3..3 swings -0.12,-0.08,+0.05,-0.10,-0.31,+0.13,+0.05,-0.15,-0.23,
+0.24,-0.22 -- non-smooth even between the non-interacting shell levels (mu=-4,-2,0,2,4). The sign is
acutely sensitive to filling.

## Not tested here
Free-energy differences are a different computation (thermodynamic integration / partition-function
ratios), not this engine's Green's-function estimator; we make no claim about them.

## Verdict (honest)
Among the measurable aggregate observables, none scales cleanly at accessible sizes. The integrated sign
provably cannot help (single-order domination); n* and R_n inherit the per-order a_n shell jumps; R(mu)
oscillates within a single cluster. The contaminant is partial-shell FILLING at small N. The principled
cure the data points to is fixing the filling fraction -- restricting to closed-shell cluster families so
no partial shell is present -- or going to large N where shells become dense; both are out of reach with
the current small-cluster, fixed-order toolkit. So the honest status stands from v39, now stress-tested:
no clean sign-scaling benchmark is extractable at accessible sizes with these observables. That limit --
not a tidy exponent -- is the result. Reproduce: make robust.
