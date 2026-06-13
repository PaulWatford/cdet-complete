# Fully stochastic shifted CDet: sample the mu-derivatives directly, one run (v47)

The last step from exact-proof to a fully stochastic shifted CDet. v45 proved the shifted-reference scheme
exactly (ED); v46 realised it through the engine but used a mu-grid + finite differences for the mu-derivatives.
v47 removes both: the one-body counterterm = d/dmu insertions are evaluated analytically per Monte-Carlo
sample by a contour in COMPLEX mu on the SAME sampled vertex configurations. One set of vertex samples yields
a_m AND all its mu-derivatives a_m^{(j)} at once -- no finite-difference bias, no mu-grid re-sampling -- and the
v46 resummation b_n = sum_j (alpha^j/j!) U^(n-j) a_{n-j}^{(j)}(mu-alpha) gives the shifted coeffs in one run.

## Faithful connected determinant
C_V is a Python port of the frozen engine (engine/cdet_engine.c D_corr/D_vac/Rossi recursion), vectorised
over the complex-mu circle. Validated: the propagator reproduces lattice_G0 to 1e-16, and the piecewise-
quadrature-integrated a_1 reproduces ED to 1e-16 (the kinks at the external times must be split, exactly as
cdet_small does). So the sampler computes the same connected determinant as the validated C engine.

## Verification (2-site ring, mu=1.1, beta=4, U=4, alpha=1.5; sampled at mu_ref=-0.4)
Bare coeffs and their mu-derivative, all from ONE run (vs ED):
  a1   direct +0.034225 +- 0.000363   ED +0.034347   (0.3 sigma)
  a1'  direct +0.030091 +- 0.000174   ED +0.030150   (0.3 sigma)   <- mu-derivative, sampled, no FD
  a2   direct -0.004596 +- 0.000312   ED -0.004547   (0.2 sigma)
The mu-derivative a1' is independently cross-checked against ED's Cauchy-in-mu value (0.3 sigma) -- so the
derivative SAMPLING is verified, not merely self-consistent.

Shifted coeffs assembled from the one-run sampled mu-derivatives (vs ED shifted):
  b1   direct +0.03369 +- 0.00145   ED +0.03418   (0.3 sigma)
  b2   direct +0.03961 +- 0.00511   ED +0.04074   (0.2 sigma)

## Why this is the production form
The complex-mu contour on shared samples IS the analytic density-operator (d/dmu) insertion: it returns the
exact derivative of each sampled configuration, so there is no finite-difference truncation bias (v46's FD
mu-derivative had ~1e-5 bias) and no need to re-run the sampler at a grid of mu. One run delivers a_m and
every a_m^{(j)} needed for the shift. Combined with v45/v46: the bare series at this (mu,U) diverges, yet a
few low-order shifted coeffs -- now obtainable in a single stochastic run -- converge.

## Honest scope
- VERIFIED: orders 1-2 to MC statistics (0.2-0.3 sigma), with the sampled mu-derivative independently checked
  against ED. The C_V port is bit-faithful to the engine (G0 and a_1 match to 1e-16).
- This is a Python REFERENCE implementation of the production estimator (vectorised over the mu-contour),
  demonstrating the method end-to-end. Porting the complex-mu contour into the C mc2d high-order sampler is a
  straightforward optimisation, not done here; the frozen engine is untouched (still 194/194).
- The complex-mu contour is one concrete realisation of the d/dmu insertion; an equivalent forward-mode (jet)
  propagation of d/dmu G0 through the determinant would give the same derivatives without complex arithmetic.
Reproduce: make sampler.
