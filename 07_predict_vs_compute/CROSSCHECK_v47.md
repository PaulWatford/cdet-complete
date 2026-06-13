# Cross-check (v47) — fully stochastic shifted CDet: sample the mu-derivatives directly, one run

Reproduce: 08_2d_interacting (make sampler). Completes v45 (exact proof) -> v46 (engine route, FD) -> v47
(direct sampling, no FD). The counterterm = d/dmu insertions are evaluated per Monte-Carlo sample by a contour
in complex mu on the SAME sampled vertices: one run yields a_m and all a_m^{(j)}.

## Faithful C_V
Python port of engine/cdet_engine.c (D_corr/D_vac/Rossi), vectorised over the complex-mu circle. Validated:
G0 reproduces lattice_G0 to 1e-16; piecewise-quadrature a_1 reproduces ED to 1e-16 (split at external times,
as cdet_small does).

## Verified (2-site ring, mu=1.1, beta=4, U=4, alpha=1.5; sampled at mu_ref=-0.4)
- a1   direct +0.034225(363)  ED +0.034347  (0.3 sigma)
- a1'  direct +0.030091(174)  ED +0.030150  (0.3 sigma)  [mu-derivative sampled, independently checked vs ED]
- a2   direct -0.004596(312)  ED -0.004547  (0.2 sigma)
- b1   direct +0.03369(145)   ED-shifted +0.03418  (0.3 sigma)
- b2   direct +0.03961(511)   ED-shifted +0.04074  (0.2 sigma)
All within MC error; the sampled mu-derivative is verified against ED's Cauchy-in-mu value (not merely
self-consistent).

## Significance
The complex-mu contour on shared samples is the analytic d/dmu (density-operator) insertion: exact per-sample
derivatives, so NO finite-difference bias (v46 FD had ~1e-5) and NO mu-grid re-sampling. One run -> all
mu-derivatives -> shifted coeffs. With v45/v46: bare diverges at this (mu,U) yet the low-order shifted coeffs,
now from a single stochastic run, converge.

## Honesty
Orders 1-2 verified to MC statistics; C_V port bit-faithful to the engine (G0, a_1 to 1e-16). Python REFERENCE
implementation of the production estimator; porting the contour into the C mc2d high-order sampler is an
unshipped optimisation. Frozen engine UNTOUCHED (194/194; cdet_order constants bit-identical). An equivalent
jet (forward-mode d/dmu G0) would give the same derivatives without complex arithmetic.
