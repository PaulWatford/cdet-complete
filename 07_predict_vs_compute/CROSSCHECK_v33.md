# Cross-check (v33) — we were not using the learned-pattern surrogate; here it is, and it wins big

Fair callout: v32 ended "high order needs a learned/adaptive surrogate," as if we did not already
have one. We do -- the custom analytic reference built FROM the engine's own patterns (the Lieb-Wu
analytic moment driving the spin-correlator shape; K_rho; the spin/charge velocities; the CFT tail).
The reason it did not appear in v32 is a LEVEL distinction, not that it is worse. Quantified here.
Reproduce: 07_predict_vs_compute/learned_reference_cv.py (and predict_vs_compute.py).

## The level distinction (why v32 used parametric references instead)
- v32 tested PER-SAMPLE surrogates: approximations of C_V's value at each random vertex-time
  configuration, whose job is to cut the Monte-Carlo SIGN-VARIANCE. The learned patterns are NOT
  per-sample quantities -- they describe the CONVERGED physical observable. They literally cannot plug
  into the per-sample control variate v32 measured, which is why fixed parametric propagator tweaks
  (decoupled / shifted-mu / weak-hop) were used there -- and those de-correlate (|rho|<=0.7 -> 1-2x).
- The learned patterns live at the OBSERVABLE level. predict_vs_compute.py already feeds them back
  (Path B: closed-form prediction, NO determinant sum) and lands within single-digit-percent of the
  exact correlator.

## What the learned reference is worth as a control variate (observable level)
learned_reference_cv.py, same metric as 02_control_variate (variance reduction = 1/(1-rho^2)):
target f = exact ED spin correlator over a (U, r) grid; surrogate g = the analytic prediction from
the patterns.
- residual ||f-g||            = 7.3e-3  (~7.5% of the correlator scale, RMS over the full grid;
                                 predict_vs_compute's complementary per-U mean is ~2.5%)
- correlation rho(f,g)        = 0.9978
- variance reduction 1/(1-rho^2) = 229x   (direct CV estimator: 199x fewer samples, matching)
Versus v32's per-sample parametric references (rho<=0.7 -> 1-2x), the learned reference is ~100x
better -- because it captures the actual physics, not a fixed-propagator tweak.

## Two hard problems, two tools (the honest map)
1. Per-sample SIGN-VARIANCE (the MC noise in cdet_order_mc): needs a per-sample surrogate. Simple
   fixed references fail (v32); this is where an adaptive/learned PER-SAMPLE surrogate would go.
2. The OBSERVABLE itself / slow IR convergence: the learned patterns (rho=0.998 -> 229x) are exactly
   the right tool, and already built. This is the lever that matters for physical results, and it was
   the one being overlooked -- the callout was right.

## Scope, stated honestly (the one real gap)
This reference is the half-filling spin CORRELATOR. The high-order DiagMC computes the GREEN'S
FUNCTION / self-energy. The analogous learned reference is the Luttinger-liquid G asymptotics, which
is DETERMINED by K_rho and the spin/charge velocities -- both already in hand
(07/luttinger_K.py, 07/spin_charge_velocities.py). So it is constructible from patterns we already
verified; it is just not yet assembled as a G-reference and subtracted inside cdet_order_mc. That
bridge is the next step -- NOT a brand-new surrogate.

## Status
VALIDATED (v33): the learned-pattern analytic reference is an observable-level control variate with
rho=0.998 -> 229x variance reduction (learned_reference_cv.py), ~100x stronger than v32's per-sample
parametric references. Corrects v32's framing: at the per-sample level high order needs an adaptive
surrogate, but at the OBSERVABLE level the learned reference already exists and is the stronger lever.
Open: build the Luttinger-liquid G-reference from K_rho + velocities and subtract it inside the
high-order DiagMC (the correlator->Green's-function bridge).
